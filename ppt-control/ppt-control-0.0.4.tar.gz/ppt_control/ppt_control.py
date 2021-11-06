import sys
sys.coinit_flags= 0
import win32com.client
import pywintypes
import os
import shutil
import socketserver
import threading
import asyncio
import websockets
import logging, logging.handlers
import json
import urllib
import posixpath
import time
import pythoncom
import pystray
from PIL import Image
from pystray._util import win32
from copy import copy

import ppt_control.__init__ as pkg_base
import ppt_control.http_server_39 as http_server    # 3.9 version of the HTTP server (details in module)
import ppt_control.config as config

logging.basicConfig()

http_daemon = None
my_http_server = None
ws_daemon = None
users = set()
logger = None
refresh_daemon = None
icon = None
ppt_application = None
ppt_presentations = {}
disable_protected_attempted = set()

PKG_NAME = pkg_base.__name__
PKG_VERSION = pkg_base.__version__
DELAY_CLOSE = 0.2
DELAY_PROTECTED = 0.5
DELAY_FINAL = 0.1

class MyIcon(pystray.Icon):
    """
    Custom pystray.Icon class which displays menu when left-clicking on icon, as well as the 
    default right-click behaviour.
    """
    def _on_notify(self, wparam, lparam):
        """Handles ``WM_NOTIFY``.
        If this is a left button click, this icon will be activated. If a menu
        is registered and this is a right button click, the popup menu will be
        displayed.
        """
        if lparam == win32.WM_LBUTTONUP or (
                self._menu_handle and lparam == win32.WM_RBUTTONUP):
            super()._on_notify(wparam, win32.WM_RBUTTONUP)

