"""
    domonic.window
    ====================================

    be mindful there are 2 types of window to be found in domonic:

        1. the javascript window - a window with only static js methods

        2. the domonic window (this one) - a window connected to other things i.e. dom

    You can extend or import either for your own purposes.

"""
import sys

from domonic import domonic
from domonic.javascript import Window
from domonic.dom import *
from domonic.dom import document, Location

from domonic.webapi import Storage

# TODO - test
class CustomElementRegistry():
    """ The CustomElementRegistry interface provides methods for registering custom elements and querying registered elements.
    To get an instance of it, use the window.customElements property. """

    def __init__(self):
        self.store = {}

    # Defines a new custom element.
    def define(self, name, constructor, options=None):
        """[defines a new custom element.]

        Args:
            name ([str]): [Name for the new custom element. Note that custom element names must contain a hyphen.]
            constructor ([type]): [Constructor for the new custom element.]
            options ([dict]): [Object that controls how the element is defined. One option is currently supported: extends]
        """
        if '-' not in name:
            raise ValueError('Invalid custom element name. Must contain hypen: ' + name)
        # el = document.createElement(name)
        # el.constructor = constructor
        from domonic.html import tag
        from domonic.dom import Element
        el = type(name, (tag, Element), {'name': name, '__init__': constructor})
        if options is not None:
            if 'extends' in options:
                el.extends = options['extends']
        self.store[name] = el
        return el

    def get(self, name):
        """
            Returns the constructor for the named custom element,
            or undefined if the custom element is not defined.
        """
        # see if its in the store or return none
        if name in self.store:
            return self.store[name]
        else:
            return None

    # Upgrades a custom element directly, even before it is connected to its shadow root.
    def upgrade(self):
        pass

    # Returns an empty promise that resolves when a custom element becomes defined with the given name.
    # If such a custom element is already defined, the returned promise is immediately fulfilled.
    def whenDefined(self):
        pass


from domonic.webapi.netinfo import NetworkInformation
from domonic.webapi.credentials import CredentialsContainer
from domonic.webapi.geo import Geolocation

# from domonic.webapi.mediacapabilities import MediaCapabilities
# from domonic.webapi.mediasession import MediaSession


class Navigator(object):
    """ Navigator """

    # Determines whether cookies are enabled in the browser
    cookieEnabled = False

    # Determines whether the browser is online
    # onLine = False
    @property
    def onLine(self):
        raise NotImplementedError

    # Returns the name of the browser Navigator
    appName = "domonic"

    def __init__(self, *args, **kwargs):
        self.connection = NetworkInformation()
        self.credentials = CredentialsContainer()
        self.geolocation = Geolocation()
        self.hid = None
        self.keyboard = None
        self.locks = None
        self.mediaCapabilities = None
        self.mediaSession = None
        self.mediaDevices = None
        self.presentation = None
        self.serial = None
        self.serviceWorker = None
        self.storage = None
        self.vendor = None
        self.webdriver = None
        self.xr = None
        self.buildID = None
        self.contacts = None


    # @property
    # def appVersion():
        """ Returns the version information of the browser """
        # from domonic import __version__
        # return __version__

    # @property
    # def language():
        """ Returns the language of the browser Navigator """
        # import locale
        # return locale.getdefaultlocale()

    # def languages

    @property
    def platform(self):
        """ Returns the platform """
        if 'darwin' in sys.platform:
            return 'mac'
        elif 'linux' in sys.platform:
            return 'linux'
        elif 'win32' in sys.platform:
            return 'windows'
        else:
            return 'unknown'

    @property
    def product(self):
        """ Returns the product name """
        return self.appName

    @property
    def userAgent(self):
        """ Returns the user-agent header sent by the browser to the server Navigator """
        raise NotImplementedError

    @property
    def deviceMemory(self):
        """ Returns the amount of memory available on the device """
        return 1

    @property
    def doNotTrack(self):
        """ Returns the value of the doNotTrack attribute of the Navigator object """
        # return False
        return 'lol'

    @property
    def hardwareConcurrency(self):
        """ Returns the number of logical processors available to the browser Navigator """
        return 1

    @property
    def maxTouchPoints(self):
        """ Returns the maximum number of touch points Navigator """
        return 1

    @saticmethod
    def registerProtocolHandler(scheme, url, title):
        """ Registers a new protocol handler Navigator """
        raise NotImplementedError

    @staticmethod
    def requestMediaKeySystemAccess(keySystem, supportedConfigurations):
        """ Requests a new MediaKeySystemAccess object Navigator """
        raise NotImplementedError

    def canShare(self):
        """ Returns whether the browser Navigator can share files """
        return False

    def clearAppBadge(self):
        """ Clears the app badge Navigator """
        raise NotImplementedError

    def getBattery(self):
        """ Returns the battery information Navigator """
        raise NotImplementedError

    @property
    def javaEnabled(self):
        """ Returns whether the browser Navigator supports Java """
        return False

    def vibrate(self, pattern):
        """ Vibrates the device Navigator """
        raise NotImplementedError

    # deprecated
    # Navigator.securitypolicy
    # Navigator.standalone
    # Navigator.wakeLock
    # Navigator.appCodeName
    # Navigator.appName
    # Navigator.appVersion
    # Navigator.activeVRDisplays
    # Navigator.battery
    # Navigator.mimeTypes
    # Navigator.oscpu
    # Navigator.platform
    # Navigator.plugins
    # Navigator.product
    # Navigator.productSub
    # Navigator.vendorSub