class Handler(http_server.SimpleHTTPRequestHandler):
    """
    Custom handler to translate /cache* urls to the cache directory (set in the config)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.realpath(__file__)) + r'''\static''')
        
    def log_request(self, code='-', size='-'):
        return

        
    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = list(filter(None, words))
        if len(words) > 0 and words[0] == "cache":
            if words[1] in ppt_presentations:
                path = config.prefs["Main"]["cache"]
            else:
                path = "black.jpg"
                logger.warning("Request for cached file {} for non-existent presentation".format(path))
            words.pop(0)
        else:
            path = self.directory
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

async def ws_handler(websocket, path):
    """
    Handle a WebSockets connection
    """
    logger.debug("Handling WebSocket connection")
    recv_task = asyncio.ensure_future(ws_receive(websocket, path))
    send_task = asyncio.ensure_future(ws_send(websocket, path))
    done, pending = await asyncio.wait(
        [recv_task, send_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

async def ws_receive(websocket, path):
    """
    Process data received on the WebSockets connection
    """
    users.add(websocket)
    try:
        # Send initial state to clients on load
        for pres in ppt_presentations:
            broadcast_presentation(ppt_presentations[pres])
        async for message in websocket:
            logger.debug("Received websocket message: " + str(message))
            data = json.loads(message)
            if data["presentation"]:
                pres = ppt_presentations[data["presentation"]]
            else:
                # Control last-initialised presentation if none specified (e.g. if using OBS script
                # which doesn't have any visual feedback and hence no method to choose a
                # presentation). This relies on any operations on the ppt_presentations dictionary
                # being stable so that the order does not change. So far no problems have been
                # detected with this, but it is not an ideal method.
                pres = ppt_presentations[list(ppt_presentations.keys())[-1]]
            if data["action"] == "prev":
                pres.prev()
            elif data["action"] == "next":
                pres.next()
                # Advancing to the black screen before the slideshow ends doesn't trigger 
                # ApplicationEvents.OnSlideShowNextSlide, so we have to check for that here and
                # broadcast the new state if necessary. A delay is required since the event is 
                # triggered before the slideshow is actually closed, and we don't want to attempt
                # to check the current slide of a slideshow that isn't running.
                time.sleep(DELAY_FINAL)
                if (pres.get_slideshow() is not None and 
                        pres.slide_current() == pres.slide_total() + 1):
                    logger.debug("Advanced to black slide before end")
                    broadcast_presentation(pres)
            elif data["action"] == "first":
                pres.first()
            elif data["action"] == "last":
                pres.last()
            elif data["action"] == "black":
                if pres.state() == 3 or (
                    config.prefs["Main"]["blackwhite"] == "both" and pres.state() == 4):
                    pres.normal()
                else:
                    pres.black()
            elif data["action"] == "white":
                if pres.state() == 4  or (
                    config.prefs["Main"]["blackwhite"] == "both" and pres.state() == 3):
                    pres.normal()
                else:
                    pres.white()
            elif data["action"] == "goto":
                pres.goto(int(data["value"]))
                # Advancing to the black screen before the slideshow ends doesn't trigger 
                # ApplicationEvents.OnSlideShowNextSlide, so we have to check for that here and
                # broadcast the new state if necessary. A delay is required since the event is 
                # triggered before the slideshow is actually closed, and we don't want to attempt
                # to check the current slide of a slideshow that isn't running.
                time.sleep(DELAY_FINAL)
                if (pres.get_slideshow() is not None and 
                        pres.slide_current() == pres.slide_total() + 1):
                    logger.debug("Jumped to black slide before end")
                    broadcast_presentation(pres)
            elif data["action"] == "start":
                pres.start_slideshow()
            elif data["action"] == "stop":
                pres.stop_slideshow()
            else:
                logger.error("Received unnsupported event: {}", data)
    finally:
        users.remove(websocket)

async def ws_send(websocket, path):
    """
    Broadcast data to all WebSockets clients
    """
    while True:
        message = await ws_queue.get()
        await asyncio.wait([user.send(message) for user in users])


def run_http():
    """
    Start the HTTP server
    """
    global my_http_server
    my_http_server = http_server.HTTPServer((config.prefs["HTTP"]["interface"], config.prefs.getint("HTTP", "port")), Handler)
    my_http_server.serve_forever()


def run_ws():
    """
    Set up threading/async for WebSockets server
    """
    # https://stackoverflow.com/questions/21141217/how-to-launch-win32-applications-in-separate-threads-in-python/22619084#22619084
    # https://www.reddit.com/r/learnpython/comments/mwt4qi/pywintypescom_error_2147417842_the_application/
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    asyncio.set_event_loop(asyncio.new_event_loop())
    global ws_queue
    ws_queue = asyncio.Queue()
    global loop
    loop = asyncio.get_event_loop()
    start_server = websockets.serve(ws_handler, config.prefs["WebSocket"]["interface"], config.prefs.getint("WebSocket", "port"), ping_interval=None)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def setup_http():
    """
    Set up threading for HTTP server
    """
    http_daemon = threading.Thread(name="http_daemon", target=run_http)
    http_daemon.setDaemon(True)
    http_daemon.start()
    logger.info("Started HTTP server")

def setup_ws():
    """
    Set up threading for WebSockets server
    """
    global ws_daemon
    ws_daemon = threading.Thread(name="ws_daemon", target=run_ws)
    ws_daemon.setDaemon(True)
    ws_daemon.start()
    logger.info("Started websocket server")
    

def broadcast_presentation(pres):
    """
    Broadcast the state of a single presentation to all connected clients. Also ensures the current
    slide and the two upcoming slides are exported and cached.
    """
    name = pres.presentation.Name
    pres_open = name in ppt_presentations
    slideshow = pres.slideshow is not None
    visible = pres.state()
    slide_current = pres.slide_current()
    slide_total = pres.slide_total()

    pres.export_current_next()
    
    if users:   # asyncio.wait doesn't accept an empty list
        state = {"name": name, "pres_open": pres_open, "slideshow": slideshow, "visible": visible,
                    "slide_current": slide_current, "slide_total": slide_total}
        loop.call_soon_threadsafe(ws_queue.put_nowait, json.dumps({"type": "state", **state}))

class ApplicationEvents:
    """
    Events assigned to the root application.
    Ref: https://docs.microsoft.com/en-us/office/vba/api/powerpoint.application#events
    """
    def OnSlideShowNextSlide(self, window, *args):
        """
        Triggered when the current slide number of any slideshow is incremented, locally or through
        ppt_control.
        """
        logger.debug("Slide advanced for {}".format(window.Presentation.Name))
        broadcast_presentation(ppt_presentations[window.Presentation.Name])

    def OnSlideShowPrevSlide(self, window, *args):
        """
        Triggered when the current slide number of any slideshow is decremented, locally or through
        ppt_control.
        """
        logger.debug("Slide decremented for {}".format(window.Presentation.Name))
        broadcast_presentation(ppt_presentations[window.Presentation.Name])
    
    def OnAfterPresentationOpen(self, presentation, *args):
        """
        Triggered when an existing presentation is opened. This adds the newly opened presentation
        to the list of open presentations.
        """
        logger.debug("Presentation {} opened - adding to list".format(presentation.Name))
        global ppt_presentations
        ppt_presentations[presentation.Name] = Presentation(ppt_application, pres_obj=presentation)
        broadcast_presentation(ppt_presentations[presentation.Name])
        disable_protected_attempted.discard(presentation.Name)
        icon.notify("Connected to {}".format(presentation.Name), PKG_NAME)

    def OnAfterNewPresentation(self, presentation, *args):
        """
        Triggered when a new presentation is opened. This adds the new presentation to the list
        of open presentations.
        """
        logger.debug("Presentation {} opened (blank) - adding to list".format(presentation.Name))
        global ppt_presentations
        ppt_presentations[presentation.Name] = Presentation(ppt_application, pres_obj=presentation)
        broadcast_presentation(ppt_presentations[presentation.Name])
        icon.notify("Connected to {}".format(presentation.Name), PKG_NAME)

    def OnPresentationClose(self, presentation, *args):
        """
        Triggered when a presentation is closed. This removes the presentation from the list of
        open presentations. A delay is included to make sure the presentation is 
        actually closed, since the event is called simultaneously as the presentation is removed
        from PowerPoint's internal structure. Ref:
        https://docs.microsoft.com/en-us/office/vba/api/powerpoint.application.presentationclose
        """
        logger.debug("Presentation {} closed - removing from list".format(presentation.Name))
        global ppt_presentations
        time.sleep(DELAY_CLOSE)
        broadcast_presentation(ppt_presentations.pop(presentation.Name))
        icon.notify("Disconnected from {}".format(presentation.Name), PKG_NAME)

    def OnSlideShowBegin(self, window, *args):
        """
        Triggered when a slideshow is started. This initialises the Slideshow object in the 
        appropriate Presentation object.
        """
        logger.debug("Slideshow started for {}".format(window.Presentation.Name))
        global ppt_presentations
        ppt_presentations[window.Presentation.Name].slideshow = window
        broadcast_presentation(ppt_presentations[window.Presentation.Name])
    
    def OnSlideShowEnd(self, presentation, *args):
        """
        Triggered when a slideshow is ended. This deinitialises the Slideshow object in the 
        appropriate Presentation object.
        """
        logger.debug("Slideshow ended for {}".format(presentation.Name))
        global ppt_presentations
        ppt_presentations[presentation.Name].slideshow = None
        broadcast_presentation(ppt_presentations[presentation.Name])


class Presentation:
    """
    Class representing an instance of PowerPoint with a file open (so-called "presentation"
    in PowerPoint terms). Mostly just a wrapper for PowerPoint's `Presentation` object.
    """
    def __init__(self, application, pres_index=None, pres_obj=None):
        """
        Initialise a Presentation object.
            application     The PowerPoint application which the presentation is being run within
            pres_index      PowerPoint's internal presentation index (NOTE this is indexed from 1)
        """
        if pres_index == None and pres_obj == None:
            raise ValueError("Cannot initialise a presentation without a presentation ID or object")
        assert len(application.Presentations) > 0, "Cannot initialise presentation from application with no presentations"

        self.__application = application
        if pres_obj is not None:
            self.presentation = pres_obj
        else:
            self.presentation = application.Presentations(pres_index)
        self.slideshow = self.get_slideshow()


    def get_slideshow(self):
        """
        Check whether the presentation is in slideshow mode, and if so, return the SlideShowWindow.
        """
        try:
            return self.presentation.SlideShowWindow
        except pywintypes.com_error as exc:
            logger.debug("Couldn't get slideshow for {}: {}".format(self.presentation.Name, exc))
            return None

    def start_slideshow(self):
        """
        Start the slideshow. Updating the state of this object is managed by the OnSlideshowBegin 
        event of the applicable Application.
        """
        if self.get_slideshow() is None:
            self.presentation.SlideShowSettings.Run()
        else:
            logger.warning("Cannot start slideshow that is already running (presentation {})".format(
                self.presentation.Name))

    def stop_slideshow(self):
        """
        Stop the slideshow. Updating the state of this object is managed by the OnSlideshowEnd
        event of the applicable Application.
        """
        if self.get_slideshow() is not None:
            self.presentation.SlideShowWindow.View.Exit()
        else:
            logger.warning("Cannot stop slideshow that is not running (presentation {})".format(
                self.presentation.Name))

    def state(self):
        """
        Returns the visibility state of the slideshow:
        1: running
        2: paused
        3: black
        4: white
        5: done
        Source: https://docs.microsoft.com/en-us/office/vba/api/powerpoint.ppslideshowstate
        """
        if self.slideshow is not None:
            return self.slideshow.View.State
        else:
            return 0

    def slide_current(self):
        """
        Returns the current slide number of the slideshow, or 0 if no slideshow is running.
        """
        if self.slideshow is not None:
            return self.slideshow.View.CurrentShowPosition
        else:
            return 0

    def slide_total(self):
        """
        Returns the total number of slides in the presentation, regardless of whether a slideshow
        is running.
        """
        return self.presentation.Slides.Count

    def prev(self):
        """
        Go to the previous slide if there is a slideshow running. Notifying clients of the new state
        is managed by the ApplicationEvent.
        """
        assert self.slideshow is not None, "Slideshow is not running for {}".format(self.presentation.Name)
        self.slideshow.View.Previous()

    def next(self):
        """
        Go to the previous slide if there is a slideshow running. Notifying clients of the new state
        is managed by the ApplicationEvent.
        """
        assert self.slideshow is not None, "Slideshow is not running for {}".format(self.presentation.Name)
        self.slideshow.View.Next()

    def first(self):
        """
        Go to the first slide if there is a slideshow running. Notifying clients of the new state
        is managed by the ApplicationEvent.
        """
        assert self.slideshow is not None, "Slideshow is not running for {}".format(self.presentation.Name)
        self.slideshow.View.First()
                
    def last(self):
        """
        Go to the last slide if there is a slideshow running. Notifying clients of the new state
        is managed by the ApplicationEvent.
        """
        assert self.slideshow is not None, "Slideshow is not running for {}".format(self.presentation.Name)
        self.slideshow.View.Last()

    def goto(self, slide):
        """
        Go to a numbered slide if there is a slideshow running. Notifying clients of the new state
        is managed by the ApplicationEvent.
        """
        assert self.slideshow is not None, "Slideshow is not running for {}".format(self.presentation.Name)
        if slide <= self.slide_total():
            self.slideshow.View.GotoSlide(slide)
        else:
            self.last()
            self.next()

    def normal(self):
        """
        Make the slideshow visible if there is a slideshow running. Note this puts the slideshow into 
        "running" state rather than the normal "paused" to ensure animations work correctly and the 
        slide is actually visible after changing the state. The state is normally returned to 
        "paused" automatically by PPT when advancing to the following slide. State enumeration ref: 
        https://docs.microsoft.com/en-us/office/vba/api/powerpoint.ppslideshowstate
        """
        assert self.slideshow is not None, "Slideshow is not running for {}".format(self.presentation.Name)
        self.slideshow.View.State = 1
        broadcast_presentation(self)

    def black(self):
        """
        Make the slideshow black if there is a slideshow running. 
        """
        assert self.slideshow is not None, "Slideshow is not running for {}".format(self.presentation.Name)
        self.slideshow.View.State = 3
        broadcast_presentation(self)

    def white(self):
        """
        Make the slideshow white if there is a slideshow running. 
        """
        assert self.slideshow is not None, "Slideshow is not running for {}".format(self.presentation.Name)
        self.slideshow.View.State = 4
        broadcast_presentation(self)

    def export_current_next(self):
        """
        Export the current slide, the next slide, and the one after (ensures enough images are 
        always cached)
        """
        self.export(self.slide_current())
        self.export(self.slide_current() + 1)
        self.export(self.slide_current() + 2)

    def export(self, slide):
        """
        Export a relatively low-resolution image of a slide using PowerPoint's built-in export 
        function. The cache destination is set in the config. The slide is not exported if it has 
        a non-stale cached file.
        """
        destination = config.prefs["Main"]["cache"] + "\\" + self.presentation.Name + "\\" + str(slide) + "." + config.prefs["Main"]["cache_format"].lower()
        logger.debug("Exporting slide {} of {}".format(slide, self.presentation.Name))
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        if not os.path.exists(destination) or (config.prefs.getint("Main", "cache_timeout") > 0 and 
                time.time() - os.path.getmtime(destination) > config.prefs.getint("Main", "cache_timeout")):
            if slide <= self.slide_total():
                attempts = 0
                while attempts < 3:
                    try:
                        self.presentation.Slides(slide).Export(destination, config.prefs["Main"]["cache_format"])
                        break
                    except:
                        pass
                    attempts += 1
            elif slide == self.slide_total() + 1:
                try:
                    shutil.copyfileobj(open(os.path.dirname(os.path.realpath(__file__)) + r'''\static\black.jpg''', 'rb'), open(destination, 'wb'))
                except Exception as exc:
                    logger.warning("Failed to copy black slide (number {} for presentation {}): {}".format(slide, self.presentation.Name, exc))
            else:
                pass

    def export_all(self):
        """
        Export all slides in the presentation
        """
        for i in range(1, self.slide_total() + 2):
            self.export(i)

def null_action(*args):
    """
    Placeholder for disabled menu items in systray
    """
    pass

def edit_config(*args):
    """
    Open the config file for editing in Notepad, and create the directory if not existing
    """
    logger.debug("Opening config {}".format(pkg_base.CONFIG_PATH))
    if not os.path.exists(pkg_base.CONFIG_DIR):
        try:
            os.makedirs(pkg_base.CONFIG_DIR)
            logger.info("Made directory {}".format(pkg_base.CONFIG_DIR))
        except Exception as exc:
            logger.warning("Failed to create directory {} for config file".format(
                pkg_base.CONFIG_DIR))
            icon.notify("Create {} manually".format((pkg_base.CONFIG_DIR[:40] + '...') 
                        if len(pkg_base.CONFIG_DIR) > 40 else pkg_base.CONFIG_DIR),
                        "Failed to create config directory")
    try:
        os.popen("notepad.exe {}".format(pkg_base.CONFIG_PATH))
    except Exception as exc:
        logger.warning("Failed to edit config {}: {}".format(pkg_base.CONFIG_PATH, exc))
        icon.notify("Edit {} manually".format((pkg_base.CONFIG_PATH[:40] + '...') 
                        if len(pkg_base.CONFIG_PATH) > 40 else pkg_base.CONFIG_PATH),
                        "Failed to open config")
                
def refresh():
    """
    Clear COM events and update interface elements at an interval defined in "refresh" in the config
    TODO: fix "argument of type 'com_error' is not iterable"
    """
    while getattr(refresh_daemon, "do_run", True):
        try:
            pythoncom.PumpWaitingMessages()
            # TODO: don't regenerate entire menu on each refresh, use pystray.Icon.update_menu()
            icon.menu = (pystray.MenuItem("Status: " + "dis"*(len(ppt_presentations) == 0) + "connected",
                lambda: null_action(), enabled=False),
                pystray.MenuItem("Stop", lambda: exit(icon)),
                pystray.MenuItem("Edit config", lambda: edit_config()))
            manage_protected_view(ppt_application)
            time.sleep(float(config.prefs["Main"]["refresh"]))
        except Exception as exc:
            # Deal with any exceptions, such as RPC server restarting, by reconnecting to application
            # (if this fails again, that's okay because we'll keep trying until it works)
            logger.error("Error whilst refreshing state: {}".format(exc))
            app = get_application()
        

def get_application():
    """
    Create an Application object representing the PowerPoint application installed on the machine.
    This should succeed regardless of whether PowerPoint is running, as long as PowerPoint is
    installed.
    Returns the Application object if successful, otherwise returns None.
    """
    try:
        return win32com.client.Dispatch('PowerPoint.Application')
    except pywintypes.com_error:
        # PowerPoint is probably not installed, or other COM failure
        return None
        

def manage_protected_view(app):
    """
    Attempt to unlock any presentations that have been opened in protected view. These cannot be
    controlled by the program whilst they are in protected view, so we attempt to disable protected
    view, or show a notification if this doesn't work for some reason.
    """
    try:
        if app.ProtectedViewWindows.Count > 0:
            logger.debug("Found open presentation(s) but at least one is in protected view")
            for i in range(1, app.ProtectedViewWindows.Count + 1):  # +1 to account for indexing from 1
                pres_name = app.ProtectedViewWindows(i).Presentation.Name
                if pres_name in disable_protected_attempted:
                    continue
                if config.prefs.getboolean("Main", "disable_protected"):
                    try:
                        app.ProtectedViewWindows(i).Edit()
                        logger.info("Enabled editing for {}".format(pres_name))
                    except Exception as exc:
                        icon.notify("Failed to disable protected view on \"{}\"".format((pres_name[:22] + '...') 
                        if len(pres_name) > 25 else pres_name), "Disable protected view in PowerPoint")
                        logger.warning("Failed to disable protected view {} for editing - do this manually: {}".format(pres_name, exc))
                        disable_protected_attempted.add(pres_name)
                else:
                    icon.notify("Cannot control \"{}\" in protected view".format((pres_name[:22] + '...') 
                        if len(pres_name) > 25 else pres_name), "Disable protected view in PowerPoint")
                    logger.warning("Cannot control {} in protected view, and automatic disabling of protected view is turned off".format(pres_name))
                    disable_protected_attempted.add(pres_name)
    except Exception as exc:
        if type(exc) == pywintypes.com_error and "application is busy" in exc:
            # PowerPoint needs some time to finish loading file if it has just been opened,
            # otherwise we get "The message filter indicated that the application is busy". Here,
            # we deal with this by gracefully ignoring any protected view windows until the next 
            # refresh cycle, when PowerPoint is hopefully finished loading (if the refresh interval
            # is sufficiently long).
            logger.debug("COM interface not taking requests right now - will try again on next refresh")
            return
        # Sometimes gets pywintypes.com_error "The object invoked has disconnected from its clients"
        # at this point.
        logger.warning("{} whilst dealing with protected view windows: {}".format(type(exc), exc))
        app = get_application()



def connect_ppt():
    """
    Connect to the PowerPoint COM interface and perform initial enumeration of open files 
    ("presentations"). Files that are subsequently opened are dealt with using COM events (see the
    ApplicationEvents class above). Therefore, once we are finished setting things up, we just 
    call refresh() as a daemon in order to keep clients up to date.
    """
    logger.debug("Searching for a PowerPoint slideshow...")
    global ppt_application
    global ppt_presentations

    # Initialise PowerPoint application
    ppt_application = get_application()
    if ppt_application is None:
        # Couldn't find PowerPoint application
        icon.notify("Couldn't find PowerPoint application", "Error starting {}".format(PKG_NAME))
        logger.error("Couldn't find PowerPoint application - check that PowerPoint is installed and COM is working")
        sys.exit()

    # Continue because we can connect to PowerPoint
    logger.debug("Found PowerPoint application")

    # Dispatch events
    win32com.client.WithEvents(ppt_application, ApplicationEvents)
    logger.debug("Dispatched events")

    # Deal with windows in protected view
    manage_protected_view(ppt_application)

    # Initial enumeration of open presentations
    logger.debug("Enumerating {} presentation(s)".format(len(ppt_application.Presentations)))
    for n in range(1, len(ppt_application.Presentations)+1):    # PowerPoint's slide indexing starts at 1.. why!?!?!?
        pres = Presentation(ppt_application, n)
        icon.notify("Connected to {}".format(pres.presentation.Name), PKG_NAME)
        logger.debug("Found presentation {} with index {}".format(pres.presentation.Name, n))
        ppt_presentations[pres.presentation.Name] = pres
    refresh_daemon = threading.Thread(name="refresh_daemon", target=refresh)
    refresh_daemon.setDaemon(True)
    logger.debug("Handing over to refresh daemon - goodbye...")
    if len(ppt_presentations) == 0:
        # Provide some confirmation that the program has started if we haven't sent any 
        # connection notifications yet
        icon.notify("Started server", PKG_NAME)
    refresh_daemon.start()


def start_server(_=None):
    """
    Start HTTP and WS servers, then connect to PPT instance with connect_ppt() which will then 
    set off the refresh daemon.
    """
    setup_http()
    setup_ws()
    connect_ppt()
        
        
def exit(icon):
    """
    Clean up and exit when user clicks "Stop" from systray menu
    """
    logger.debug("User requested shutdown")
    icon.visible = False
    icon.stop()


def start_interface():
    """
    Main entrypoint for the program. Loads config and logging, starts systray icon, and calls
    start_server() to start the backend.
    """
    global icon
    global logger
    # Load config
    config.prefs = config.loadconf(pkg_base.CONFIG_PATH)

    # Set up logging
    if config.prefs["Main"]["logging"] == "debug":
        log_level = logging.DEBUG
    elif config.prefs["Main"]["logging"] == "info":
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-7.7s]  %(message)s")
    logger = logging.getLogger("ppt-control")
    logger.setLevel(log_level)
    logger.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)

    if not os.path.exists(pkg_base.LOG_DIR):
        try:
            os.makedirs(pkg_base.LOG_DIR)
            logger.info("Made directory {}".format(pkg_base.LOG_DIR))
        except Exception as exc:
            logger.warning("Failed to create directory {} for log".format(
                pkg_base.LOG_DIR))
            icon.notify("Create {} manually".format((pkg_base.LOG_DIR[:40] + '...') 
                        if len(pkg_base.LOG_DIR) > 40 else pkg_base.LOG_DIR),
                        "Failed to create log directory")
    file_handler = logging.FileHandler(pkg_base.LOG_PATH)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    #logging.getLogger("asyncio").setLevel(logging.ERROR)
    #logging.getLogger("asyncio.coroutines").setLevel(logging.ERROR)
    logging.getLogger("websockets.server").setLevel(logging.ERROR)
    #logging.getLogger("websockets.protocol").setLevel(logging.ERROR)


    logger.debug("Finished setting up config and logging")

    # Start systray icon and server
    logger.debug("Starting system tray icon")
    icon = MyIcon(PKG_NAME)
    icon.icon = Image.open(os.path.dirname(os.path.realpath(__file__)) + r'''\static\icons\ppt.ico''')
    icon.title = "{} {}".format(PKG_NAME, PKG_VERSION)
    icon.visible = True
    icon.run(setup=start_server)

    # Exit when icon has stopped
    sys.exit(0)

if __name__ == "__main__":
    start_interface()