class Window(Window):

    def __init__(self):
        self.customElements = CustomElementRegistry()
        # from domonic.dom import document
        # self.document = document

        self._localStorage = Storage()  # TODO - should persist across sessions
        self._sessionStorage = Storage()  # TODO - should reset on page refresh
        self._navigator = Navigator()

        self._location = Location('eventual.technology')
        super(Window, Window).__init__(self)

    @property
    def localStorage(self):
        """ Returns the local storage object """
        return self._localStorage

    @property
    def sessionStorage(self):
        """ Returns the session storage object """
        return self._sessionStorage

    @staticmethod
    def document(self):
        from domonic.dom import document
        return document

    @property
    def location(self):
        return self._location
        # return Location(self.window.location.href)

    @location.setter
    def location(self, value):
        # NOTE - not documented. still unverified
        # self._location = value
        # TODO - load the content of the location using requests
        if value is None:
            return
        import requests
        r = requests.get(value)
        content = r.text  # .encode('utf-8')
        # print(content)
        # content = content.replace('\n', '')
        # content = content.replace('\t', '')
        # content = content.replace(' ', '')
        # content = content.replace('\r', '')

        from domonic.parsers import remove_tags, remove_doctype
        content = remove_tags(content, ['js', 'css', '#'])
        content = remove_doctype(content)

        # from domonic.utils import Utils
        # content = Utils.escape(content)
        # content = domonic.parsers.remove_html_tag_by_name(content, 'head') # TODO - buggy.removed start of docs too?
        # content = domonic.parsers.remove_html_tag_by_name(content, 'body')

        # clean invalid html
        content.replace('&', '&amp;')
        content = domonic.parsers.remove_whitespace(content)
        content = domonic.parsers.remove_newlines(content)
        content = domonic.parsers.remove_tabs(content)

        print(content)
        # return
        # clean the html before parsing

        # TODO - don't use parseString as it is not a HTML parser its XML parser. atm I'm just using for testing
        self.document = domonic.domonic.parseString(content)
        self._location = Location(value)

    # WINDOW
    # """ Removes focus from an element """
    def blur(self):
        raise NotImplementedError

    # Returns a Boolean value indicating whether a window has been closed or not
    def closed(self):
        raise NotImplementedError

    # Closes the output stream previously opened with document.open()
    def close(self):
        raise NotImplementedError

    def confirm(self, message):
        """[Displays a dialog box with a message and an OK and a Cancel button.]
        (https://developer.mozilla.org/en-US/docs/Web/API/Window/confirm)

        Args:
            message ([type]): [the message to display in the dialog box]
        """
        raise NotImplementedError

    @property
    def defaultStatus(self):
        """ Returns the default status message of the window """
        raise NotImplementedError

    @defaultStatus.setter
    def defaultStatus(self, value=None):
        """ Sets the default text in the statusbar of a window """
        raise NotImplementedError

    def focus(self):
        """ Gives focus to an element """
        raise NotImplementedError

    # Returns the <iframe> element in which the current window is inserted  
    def frameElement(self):
        raise NotImplementedError

    # Gets the current computed CSS styles applied to an element
    def getComputedStyle(self, el, pseudo=None):
        raise NotImplementedError

    # Returns a Selection object representing the range of text selected by the user
    def getSelection(self):
        raise NotImplementedError

    def history(self):
        """ Returns the History object for the window """
        raise NotImplementedError
        # from domonic.webapi.history import History
        # return History()

    def innerHeight(self):
        """[Returns the height of the window's content area (viewport) including scrollbars]
        """
        raise NotImplementedError

    def innerWidth(self):
        """[Returns the width of a window's content area (viewport) including scrollbars]
        """
        raise NotImplementedError

    # Returns a MediaQueryList object representing the specified CSS media query string 
    def matchMedia(self, media_query_list):
        raise NotImplementedError

    def moveBy(self, x: int, y: int):
        """[Moves a window relative to its current position]

        Args:
            x ([int]): [the horizontal offset]
            y ([int]): [the vertical offset]
        """
        raise NotImplementedError

    def moveTo(self, x: int, y: int):
        """[Moves a window to the specified position]

        Args:
            x (int): [the position on the x-axis]
            y (int): [the position on the y-axis]
        """
        raise NotImplementedError

    def name(self):
        """ Returns the name of the window """
        raise NotImplementedError

    @property
    def navigator(self):
        """ Returns the Navigator object for the window """
        return self._navigator
    
    '''
    # # The event occurs when the window's history changes  PopStateEvent?
    # def onpopstate(self):
    #     raise NotImplementedError

    # Opens an HTML output stream to collect output from document.write() Document, Window
    def open(self):
        raise NotImplementedError

    # Returns a reference to the window that created the window 
    def opener(self):
        raise NotImplementedError

    # Returns the height of the browser window, including toolbars/scrollbars Window
    def outerHeight(self):
        raise NotImplementedError

    # Returns the width of the browser window, including toolbars/scrollbars
    def outerWidth(self):
        raise NotImplementedError

    # Returns the pixels the current document has been scrolled (horizontally) from the upper left corner of the window 
    def pageXOffset(self):
        raise NotImplementedError

    # Returns the pixels the current document has been scrolled (vertically) from the upper left corner of the window Window
    def pageYOffset(self):
        raise NotImplementedError

    # Returns the parent window of the current window Window
    def parent(self):
        raise NotImplementedError

    # Prints the content of the current window  
    def _print(self):
        raise NotImplementedError

    # Resizes the window by the specified pixels
    def resizeBy(self):
        raise NotImplementedError

    # Resizes the window to the specified width and height  
    def resizeTo(self):
        raise NotImplementedError

    # Returns the Screen object for the window (See Screen object)  
    def screen(self):
        raise NotImplementedError

    # Returns the horizontal coordinate of the window relative to the screen
    def screenLeft(self):
        raise NotImplementedError

    # Returns the vertical coordinate of the window relative to the screen  
    def screenTop(self):
        raise NotImplementedError

    # Deprecated. This method has been replaced by the scrollTo() method. Window
    def scroll(self):
        raise NotImplementedError

    # Scrolls the document by the specified number of pixels
    def scrollBy(self):
        raise NotImplementedError

    # Scrolls the specified element into the visible area of the browser window   Element
    def scrollIntoView(self):
        raise NotImplementedError

    # Scrolls the document to the specified coordinates  < TODO - this will be fun
    def scrollTo(self):
        raise NotImplementedError

    # An alias of pageXOffset Window
    def scrollX(self):
        raise NotImplementedError

    # An alias of pageYOffset Window
    def scrollY(self):
        raise NotImplementedError

    # Stops the window from loading 
    def stop(self):
        raise NotImplementedError

    # Sets or returns the text in the statusbar of a window 
    def status(self):
        raise NotImplementedError

    # the topmost browser window
    def top(self):
        raise NotImplementedError
    '''

# global window
window = Window()
