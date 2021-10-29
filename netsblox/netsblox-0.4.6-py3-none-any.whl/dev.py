import collections as _collections
import threading as _threading
import traceback as _traceback
import inspect as _inspect
import time as _time
import json as _json
import sys as _sys
import io as _io

from PIL import Image

from typing import Optional, Any, List

import websocket as _websocket
import requests as _requests

import netsblox.common as _common
import netsblox.events as _events

_websocket.enableTrace(False) # disable auto-outputting of socket events

class Client:
    '''
    Holds all the information and plumbing required to connect to netsblox, exchange messages, and call RPCs.
    '''

    def __init__(self, *, run_forever = False):
        '''
        Opens a new client connection to NetsBlox, allowing you to access any of the NetsBlox services from python.

        run_forever prevents the python program from terminating even after the end of your script.
        This is useful if you have long-running programs that are based on message-passing rather than looping.
        Note: this does not stop the main thread of execution from terminating, which could be a problem in environments like Google Colab;
        instead, you can explicitly call wait_till_disconnect() at the end of your program.
        '''

        self._client_id = f'_pyblox{round(_time.time() * 1000)}'
        self._base_url = 'https://dev.netsblox.org'

        # set these up before the websocket since it might send us messages
        self._message_cv = _threading.Condition(_threading.Lock())
        self._message_queue = _collections.deque()
        self._message_handlers = {}
        self._message_last = {} # maps msg type to {received_count, last_content, waiters (count)}
        self._message_stream_stopped = False

        # create a websocket and start it before anything non-essential (has some warmup communication)
        self._ws_lock = _threading.Lock()
        self._ws = _websocket.WebSocketApp(self._base_url.replace('http', 'ws'),
            on_open = self._ws_open, on_close = self._ws_close, on_error = self._ws_error, on_message = self._ws_message)
        self._ws_thread = _threading.Thread(target = self._ws.run_forever)
        self._ws_thread.setDaemon(not run_forever)
        self._ws_thread.start()

        # create a thread to manage the message queue
        self._message_thread = _threading.Thread(target = self._message_router)
        self._message_thread.setDaemon(True)
        self._message_thread.start()

        res = _requests.post(f'{self._base_url}/api/newProject',
            _common.small_json({ 'clientId': self._client_id, 'name': None }),
            headers = { 'Content-Type': 'application/json' })
        res = _json.loads(res.text)
        self._project_id = res['projectId']
        self._project_name = res['name']
        self._role_id = res['roleId']
        self._role_name = res['roleName']

        self.air_quality = AirQuality(self)
        '''
        The AirQuality Service provides access to real-time air quality data using the AirNowAPI.
        For more information, check out https://docs.airnowapi.org/.
        '''

        self.alexa = Alexa(self)
        '''
        The Alexa service provides capabilities for building your own Alexa skills!
        
        An Alexa skill consists of some general information (such as the name to use
        for invocation) as well as a list of supported intents. An intent is a command
        or question to which the skill can respond. Intents consist of a name, list of
        utterances, and any required slots. Utterances are examples of how the user might
        phrase questions or commands. Slots are used to define placeholders for concepts
        like names, cities, etc.
        
        When Alexa determines that a request was made to a given intent, the slots are
        resolved to their corresponding values and then passed to the "handler" for the
        intent.
        '''

        self.autograders = Autograders(self)
        '''
        The Autograders service enables users to create custom autograders for
        use within NetsBlox.
        
        For more information, check out https://editor.netsblox.org/docs/services/Autograders/index.html
        '''

        self.base_x = BaseX(self)
        '''
        The BaseX Service provides access to an existing BaseX instance.
        '''

        self.battleship = Battleship(self)
        '''
        The Battleship Service provides helpful utilities for building a distributed
        game of battleship.
        
        Overview
        --------
        
        Like regular Battleship, the Battleship service has two states: placing ships and shooting at ships.
        During placement, it expects each role to place each ship on his/her board and will not allow the game to proceed to the shooting phase until each role has placed all his/her ships.
        Placement, firing and starting blocks will return true if successful or an error message if it fails.
        
        Blocks
        ------
        
        - place <ship> at <row> <column> facing <direction> - Places a ship on your board with the front at the given row and column facing the given direction. Returns true if placed successfully (eg, on the board and not overlapping another ship). Also, placing a ship twice results in a move (not duplicates).
        - start game - Try to start the game. If both users have all their ships placed, it should return true and send start messages to all roles. Otherwise, it will return with a message saying that it is waiting on a specific role.
        - fire at <row> <column> - This block allows the user to try to fire at the given row and column. It returns true if it was a valid move; otherwise it will return an error message like it's not your turn!. On a successful move, the server will send either a hit or miss message to everyone in the room. Then it will send a your turn message to the player to play next.
        - active ships for <role> - This block returns a list of all ships that are still afloat for the given role. If no role is specified, it defaults to the sender's role.
        - all ships - Returns a list of all ship names. Useful in programmatically placing ships.
        - ship length <ship> - Returns the length of the given ship.
        - restart game - Restarts the given game (all boards, etc)
        
        Message Types
        -------------
        
        - start - Received when start game finishes successfully for any role. After game has officially started, users can no longer move ships.
        - your turn - Received when the given role's turn starts.
        - hit - role is the owner of the ship that has been hit. ship is the name of the ship that has been hit, and row and column provide the location on the board where it was hit. sunk provides a true/false value for if the ship was sunk.
        - miss - role is the owner of the board receiving the shot and row and column correspond to the board location or the shot.
        '''

        self.covid19 = COVID19(self)
        '''
        The COVID-19 Service provides access to the 2019-nCoV dataset compiled by Johns Hopkins University.
        This dataset includes deaths, confirmed cases, and recoveries related to the COVID-19 pandemic.
        Vaccination data is provided by Our World in Data.
        
        For more information, check out https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases
        and https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations.
        '''

        self.chart = Chart(self)
        '''
        A charting service powered by gnuplot.
        '''

        self.cloud_variables = CloudVariables(self)
        '''
        The CloudVariables Service provides support for storing variables on the cloud.
        Variables can be optionally password-protected or stored only for the current user.
        
        Cloud variables that are inactive (no reads or writes) for 30 days are subject to deletion.
        '''

        self.connect_n = ConnectN(self)
        '''
        The ConnectN Service provides helpers for building games like Connect-4 and Tic-Tac-Toe.
        '''

        self.core_nlp = CoreNLP(self)
        '''
        Use CoreNLP to annotate text.
        For more information, check out https://stanfordnlp.github.io/CoreNLP/.
        '''

        self.dev = Dev(self)
        

        self.earth_orbit = EarthOrbit(self)
        '''
        Access to Astronomical Solutions for Earth Paleoclimates. There are three researches (in 1993, 2004, and 2010) about 
        earth orbital parameters' data. This service only uses the 2004 data. 
        
        For more information, check out
        http://vo.imcce.fr/insola/earth/online/earth/earth.html.
        
        Original datasets are available at:
        
        - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLN.LA2004.BTL.100.ASC
        - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLN.LA2004.BTL.250.ASC
        - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLN.LA2004.BTL.ASC
        - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLP.LA2004.BTL.ASC
        - http://vo.imcce.fr/webservices/miriade/proxy.php?file=http://145.238.217.35//tmp/insola/insolaouto7Yk3u&format=text
        - http://vo.imcce.fr/webservices/miriade/proxy.php?file=http://145.238.217.38//tmp/insola/insolaouteXT96X&format=text
        '''

        self.earthquakes = Earthquakes(self)
        '''
        The Earthquakes Service provides access to historical earthquake data.
        For more information, check out https://earthquake.usgs.gov/.
        '''

        self.eclipse2017 = Eclipse2017(self)
        '''
        The Eclipse2017 Service provides access to US weather data along the path of the Great American Eclipse.
        For more information about the eclipse, check out https://www.greatamericaneclipse.com/.
        '''

        self.execute = Execute(self)
        '''
        The Execute Service provides capabilities for executing blocks on the NetsBlox
        server. This is particularly useful for batching RPC requests.
        '''

        self.geolocation = Geolocation(self)
        '''
        The Geolocation Service provides access to the Google Places API and geocoding capabilities.
        For more information, check out https://developers.google.com/places/
        
        Terms of service: https://developers.google.com/maps/terms
        '''

        self.google_maps = GoogleMaps(self)
        '''
        The GoogleMaps Service provides access to the Google Maps API along with helper functions for interacting with the maps (such as converting coordinates).
        For more information, check out https://developers.google.com/maps/documentation/static-maps/intro
        
        Terms of use: https://developers.google.com/maps/terms
        '''

        self.google_street_view = GoogleStreetView(self)
        '''
        The GoogleStreetView Service provides access to the Google Street View Image API
        For more information, check out https://developers.google.com/maps/documentation/streetview/intro
        
        Terms of use: https://developers.google.com/maps/terms
        '''

        self.hangman = Hangman(self)
        '''
        The Hangman Service provides helpers for mediating a distributed game of hangman.
        '''

        self.historical_temperature = HistoricalTemperature(self)
        '''
        Access to Berkeley Earth data.
        See http://berkeleyearth.org/data/ for additional details.
        
        These RPCs take a region argument, which can either be a country
        or one of the following special values:
        
        - all land - get data for all landmasses around the world
        - global - get data for the entire Earth (including oceans)
        - northern hemisphere - only northern landmasses
        - southern hemisphere - only southern landmasses
        '''

        self.human_mortality_database = HumanMortalityDatabase(self)
        '''
        This service accesses data from the human mortality database which tabulates
        death rates broken down by age group and gender for various countries.
        
        For more information, see https://www.mortality.org/.
        
        Note: for countries that don't report separate male and female death counts,
        the gender breakdowns are just the total multiplied by a rough estimate
        of the percent of people in that country who are male/female.
        '''

        self.hurricane_data = HurricaneData(self)
        '''
        The HurricaneData service provides access to the revised Atlantic hurricane
        database (HURDAT2) from the National Hurricane Center (NHC).
        
        For more information, check out https://www.aoml.noaa.gov/hrd/data_sub/re_anal.html
        '''

        self.ice_core_data = IceCoreData(self)
        '''
        Access to NOAA Paleoclimatology ice core data.
        
        For more information, check out
        https://www.ncdc.noaa.gov/data-access/paleoclimatology-data/datasets/ice-core.
        
        Original datasets are available at:
        
        - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/antarctica2015co2composite.txt
        - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/antarctica2015co2law.txt
        - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/antarctica2015co2wais.txt
        - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/vostok/co2nat.txt
        - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/vostok/deutnat.txt
        - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/epica_domec/edc3deuttemp2007.txt
        - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/greenland/summit/grip/isotopes/gripd18o.txt
        - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/vostok/gt4nat.txt
        - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/law/law2012d18o.txt
        - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/wdc05a2013d18o.txt
        '''

        self.io_tscape = IoTScape(self)
        '''
        The IoTScape Service enables remote devices to provide custom services. Custom
        Services can be found under the "Community/Devices" section using the call <RPC>
        block.
        '''

        self.key_value_store = KeyValueStore(self)
        '''
        The KeyValueStore Service provides basic storage functionality using a hierarchical
        key-value storage (similar to CloudVariables).
        '''

        self.mauna_loa_co2_data = MaunaLoaCO2Data(self)
        '''
        Access to NOAA Earth System Research Laboratory data collected from Mauna Loa, Hawaii.
        
        See https://www.esrl.noaa.gov/gmd/ccgg/trends/ for additional details.
        '''

        self.met_museum = MetMuseum(self)
        '''
        Access the Metropolitan Museum of Art's collection.
        For explanation on the different attributes for each object,
        visit https://metmuseum.github.io.
        '''

        self.movie_db = MovieDB(self)
        '''
        The MovieDB Service provides access to movie data using TMDB (The MovieDB API).
        For more information, check out https://www.themoviedb.org/
        
        Terms of use: https://www.themoviedb.org/documentation/api/terms-of-use
        '''

        self.nasa = NASA(self)
        '''
        The NASA Service provides access to planetary pictures and mars weather data.
        For more information, check out https://api.nasa.gov/.
        '''

        self.nplayer = NPlayer(self)
        '''
        The NPlayer Service provides helpers RPCs for ensuring round-robin turn taking
        among the roles in the project's room.
        
        Each role will receive a "start game" message at the start and then "start turn"
        message when it is the given role's turn to act.
        '''

        self.new_york_public_library = NewYorkPublicLibrary(self)
        '''
        The New York Public Library (NYPL) Service provides access to NYPL's online repository of historical items.
        '''

        self.new_york_times = NewYorkTimes(self)
        '''
        The NewYorkTimes service provides access to the New York Times API including access
        to Moview Reviews, Top Stories, and their Semantic API.
        '''

        self.ocean_data = OceanData(self)
        '''
        The OceanData service provides access to scientific ocean data including
        temperature and sea level.
        
        For more information, check out:
        
        - http://www.columbia.edu/~mhs119/Sensitivity+SL+CO2/
        - https://www.paleo.bristol.ac.uk/~ggdjl/warm_climates/hansen_etal.pdf.
        '''

        self.paleocean_oxygen_isotopes = PaleoceanOxygenIsotopes(self)
        '''
        Access to NOAA Global Pliocene-Pleistocene Benthic d18O Stack.
        
        For more information, check out
        https://www.ncdc.noaa.gov/paleo-search/study/5847
        
        Original datasets are available at:
        https://www1.ncdc.noaa.gov/pub/data/paleo/contributions_by_author/lisiecki2005/lisiecki2005.txt.
        '''

        self.parallel_dots = ParallelDots(self)
        '''
        Uses ParallelDots AI to process or compare text for a variety of features.
        See the API documentation, at 
        http://apis.paralleldots.com/text_docs/index.html
        
        Terms of use: https://www.paralleldots.com/terms-and-conditions
        '''

        self.phone_iot = PhoneIoT(self)
        '''
        PhoneIoT is a service in NetsBlox <https://netsblox.org/>_ that's meant to teach Internet of Things (IoT) topics as early as K-12 education.
        It allows you to programmatically access your smartphone's sensors and display.
        This includes accessing hardware sensors such as the accelerometer, gyroscope, microphone, camera, and many others depending on the device.
        PhoneIoT also allows you to control a customizable interactive display, enabling you to use your device as a custom remote control, or even create and run distributed (multiplayer) applications.
        The limits are up to your imagination!
        
        To get started using PhoneIoT, download the PhoneIoT app on your mobile device, available for Android <https://play.google.com/store/apps/details?id=org.netsblox.phoneiot>_ and iOS, and then go to the NetsBlox editor <https://editor.NetsBlox.org>_.
        In the top left of the editor, you should see a grid of several colored tabs.
        Under the Network tab, grab a call block and place it in the center script area.
        Click the first dropdown on the call block and select the PhoneIoT service.
        The second dropdown selects the specific *Remote Procedure Call* (RPC) to execute - see the table of contents  for information about the various RPCs.
        
        Inside the PhoneIoT app on your mobile device, click the button at the top left to open the menu, and then click connect.
        If you successfully connected, you should get a small popup message at the bottom of the screen.
        If you don't see this message, make sure you have either Wi-Fi or mobile data turned on and try again.
        Near the top of the menu, you should see an ID and password, which will be needed to connect to the device from NetsBlox.
        
        Back in NetsBlox, select the setCredentials RPC and give it your ID and password.
        For convenience, you might want to save the ID in a variable (e.g. device), as it will be referenced many times.
        If you click the call block to run it, you should get an OK result, meaning you successfully connected.
        If you don't see this, make sure you entered the ID and password correctly.
        
        You're now ready to start using the other RPCs in PhoneIoT to communicate with the device!
        '''

        self.project_gutenberg = ProjectGutenberg(self)
        '''
        The Project Gutenberg service provides access to public domain books. For more information, check out https://project-gutenberg.org/.
        '''

        self.public_roles = PublicRoles(self)
        '''
        The PublicRoles Service provides access to the user's public role
        ID programmatically. This enables communication between projects.
        '''

        self.robo_scape = RoboScape(self)
        

        self.service_creation = ServiceCreation(self)
        '''
        The ServiceCreation Service enables users to create custom services. Custom
        Services can be found under the "Community" section using the call <RPC>
        block.
        '''

        self.simple_hangman = SimpleHangman(self)
        '''
        The SimpleHangman Service provides RPCs for playing single player hangman.
        The service will choose a word for the player to guess using the given RPCs.
        '''

        self.smithsonian = Smithsonian(self)
        '''
        The Smithsonian Service provides access to the Smithsonan open-access EDAN database,
        containing catalogued information on millions of historical items.
        '''

        self.star_map = StarMap(self)
        '''
        The StarMap Service provides access to astronomy data using Sloan Digital Sky Survey.
        For more information, check out http://skyserver.sdss.org/dr14/en/home.aspx
        '''

        self.thingspeak = Thingspeak(self)
        '''
        The ThingSpeak Service provides access to the ThingSpeak IoT analytics platform.
        For more information, check out https://thingspeak.com/.
        
        Terms of use: https://thingspeak.com/pages/terms
        '''

        self.this_x_does_not_exist = ThisXDoesNotExist(self)
        '''
        This service uses Artificial Intelligence (AI) to make random, realistic images.
        For a list of example websites, see https://thisxdoesnotexist.com/.
        These are typically made by a Generative Adversarial neural Network (GAN).
        Put simply, this involves two AIs: one to make images and another to guess if they're real or fake, and making them compete to mutually improve.
        For more information, see https://en.wikipedia.org/wiki/Generative_adversarial_network.
        '''

        self.traffic = Traffic(self)
        '''
        The Traffic Service provides access to real-time traffic data using the Bing Traffic API.
        For more information, check out https://msdn.microsoft.com/en-us/library/hh441725.aspx
        '''

        self.translation = Translation(self)
        '''
        Uses Microsoft's Azure Cognitive Services API to translate text.
        For more information, check out https://azure.microsoft.com/en-us/pricing/details/cognitive-services/translator-text-api/.
        
        Terms of use: https://www.microsoft.com/en-us/servicesagreement
        '''

        self.trivia = Trivia(self)
        '''
        The Trivia Service provides access to trivia questions using the jservice API.
        For more information, check out https://jservice.io.
        '''

        self.twenty_questions = TwentyQuestions(self)
        '''
        The TwentyQuestions Service aids in the creation of a multiplayer
        game of twenty questions.
        '''

        self.twitter = Twitter(self)
        '''
        The Twitter Service provides access to posts and profile information from Twitter.
        For more information, check out https://twitter.com.
        
        Terms of use: https://twitter.com/en/tos
        '''

        self.water_watch = WaterWatch(self)
        '''
        The WaterWatch Service provides access to real-time water data.
        For more information, check out https://waterservices.usgs.gov/
        '''

        self.weather = Weather(self)
        '''
        The Weather Service provides access to real-time weather data using OpenWeatherMap.
        For more information, check out https://openweathermap.org/.
        
        Terms of Service: https://openweathermap.org/terms
        '''


    def _ws_open(self, ws):
        with self._ws_lock:
            ws.send(_common.small_json({ 'type': 'set-uuid', 'clientId': self._client_id }))

    def _ws_close(self, ws, status, message):
        print('ws close', file = _sys.stderr)
    def _ws_error(self, ws, error):
        print('ws error:', error, file = _sys.stderr)

    def _ws_message(self, ws, message):
        try:
            message = _json.loads(message)
            ty = message['type']

            if ty == 'connected': # currently unused
                return
            elif ty == 'ping':
                with self._ws_lock:
                    ws.send(_common.small_json({ 'type': 'pong' }))
                    return
            elif ty == 'message':
                with self._message_cv:
                    self._message_queue.append(message)
                    self._message_cv.notify()
        except:
            pass
    
    def get_public_role_id(self):
        '''
        Returns the public role id, which can be used as a target for send_message() to send a message directly to yourself.
        This can be given to another client so that they can send messages directly to you.
        '''
        return f'{self._role_name}@{self._project_name}@{self._client_id}'
    def send_message(self, msg_type, target='everyone in room', **values):
        '''
        Sends a message of the given type to the target, which might represent multiple recipients.
        The default value for target, 'everyone in room', will send the message to everyone connected to this project (including yourself).
        You can receive messages by registering a receiver with on_message().
        '''
        with self._ws_lock:
            self._ws.send(_common.small_json({
                'type': 'message',
                'msgType': msg_type,
                'content': values,
                'dstId': target,
                'srcId': self.get_public_role_id()
            }))

    @staticmethod
    def _check_handler(handler, content):
        argspec = _inspect.getfullargspec(handler.wrapped())
        unused_params = set(content.keys())
        for arg in argspec.args + argspec.kwonlyargs:
            if arg not in content and arg != 'self':
                return f'    unknown param: \'{arg}\' typo?\n    available params: {list(content.keys())}'
            unused_params.discard(arg)
        return { k: content[k] for k in content.keys() if k not in unused_params } if unused_params and argspec.varkw is None else content
    def _message_get_last_assume_locked(self, msg_type):
        if msg_type not in self._message_last:
            self._message_last[msg_type] = { 'received_count': 0, 'last_content': {}, 'waiters': 0 }
        return self._message_last[msg_type]
    def _message_router(self):
        while True:
            try:
                message = None
                handlers = None
                with self._message_cv:
                    # if no more messages and stream has stopped, kill the thread
                    if not self._message_queue and self._message_stream_stopped:
                        return
                    # wait for a message or kill signal
                    while not self._message_queue and not self._message_stream_stopped:
                        self._message_cv.wait()
                    # if we didn't get a message, kill the thread
                    if not self._message_queue:
                        return

                    message = self._message_queue.popleft()
                    handlers = self._message_handlers.get(message['msgType'])
                    handlers = handlers[:] if handlers is not None else [] # iteration without mutex needs a (shallow) copy

                    last = self._message_get_last_assume_locked(message['msgType'])
                    last['received_count'] += 1
                    last['last_content'] = message['content']
                    if last['waiters'] > 0:
                        last['waiters'] = 0
                        self._message_cv.notify_all()
                
                content = message['content']
                for handler in handlers: # without mutex lock so we don't block new ws messages or on_message()
                    try:
                        packet = Client._check_handler(handler, content)
                        if type(packet) == str:
                            print(f'\'{message["msgType"]}\' message handler error:\n{packet}', file = _sys.stderr)
                            continue

                        handler.schedule(**packet)
                    except:
                        _traceback.print_exc(file = _sys.stderr)
            except:
                _traceback.print_exc(file = _sys.stderr)
    
    def wait_for_message(self, msg_type: str) -> dict:
        '''
        Waits until we receive the next message of the given type.
        Returns the received message upon resuming.

        You can trigger this manually by sending a message to yourself.
        '''
        with self._message_cv:
            last = self._message_get_last_assume_locked(msg_type)
            last['waiters'] += 1
            v = last['received_count']
            while last['received_count'] <= v:
                self._message_cv.wait()
            return last['last_content']

    def _on_message(self, msg_type: str, handler):
        with self._message_cv:
            handlers = self._message_handlers.get(msg_type)
            if handlers is None:
                handlers = []
                self._message_handlers[msg_type] = handlers
            handlers.append(_events.get_event_wrapper(handler))
    def on_message(self, *msg_types: str):
        '''
        This is a decorator that can be applied to a turtle/stage method or a function
        to cause the function to be executed when a message of the given type is received from NetsBlox.
        You can receive message fields by specifying input parameters.

        ```
        @nb.on_message('start')
        def on_start():
            print('started')

        @nb.on_message('left', 'right')
        def on_left_or_right(self, distance):
            print('moved', distance, 'cm')
        ```
        '''
        def wrapper(f):
            if _common.is_method(f):
                if not hasattr(f, '__run_on_message'):
                    setattr(f, '__run_on_message', [])
                # mark it for the constructor to handle when an instance is created
                def stupid_closure_semantics(_msg_type):
                    return lambda x: self._on_message(_msg_type, x)
                getattr(f, '__run_on_message').extend([stupid_closure_semantics(msg_type) for msg_type in msg_types])
            else:
                for msg_type in msg_types:
                    self._on_message(msg_type, f)

            return f
        return wrapper

    def _call(self, service, rpc, payload):
        payload = { k: _common.prep_send(v) for k,v in payload.items() }
        state = f'uuid={self._client_id}&projectId={self._project_id}&roleId={self._role_id}&t={round(_time.time() * 1000)}'
        url = f'{self._base_url}/services/{service}/{rpc}?{state}'
        res = _requests.post(url,
            _common.small_json(payload), # if the json has unnecessary white space, request on the server will hang for some reason
            headers = { 'Content-Type': 'application/json' })

        if res.status_code == 200:
            try:
                if 'Content-Type' in res.headers:
                    ty = res.headers['Content-Type']
                    if ty.startswith('image/'):
                        return Image.open(_io.BytesIO(res.content))
                return _json.loads(res.text)
            except:
                return res.text # strings are returned unquoted, so they'll fail to parse as json
        elif res.status_code == 404:
            raise _common.NotFoundError(res.text)
        elif res.status_code == 500:
            raise _common.ServerError(res.text)
        else:
            raise Exception(f'Unknown error: {res.status_code}\n{res.text}')

    def disconnect(self):
        '''
        Disconnects the client from the NetsBlox server.
        If the client was created with run_forever, this will allow the program to terminate.
        '''
        with self._ws_lock:
            self._ws.close() # closing the websocket will kill the ws thread
        with self._message_cv:
            self._message_stream_stopped = True # send the kill signal
            self._message_cv.notify()
    def wait_till_disconnect(self):
        '''
        This function waits until the client is disconnected and all queued messages have been handled.
        Other (non-waiting) code can call disconnect() to trigger this manually.
        This is useful if you have long-running code using messaging, e.g., a server.

        If you want similar behavior without having to actually disconnect the client, you can use a Signal instead.

        Note that calling this function is not equivalent to setting the run_forever option when creating the client, as that does not block the main thread.
        This can be used in place of run_forever, and is needed if other code waits for the main thread to finish (e.g., Google Colab).

        Note: you should not call this from a message handler (or any function that a message handler calls),
        as that will suspend the thread that handles messages, and since this waits until all messages have been handled, it will end up waiting forever.
        '''
        self._message_thread.join()

class AirQuality:
    '''
    The AirQuality Service provides access to real-time air quality data using the AirNowAPI.
    For more information, check out https://docs.airnowapi.org/.
    '''
    def __init__(self, client):
        self._client = client
    def quality_index(self, latitude: float, longitude: float) -> float:
        '''
        Get air quality index of closest reporting location for coordinates
        
        :latitude: latitude of location
        
        :longitude: Longitude of location
        
        :returns: AQI of closest station
        '''
        res = self._client._call('AirQuality', 'qualityIndex', { 'latitude': latitude, 'longitude': longitude })
        return float(res)
    def quality_index_by_zip_code(self, zip_code: int) -> float:
        '''
        Get air quality index of closest reporting location for ZIP code
        
        :zip_code: ZIP code of location
        
        :returns: AQI of closest station
        '''
        res = self._client._call('AirQuality', 'qualityIndexByZipCode', { 'zipCode': zip_code })
        return float(res)
class Alexa:
    '''
    The Alexa service provides capabilities for building your own Alexa skills!
    
    An Alexa skill consists of some general information (such as the name to use
    for invocation) as well as a list of supported intents. An intent is a command
    or question to which the skill can respond. Intents consist of a name, list of
    utterances, and any required slots. Utterances are examples of how the user might
    phrase questions or commands. Slots are used to define placeholders for concepts
    like names, cities, etc.
    
    When Alexa determines that a request was made to a given intent, the slots are
    resolved to their corresponding values and then passed to the "handler" for the
    intent.
    '''
    def __init__(self, client):
        self._client = client
    def create_skill(self, configuration: dict) -> str:
        '''
        Create an Alexa Skill from a configuration.
        
        :configuration: 
          - :name: (str) The name of the skill
          - :invocation: (str) The name to use to invoke the skill (eg, "tell <invocation> to <intent>")
          - :intents: (List[dict]) Intents (ie, commands) supported by the skill.
          - :description: (str) 
          - :category: (str) 
          - :keywords: (List[str]) 
          - :summary: (str) 
          - :examples: (List[str]) 
        
        :returns: ID
        '''
        res = self._client._call('Alexa', 'createSkill', { 'configuration': configuration })
        return str(res)
    def delete_skill(self, id: str):
        '''
        Delete the given Alexa Skill (created within NetsBlox).
        
        :id: ID of the Alexa skill to delete
        '''
        return self._client._call('Alexa', 'deleteSkill', { 'ID': id })
    def get_skill(self, id: str):
        '''
        Get the configuration of the given Alexa Skill.
        
        :id: 
        '''
        return self._client._call('Alexa', 'getSkill', { 'ID': id })
    def get_skill_categories(self):
        '''
        Get a list of all valid categories for Alexa skills.
        '''
        return self._client._call('Alexa', 'getSkillCategories', {  })
    def get_slot_types(self):
        '''
        Get a list of all valid slot types that can be added to an intent.
        For more information, check out https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html
        '''
        return self._client._call('Alexa', 'getSlotTypes', {  })
    def invoke_skill(self, id: str, utterance: str) -> str:
        '''
        Invoke the skill with the given utterance using the closest intent.
        
        :id: Alexa Skill ID to send utterance to
        
        :utterance: Text to send to skill
        
        :returns: ID
        '''
        res = self._client._call('Alexa', 'invokeSkill', { 'ID': id, 'utterance': utterance })
        return str(res)
    def list_skills(self) -> List[str]:
        '''
        List the IDs of all the Alexa Skills created in NetsBlox for the given user.
        
        :returns: IDs
        '''
        res = self._client._call('Alexa', 'listSkills', {  })
        return _common.vectorize(str)(res)
    def update_skill(self, id: str, configuration: dict):
        '''
        Update skill configuration with the given ID.
        
        :id: ID of the skill to update
        
        :configuration: 
          - :name: (str) The name of the skill
          - :invocation: (str) The name to use to invoke the skill (eg, "tell <invocation> to <intent>")
          - :intents: (List[dict]) Intents (ie, commands) supported by the skill.
          - :description: (str) 
          - :category: (str) 
          - :keywords: (List[str]) 
          - :summary: (str) 
          - :examples: (List[str]) 
        '''
        return self._client._call('Alexa', 'updateSkill', { 'ID': id, 'configuration': configuration })
class Autograders:
    '''
    The Autograders service enables users to create custom autograders for
    use within NetsBlox.
    
    For more information, check out https://editor.netsblox.org/docs/services/Autograders/index.html
    '''
    def __init__(self, client):
        self._client = client
    def create_autograder(self, configuration: dict):
        '''
        Create an autograder using the supplied configuration.
        
        :configuration: 
        '''
        return self._client._call('Autograders', 'createAutograder', { 'configuration': configuration })
    def get_autograder_config(self, name: str):
        '''
        Fetch the autograder configuration.
        
        :name: 
        '''
        return self._client._call('Autograders', 'getAutograderConfig', { 'name': name })
    def get_autograders(self):
        '''
        List the autograders for the given user.
        '''
        return self._client._call('Autograders', 'getAutograders', {  })
class BaseX:
    '''
    The BaseX Service provides access to an existing BaseX instance.
    '''
    def __init__(self, client):
        self._client = client
    def command(self, url: str, command: str, username: Optional[str] = None, password: Optional[str] = None):
        '''
        Execute a single database command.
        
        A list of commands can be found at http://docs.basex.org/wiki/Commands
        
        :url: 
        
        :command: 
        
        :username: 
        
        :password: 
        '''
        return self._client._call('BaseX', 'command', { 'url': url, 'command': command, 'username': username, 'password': password })
    def query(self, url: str, database: str, query: str, username: Optional[str] = None, password: Optional[str] = None):
        '''
        Evaluate an XQuery expression.
        
        :url: 
        
        :database: 
        
        :query: 
        
        :username: 
        
        :password: 
        '''
        return self._client._call('BaseX', 'query', { 'url': url, 'database': database, 'query': query, 'username': username, 'password': password })
class Battleship:
    '''
    The Battleship Service provides helpful utilities for building a distributed
    game of battleship.
    
    Overview
    --------
    
    Like regular Battleship, the Battleship service has two states: placing ships and shooting at ships.
    During placement, it expects each role to place each ship on his/her board and will not allow the game to proceed to the shooting phase until each role has placed all his/her ships.
    Placement, firing and starting blocks will return true if successful or an error message if it fails.
    
    Blocks
    ------
    
    - place <ship> at <row> <column> facing <direction> - Places a ship on your board with the front at the given row and column facing the given direction. Returns true if placed successfully (eg, on the board and not overlapping another ship). Also, placing a ship twice results in a move (not duplicates).
    - start game - Try to start the game. If both users have all their ships placed, it should return true and send start messages to all roles. Otherwise, it will return with a message saying that it is waiting on a specific role.
    - fire at <row> <column> - This block allows the user to try to fire at the given row and column. It returns true if it was a valid move; otherwise it will return an error message like it's not your turn!. On a successful move, the server will send either a hit or miss message to everyone in the room. Then it will send a your turn message to the player to play next.
    - active ships for <role> - This block returns a list of all ships that are still afloat for the given role. If no role is specified, it defaults to the sender's role.
    - all ships - Returns a list of all ship names. Useful in programmatically placing ships.
    - ship length <ship> - Returns the length of the given ship.
    - restart game - Restarts the given game (all boards, etc)
    
    Message Types
    -------------
    
    - start - Received when start game finishes successfully for any role. After game has officially started, users can no longer move ships.
    - your turn - Received when the given role's turn starts.
    - hit - role is the owner of the ship that has been hit. ship is the name of the ship that has been hit, and row and column provide the location on the board where it was hit. sunk provides a true/false value for if the ship was sunk.
    - miss - role is the owner of the board receiving the shot and row and column correspond to the board location or the shot.
    '''
    def __init__(self, client):
        self._client = client
    def all_ships(self) -> List[str]:
        '''
        Get list of ship types
        
        :returns: Types of ships
        '''
        res = self._client._call('Battleship', 'allShips', {  })
        return _common.vectorize(str)(res)
    def fire(self, row: float, column: float) -> bool:
        '''
        Fire a shot at the board
        
        :row: Row to fire at
        
        :column: Column to fire at
        
        :returns: If ship was hit
        '''
        res = self._client._call('Battleship', 'fire', { 'row': row, 'column': column })
        return bool(res)
    def place_ship(self, ship: str, row: float, column: float, facing: str) -> bool:
        '''
        Place a ship on the board
        
        :ship: Ship type to place
        
        :row: Row to place ship in
        
        :column: Column to place ship in
        
        :facing: Direction to face
        
        :returns: If piece was placed
        '''
        res = self._client._call('Battleship', 'placeShip', { 'ship': ship, 'row': row, 'column': column, 'facing': facing })
        return bool(res)
    def remaining_ships(self, role_id: str) -> int:
        '''
        Get number of remaining ships of a role
        
        :role_id: Name of role to use
        
        :returns: Number of remaining ships
        '''
        res = self._client._call('Battleship', 'remainingShips', { 'roleID': role_id })
        return int(res)
    def reset(self) -> bool:
        '''
        Resets the game by clearing the board and reverting to the placing phase
        
        :returns: If game was reset
        '''
        res = self._client._call('Battleship', 'reset', {  })
        return bool(res)
    def ship_length(self, ship: str) -> int:
        '''
        Get length of a ship type
        
        :ship: Type of ship
        
        :returns: Length of ship type
        '''
        res = self._client._call('Battleship', 'shipLength', { 'ship': ship })
        return int(res)
    def start(self) -> bool:
        '''
        Begins the game, if board is ready
        
        :returns: If game was started
        '''
        res = self._client._call('Battleship', 'start', {  })
        return bool(res)
class COVID19:
    '''
    The COVID-19 Service provides access to the 2019-nCoV dataset compiled by Johns Hopkins University.
    This dataset includes deaths, confirmed cases, and recoveries related to the COVID-19 pandemic.
    Vaccination data is provided by Our World in Data.
    
    For more information, check out https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases
    and https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations.
    '''
    def __init__(self, client):
        self._client = client
    def get_confirmed_counts(self, country: str, state: Optional[str] = None, city: Optional[str] = None):
        '''
        Get number of confirmed cases of COVID-19 by date for a specific country and state.
        
        Date is in month/day/year format.
        
        :country: Country or region
        
        :state: State or province
        
        :city: City
        '''
        return self._client._call('COVID-19', 'getConfirmedCounts', { 'country': country, 'state': state, 'city': city })
    def get_death_counts(self, country: str, state: Optional[str] = None, city: Optional[str] = None):
        '''
        Get number of cases of COVID-19 resulting in death by date for a specific country and state.
        
        Date is in month/day/year format.
        
        :country: Country or region
        
        :state: State or province
        
        :city: City
        '''
        return self._client._call('COVID-19', 'getDeathCounts', { 'country': country, 'state': state, 'city': city })
    def get_location_coordinates(self, country: str, state: Optional[str] = None, city: Optional[str] = None):
        '''
        Get the latitude and longitude for a location with data available.
        
        :country: 
        
        :state: 
        
        :city: City
        '''
        return self._client._call('COVID-19', 'getLocationCoordinates', { 'country': country, 'state': state, 'city': city })
    def get_locations_with_data(self) -> list:
        '''
        Get a list of all countries (and states, cities) with data available.
        
        :returns: an array of [country, state, city] for each location with data available
        '''
        return self._client._call('COVID-19', 'getLocationsWithData', {  })
    def get_recovered_counts(self, country: str, state: Optional[str] = None, city: Optional[str] = None):
        '''
        Get number of cases of COVID-19 in which the person recovered by date for a specific country and state.
        
        Date is in month/day/year format.
        
        :country: Country or region
        
        :state: State or province
        
        :city: City
        '''
        return self._client._call('COVID-19', 'getRecoveredCounts', { 'country': country, 'state': state, 'city': city })
    def get_vaccination_categories(self) -> List[str]:
        '''
        Get the list of options that can be entered in the getVaccinationData RPC
        
        :returns: 
        '''
        res = self._client._call('COVID-19', 'getVaccinationCategories', {  })
        return _common.vectorize(str)(res)
    def get_vaccination_countries(self) -> List[str]:
        '''
        The list of countries that can be entered in the getVaccinationData RPC
        
        :returns: 
        '''
        res = self._client._call('COVID-19', 'getVaccinationCountries', {  })
        return _common.vectorize(str)(res)
    def get_vaccination_data(self, country: str, state: Optional[str] = None, category: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> list:
        '''
        Get all available vaccination data for a given country or state (if country is United States).
        Optionally, you can specify category to filter to only data for the given category.
        You can further filter your data by specifying startDate and endDate.
        
        :country: name of the country for which to get data
        
        :state: name of the state to get data for (if the country is United States)
        
        :category: the category of data to pull (see getVaccinationCategories), or nothing to get all data
        
        :start_date: earliest date to include in result (mm/dd/yyyy)
        
        :end_date: latest date to include in result (mm/dd/yyyy)
        
        :returns: the requested data
        '''
        return self._client._call('COVID-19', 'getVaccinationData', { 'country': country, 'state': state, 'category': category, 'startDate': start_date, 'endDate': end_date })
    def get_vaccination_states(self) -> List[str]:
        '''
        Get the list of US states that can be entered in the getVaccinationData RPC
        
        :returns: 
        '''
        res = self._client._call('COVID-19', 'getVaccinationStates', {  })
        return _common.vectorize(str)(res)
class Chart:
    '''
    A charting service powered by gnuplot.
    '''
    def __init__(self, client):
        self._client = client
    def default_options(self) -> dict:
        '''
        Get the default options for the Chart.draw RPC.
        
        :returns: the default draw options
        '''
        res = self._client._call('Chart', 'defaultOptions', {  })
        return dict(res)
    def draw(self, lines: list, options: Optional[dict] = None) -> Any:
        '''
        Create charts and histograms from data.
        
        :lines: a single line or list of lines. Each line should be [[x1,y1], [x2,y2], ...].
        
        :options: Configuration for graph title, axes, and more
          - :title: (str) title to show on the graph
          - :width: (float) width of the returned image
          - :height: (float) height of the returned image
          - :labels: (List[str]) labels for each line
          - :types: (List[str]) types for each line
          - :xRange: (List[float]) range of X values to graph
          - :yRange: (List[float]) range of Y values to graph
          - :xLabel: (str) label on the X axis
          - :yLabel: (str) label on the Y axis
          - :xTicks: (float) tick interval for the X axis
          - :isCategorical: (bool) true to enable categorical mode
          - :smooth: (bool) true to enable smoothing
          - :grid: (str) grid type to use
          - :isTimeSeries: (bool) true to enable time series mode
          - :timeInputFormat: (str) input time format for time series data
          - :timeDisplayFormat: (str) output time format for time series data
          - :logscale: (list) logscale settings to use
        
        :returns: the generated chart
        '''
        return self._client._call('Chart', 'draw', { 'lines': lines, 'options': options })
class CloudVariables:
    '''
    The CloudVariables Service provides support for storing variables on the cloud.
    Variables can be optionally password-protected or stored only for the current user.
    
    Cloud variables that are inactive (no reads or writes) for 30 days are subject to deletion.
    '''
    def __init__(self, client):
        self._client = client
    def delete_user_variable(self, name: str):
        '''
        Delete the user variable for the current user.
        
        :name: Variable name
        '''
        return self._client._call('CloudVariables', 'deleteUserVariable', { 'name': name })
    def delete_variable(self, name: str, password: Optional[str] = None):
        '''
        Delete a given cloud variable
        
        :name: Variable to delete
        
        :password: Password (if password-protected)
        '''
        return self._client._call('CloudVariables', 'deleteVariable', { 'name': name, 'password': password })
    def get_user_variable(self, name: str) -> Any:
        '''
        Get the value of a variable for the current user.
        
        :name: Variable name
        
        :returns: the stored value
        '''
        return self._client._call('CloudVariables', 'getUserVariable', { 'name': name })
    def get_variable(self, name: str, password: Optional[str] = None) -> Any:
        '''
        Get the value of a cloud variable
        
        :name: Variable name
        
        :password: Password (if password-protected)
        
        :returns: the stored value
        '''
        return self._client._call('CloudVariables', 'getVariable', { 'name': name, 'password': password })
    def lock_variable(self, name: str, password: Optional[str] = None):
        '''
        Lock a given cloud variable.
        
        A locked variable cannot be changed by anyone other than the person
        who locked it. A variable cannot be locked for more than 5 seconds.
        
        :name: Variable to lock
        
        :password: Password (if password-protected)
        '''
        return self._client._call('CloudVariables', 'lockVariable', { 'name': name, 'password': password })
    def set_user_variable(self, name: str, value: Any):
        '''
        Set the value of the user cloud variable for the current user.
        
        :name: Variable name
        
        :value: Value to store in variable
        '''
        return self._client._call('CloudVariables', 'setUserVariable', { 'name': name, 'value': value })
    def set_variable(self, name: str, value: Any, password: Optional[str] = None):
        '''
        Set a cloud variable.
        If a password is provided on creation, the variable will be password-protected.
        
        :name: Variable name
        
        :value: Value to store in variable
        
        :password: Password (if password-protected)
        '''
        return self._client._call('CloudVariables', 'setVariable', { 'name': name, 'value': value, 'password': password })
    def unlock_variable(self, name: str, password: Optional[str] = None):
        '''
        Unlock a given cloud variable.
        
        A locked variable cannot be changed by anyone other than the person
        who locked it. A variable cannot be locked for more than 5 minutes.
        
        :name: Variable to delete
        
        :password: Password (if password-protected)
        '''
        return self._client._call('CloudVariables', 'unlockVariable', { 'name': name, 'password': password })
class ConnectN:
    '''
    The ConnectN Service provides helpers for building games like Connect-4 and Tic-Tac-Toe.
    '''
    def __init__(self, client):
        self._client = client
    def is_full_board(self) -> bool:
        '''
        Check if every position on the current board is occupied.
        
        :returns: true if the board is full, otherwise false
        '''
        res = self._client._call('ConnectN', 'isFullBoard', {  })
        return bool(res)
    def is_game_over(self) -> bool:
        '''
        Check if the current game is over.
        
        :returns: true if game over, otherwise false
        '''
        res = self._client._call('ConnectN', 'isGameOver', {  })
        return bool(res)
    def new_game(self, row: Optional[float] = None, column: Optional[float] = None, num_dots_to_connect: Optional[float] = None):
        '''
        Create a new ConnectN game
        
        :row: The number of rows on the game board
        
        :column: The number of columns on the game board
        
        :num_dots_to_connect: The number of connected tiles required to win
        '''
        return self._client._call('ConnectN', 'newGame', { 'row': row, 'column': column, 'numDotsToConnect': num_dots_to_connect })
    def play(self, row: int, column: int):
        '''
        Play at the given row, column to occupy the location.
        
        :row: The given row at which to move
        
        :column: The given column at which to move
        '''
        return self._client._call('ConnectN', 'play', { 'row': row, 'column': column })
class CoreNLP:
    '''
    Use CoreNLP to annotate text.
    For more information, check out https://stanfordnlp.github.io/CoreNLP/.
    '''
    def __init__(self, client):
        self._client = client
    def annotate(self, text: str, annotators: Optional[List[str]] = None) -> dict:
        '''
        Annotate text using the provided annotators.
        
        :text: the text to annotate
        
        :annotators: a list of the annotators to use
        
        :returns: structured data containing the annotation results
        '''
        res = self._client._call('CoreNLP', 'annotate', { 'text': text, 'annotators': annotators })
        return dict(res)
    def get_annotators(self) -> List[str]:
        '''
        Get a list of all the supported annotators.
        The complete list is available at https://stanfordnlp.github.io/CoreNLP/annotators.html.
        
        :returns: list of supported annotators
        '''
        res = self._client._call('CoreNLP', 'getAnnotators', {  })
        return _common.vectorize(str)(res)
class Dev:
    
    def __init__(self, client):
        self._client = client
    def caller_info(self):
        '''
        Return the caller info as detected by the server.
        '''
        return self._client._call('Dev', 'callerInfo', {  })
    def clear_logs(self):
        '''
        Fetch debug logs for debugging remotely.
        '''
        return self._client._call('Dev', 'clearLogs', {  })
    def detect_abort(self):
        '''
        Sleep for 3 seconds and detect if the RPC was aborted.
        '''
        return self._client._call('Dev', 'detectAbort', {  })
    def echo(self, argument: Any):
        '''
        A function responding with the provided argument.
        
        :argument: 
        '''
        return self._client._call('Dev', 'echo', { 'argument': argument })
    def echo_if_within(self, input: float):
        '''
        Echo if the input is within 10 and 20 (manual test for parameterized types)
        
        :input: 
        '''
        return self._client._call('Dev', 'echoIfWithin', { 'input': input })
    def echo_options_example(self, options: dict):
        '''
        Call an argument with a duck typed options object
        
        :options: 
          - :name: (str) 
          - :age: (float) 
          - :height: (float) 
        '''
        return self._client._call('Dev', 'echoOptionsExample', { 'options': options })
    def get_logs(self):
        '''
        Fetch debug logs for debugging remotely.
        '''
        return self._client._call('Dev', 'getLogs', {  })
    def image(self):
        '''
        A function returning an image.
        '''
        return self._client._call('Dev', 'image', {  })
    def sum(self, numbers: List[float]):
        '''
        Return the sum of the inputs
        
        :numbers: 
        '''
        return self._client._call('Dev', 'sum', { 'numbers': numbers })
    def throw(self, msg: str):
        '''
        A function throwing an error.
        
        :msg: Error message
        '''
        return self._client._call('Dev', 'throw', { 'msg': msg })
class EarthOrbit:
    '''
    Access to Astronomical Solutions for Earth Paleoclimates. There are three researches (in 1993, 2004, and 2010) about 
    earth orbital parameters' data. This service only uses the 2004 data. 
    
    For more information, check out
    http://vo.imcce.fr/insola/earth/online/earth/earth.html.
    
    Original datasets are available at:
    
    - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLN.LA2004.BTL.100.ASC
    - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLN.LA2004.BTL.250.ASC
    - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLN.LA2004.BTL.ASC
    - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLP.LA2004.BTL.ASC
    - http://vo.imcce.fr/webservices/miriade/proxy.php?file=http://145.238.217.35//tmp/insola/insolaouto7Yk3u&format=text
    - http://vo.imcce.fr/webservices/miriade/proxy.php?file=http://145.238.217.38//tmp/insola/insolaouteXT96X&format=text
    '''
    def __init__(self, client):
        self._client = client
    def get_eccentricity(self, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get eccentricity by year. For more information about eccentricity, please visit: 
        https://climate.nasa.gov/news/2948/milankovitch-orbital-cycles-and-their-role-in-earths-climate/
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :startyear: first year of data to include
        
        :endyear: last year of data to include
        
        :returns: list of historical eccentricity values for each year
        '''
        return self._client._call('EarthOrbit', 'getEccentricity', { 'startyear': startyear, 'endyear': endyear })
    def get_insolation(self, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get insolation by year. Insolation here is the amount of solar radiation received at 65 N in June on Earth.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :startyear: first year of data to include
        
        :endyear: last year of data to include
        
        :returns: list of historical insolation values for each year
        '''
        return self._client._call('EarthOrbit', 'getInsolation', { 'startyear': startyear, 'endyear': endyear })
    def get_longitude(self, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get longitude of perihelion from moving equinox by year. For more information about this, please visit:
        https://www.physics.ncsu.edu/classes/astron/orbits.html
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :startyear: first year of data to include
        
        :endyear: last year of data to include
        
        :returns: longitude - longitude of perihelion from moving equinox
        '''
        return self._client._call('EarthOrbit', 'getLongitude', { 'startyear': startyear, 'endyear': endyear })
    def get_obliquity(self, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get obliquity by year. For more information about obliquity, please visit:
        https://climate.nasa.gov/news/2948/milankovitch-orbital-cycles-and-their-role-in-earths-climate/
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :startyear: first year of data to include
        
        :endyear: last year of data to include
        
        :returns: list of historical obliquity values for each year
        '''
        return self._client._call('EarthOrbit', 'getObliquity', { 'startyear': startyear, 'endyear': endyear })
    def get_precession(self, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get precession by year. For more information about precession, please visit:
        https://climate.nasa.gov/news/2948/milankovitch-orbital-cycles-and-their-role-in-earths-climate/
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :startyear: first year of data to include
        
        :endyear: last year of data to include
        
        :returns: list of historical precession values for each year
        '''
        return self._client._call('EarthOrbit', 'getPrecession', { 'startyear': startyear, 'endyear': endyear })
class Earthquakes:
    '''
    The Earthquakes Service provides access to historical earthquake data.
    For more information, check out https://earthquake.usgs.gov/.
    '''
    def __init__(self, client):
        self._client = client
    def by_region(self, min_latitude: float, max_latitude: float, min_longitude: float, max_longitude: float, start_time: Optional[str] = None, end_time: Optional[str] = None, min_magnitude: Optional[float] = None, max_magnitude: Optional[float] = None):
        '''
        Send messages for earthquakes within a given region
        
        :min_latitude: Minimum latitude of region
        
        :max_latitude: Maximum latitude of region
        
        :min_longitude: Minimum longitude of region
        
        :max_longitude: Maximum longitude of region
        
        :start_time: Minimum time
        
        :end_time: Maximum time
        
        :min_magnitude: Minimum magnitude of earthquakes to report
        
        :max_magnitude: Maximum magnitude of earthquakes to report
        '''
        return self._client._call('Earthquakes', 'byRegion', { 'minLatitude': min_latitude, 'maxLatitude': max_latitude, 'minLongitude': min_longitude, 'maxLongitude': max_longitude, 'startTime': start_time, 'endTime': end_time, 'minMagnitude': min_magnitude, 'maxMagnitude': max_magnitude })
    def stop(self):
        '''
        Stop sending earthquake messages
        '''
        return self._client._call('Earthquakes', 'stop', {  })
class Eclipse2017:
    '''
    The Eclipse2017 Service provides access to US weather data along the path of the Great American Eclipse.
    For more information about the eclipse, check out https://www.greatamericaneclipse.com/.
    '''
    def __init__(self, client):
        self._client = client
    def available_stations(self, max_reading_median: float, max_distance_from_center: float, latitude: Optional[float] = None, longitude: Optional[float] = None, max_distance_from_point: Optional[float] = None):
        '''
        Get a list of reporting weather stations for the given arguments.
        
        :max_reading_median: 
        
        :max_distance_from_center: 
        
        :latitude: 
        
        :longitude: 
        
        :max_distance_from_point: 
        '''
        return self._client._call('Eclipse2017', 'availableStations', { 'maxReadingMedian': max_reading_median, 'maxDistanceFromCenter': max_distance_from_center, 'latitude': latitude, 'longitude': longitude, 'maxDistanceFromPoint': max_distance_from_point })
    def condition_history(self, station_id: str, limit: str):
        '''
        Get the reported conditions for a given weather station.
        
        :station_id: 
        
        :limit: Number of results to return (max is 3000)
        '''
        return self._client._call('Eclipse2017', 'conditionHistory', { 'stationId': station_id, 'limit': limit })
    def condition_history_range(self, station_id: str, start_time: str, end_time: str):
        '''
        Get the reported conditions during a given time for a given weather station.
        
        :station_id: 
        
        :start_time: 
        
        :end_time: 
        '''
        return self._client._call('Eclipse2017', 'conditionHistoryRange', { 'stationId': station_id, 'startTime': start_time, 'endTime': end_time })
    def eclipse_path(self):
        '''
        Get the path of the eclipse as a list of latitude, longitude, and time.
        '''
        return self._client._call('Eclipse2017', 'eclipsePath', {  })
    def past_condition(self, station_id: str, time: str):
        '''
        Get historical conditions at a given weather station.
        
        :station_id: 
        
        :time: 
        '''
        return self._client._call('Eclipse2017', 'pastCondition', { 'stationId': station_id, 'time': time })
    def past_temperature(self, station_id: str, time: str):
        '''
        Get historical temperature for a given weather station.
        
        :station_id: 
        
        :time: 
        '''
        return self._client._call('Eclipse2017', 'pastTemperature', { 'stationId': station_id, 'time': time })
    def select_point_based(self):
        '''
        Get stations selected based on the points of the eclipse path.
        '''
        return self._client._call('Eclipse2017', 'selectPointBased', {  })
    def select_section_based(self, num_sections: int, per_section: int):
        '''
        Divide the eclipse path into a number of sections and select weather stations from each section.
        
        :num_sections: Number of sections to divide the path into
        
        :per_section: Number of stations to select
        '''
        return self._client._call('Eclipse2017', 'selectSectionBased', { 'numSections': num_sections, 'perSection': per_section })
    def station_info(self, station_id: str):
        '''
        Get information about a given reporting station.
        
        :station_id: Reporting station ID (pws)
        '''
        return self._client._call('Eclipse2017', 'stationInfo', { 'stationId': station_id })
    def stations(self):
        '''
        Get a list of reporting stations IDs (pws field).
        '''
        return self._client._call('Eclipse2017', 'stations', {  })
    def stations_info(self):
        '''
        Get information about all reporting weather stations.
        '''
        return self._client._call('Eclipse2017', 'stationsInfo', {  })
    def temperature_history(self, station_id: str, limit: str):
        '''
        Get the reported temperatures for a given weather station.
        
        :station_id: 
        
        :limit: Number of results to return (max is 3000)
        '''
        return self._client._call('Eclipse2017', 'temperatureHistory', { 'stationId': station_id, 'limit': limit })
    def temperature_history_range(self, station_id: str, start_time: str, end_time: str):
        '''
        Get the reported temperatures during a given time for a given weather station.
        
        :station_id: 
        
        :start_time: 
        
        :end_time: 
        '''
        return self._client._call('Eclipse2017', 'temperatureHistoryRange', { 'stationId': station_id, 'startTime': start_time, 'endTime': end_time })
class Execute:
    '''
    The Execute Service provides capabilities for executing blocks on the NetsBlox
    server. This is particularly useful for batching RPC requests.
    '''
    def __init__(self, client):
        self._client = client
    def call(self, fn: Any) -> Any:
        '''
        Execute a function on the NetsBlox server.
        
        :fn: function (ringified blocks) to execute
        
        :returns: return value of fn
        '''
        return self._client._call('Execute', 'call', { 'fn': fn })
class Geolocation:
    '''
    The Geolocation Service provides access to the Google Places API and geocoding capabilities.
    For more information, check out https://developers.google.com/places/
    
    Terms of service: https://developers.google.com/maps/terms
    '''
    def __init__(self, client):
        self._client = client
    def city(self, latitude: float, longitude: float) -> str:
        '''
        Get the name of the city nearest to the given latitude and longitude.
        
        :latitude: latitude of the target location
        
        :longitude: longitude of the target location
        
        :returns: city name
        '''
        res = self._client._call('Geolocation', 'city', { 'latitude': latitude, 'longitude': longitude })
        return str(res)
    def country(self, latitude: float, longitude: float) -> str:
        '''
        Get the name of the country nearest to the given latitude and longitude.
        
        :latitude: latitude of the target location
        
        :longitude: longitude of the target location
        
        :returns: country name
        '''
        res = self._client._call('Geolocation', 'country', { 'latitude': latitude, 'longitude': longitude })
        return str(res)
    def country_code(self, latitude: float, longitude: float) -> str:
        '''
        Get the code for the country nearest to the given latitude and longitude.
        
        :latitude: latitude of the target location
        
        :longitude: longitude of the target location
        
        :returns: country name
        '''
        res = self._client._call('Geolocation', 'countryCode', { 'latitude': latitude, 'longitude': longitude })
        return str(res)
    def county(self, latitude: float, longitude: float) -> str:
        '''
        Get the name of the county (or closest equivalent) nearest to the given latitude and longitude.
        If the country does not have counties, it will return the corresponding division for administrative level 2.
        
        For more information on administrative divisions, check out https://en.wikipedia.org/wiki/List_of_administrative_divisions_by_country
        
        :latitude: latitude of the target location
        
        :longitude: longitude of the target location
        
        :returns: county name
        '''
        res = self._client._call('Geolocation', 'county*', { 'latitude': latitude, 'longitude': longitude })
        return str(res)
    def geolocate(self, address: str) -> dict:
        '''
        Geolocates the address and returns the coordinates
        
        :address: target address
        
        :returns: structured data representing the location of the address
        '''
        res = self._client._call('Geolocation', 'geolocate', { 'address': address })
        return dict(res)
    def info(self, latitude: float, longitude: float):
        '''
        Get administrative division information for the given latitude and longitude.
        
        :latitude: latitude of the target location
        
        :longitude: longitude of the target location
        '''
        return self._client._call('Geolocation', 'info', { 'latitude': latitude, 'longitude': longitude })
    def nearby_search(self, latitude: float, longitude: float, keyword: Optional[str] = None, radius: Optional[float] = None):
        '''
        Find places near an earth coordinate (latitude, longitude) (maximum of 10 results)
        
        :latitude: 
        
        :longitude: 
        
        :keyword: the keyword you want to search for, like pizza or cinema.
        
        :radius: search radius in meters (50km)
        '''
        return self._client._call('Geolocation', 'nearbySearch', { 'latitude': latitude, 'longitude': longitude, 'keyword': keyword, 'radius': radius })
    def state(self, latitude: float, longitude: float) -> str:
        '''
        Get the name of the state (or closest equivalent) nearest to the given latitude and longitude.
        If the country does not have states, it will return the corresponding division for administrative level 1.
        
        For more information on administrative divisions, check out https://en.wikipedia.org/wiki/List_of_administrative_divisions_by_country
        
        :latitude: latitude of the target location
        
        :longitude: longitude of the target location
        
        :returns: state name
        '''
        res = self._client._call('Geolocation', 'state*', { 'latitude': latitude, 'longitude': longitude })
        return str(res)
    def state_code(self, latitude: float, longitude: float) -> str:
        '''
        Get the code for the state (or closest equivalent) nearest to the given latitude and longitude.
        If the country does not have states, it will return the corresponding division for administrative level 1.
        
        For more information on administrative divisions, check out https://en.wikipedia.org/wiki/List_of_administrative_divisions_by_country
        
        :latitude: latitude of the target location
        
        :longitude: longitude of the target location
        
        :returns: state name
        '''
        res = self._client._call('Geolocation', 'stateCode*', { 'latitude': latitude, 'longitude': longitude })
        return str(res)
class GoogleMaps:
    '''
    The GoogleMaps Service provides access to the Google Maps API along with helper functions for interacting with the maps (such as converting coordinates).
    For more information, check out https://developers.google.com/maps/documentation/static-maps/intro
    
    Terms of use: https://developers.google.com/maps/terms
    '''
    def __init__(self, client):
        self._client = client
    def get_distance(self, start_latitude: float, start_longitude: float, end_latitude: float, end_longitude: float) -> float:
        '''
        Get the straight line distance between two points in meters.
        
        :start_latitude: Latitude of start point
        
        :start_longitude: Longitude of start point
        
        :end_latitude: Latitude of end point
        
        :end_longitude: Longitude of end point
        
        :returns: Distance in meters
        '''
        res = self._client._call('GoogleMaps', 'getDistance', { 'startLatitude': start_latitude, 'startLongitude': start_longitude, 'endLatitude': end_latitude, 'endLongitude': end_longitude })
        return float(res)
    def get_earth_coordinates(self, x: float, y: float) -> list:
        '''
        Get the earth coordinates [latitude, longitude] of a given point in the last requested map image [x, y].
        
        :x: x position of the point
        
        :y: y position of the point
        
        :returns: A list containing the latitude and longitude of the given point.
        '''
        return self._client._call('GoogleMaps', 'getEarthCoordinates', { 'x': x, 'y': y })
    def get_image_coordinates(self, latitude: float, longitude: float) -> list:
        '''
        Get the image coordinates [x, y] of a given location on the earth [latitude, longitude].
        
        :latitude: latitude of the point
        
        :longitude: longitude of the point
        
        :returns: A list containing the [x, y] position of the given point.
        '''
        return self._client._call('GoogleMaps', 'getImageCoordinates', { 'latitude': latitude, 'longitude': longitude })
    def get_latitude_from_y(self, y: float) -> float:
        '''
        Convert y value of map image to latitude.
        
        :y: y value of map image
        
        :returns: Latitude of the y value from the image
        '''
        res = self._client._call('GoogleMaps', 'getLatitudeFromY', { 'y': y })
        return float(res)
    def get_longitude_from_x(self, x: float) -> float:
        '''
        Convert x value of map image to longitude.
        
        :x: x value of map image
        
        :returns: Longitude of the x value from the image
        '''
        res = self._client._call('GoogleMaps', 'getLongitudeFromX', { 'x': x })
        return float(res)
    def get_map(self, latitude: float, longitude: float, width: int, height: int, zoom: int) -> Any:
        '''
        Get a map image of the given region.
        
        :latitude: Latitude of center point
        
        :longitude: Longitude of center point
        
        :width: Image width
        
        :height: Image height
        
        :zoom: Zoom level of map image
        
        :returns: Map image
        '''
        return self._client._call('GoogleMaps', 'getMap', { 'latitude': latitude, 'longitude': longitude, 'width': width, 'height': height, 'zoom': zoom })
    def get_satellite_map(self, latitude: float, longitude: float, width: int, height: int, zoom: int) -> Any:
        '''
        Get a satellite map image of the given region.
        
        :latitude: Latitude of center point
        
        :longitude: Longitude of center point
        
        :width: Image width
        
        :height: Image height
        
        :zoom: Zoom level of map image
        
        :returns: Map image
        '''
        return self._client._call('GoogleMaps', 'getSatelliteMap', { 'latitude': latitude, 'longitude': longitude, 'width': width, 'height': height, 'zoom': zoom })
    def get_terrain_map(self, latitude: float, longitude: float, width: int, height: int, zoom: int) -> Any:
        '''
        Get a terrain map image of the given region.
        
        :latitude: Latitude of center point
        
        :longitude: Longitude of center point
        
        :width: Image width
        
        :height: Image height
        
        :zoom: Zoom level of map image
        
        :returns: Map image
        '''
        return self._client._call('GoogleMaps', 'getTerrainMap', { 'latitude': latitude, 'longitude': longitude, 'width': width, 'height': height, 'zoom': zoom })
    def get_xfrom_longitude(self, longitude: float) -> float:
        '''
        Convert longitude to the x value on the map image.
        
        :longitude: Longitude coordinate
        
        :returns: Map x coordinate of the given longitude
        '''
        res = self._client._call('GoogleMaps', 'getXFromLongitude', { 'longitude': longitude })
        return float(res)
    def get_yfrom_latitude(self, latitude: float) -> float:
        '''
        Convert latitude to the y value on the map image.
        
        :latitude: Latitude coordinate
        
        :returns: Map y coordinate of the given latitude
        '''
        res = self._client._call('GoogleMaps', 'getYFromLatitude', { 'latitude': latitude })
        return float(res)
    def max_latitude(self) -> float:
        '''
        Get the maximum latitude of the current map.
        
        :returns: 
        '''
        res = self._client._call('GoogleMaps', 'maxLatitude', {  })
        return float(res)
    def max_longitude(self) -> float:
        '''
        Get the maximum longitude of the current map.
        
        :returns: 
        '''
        res = self._client._call('GoogleMaps', 'maxLongitude', {  })
        return float(res)
    def min_latitude(self) -> float:
        '''
        Get the minimum latitude of the current map.
        
        :returns: 
        '''
        res = self._client._call('GoogleMaps', 'minLatitude', {  })
        return float(res)
    def min_longitude(self) -> float:
        '''
        Get the minimum longitude of the current map.
        
        :returns: 
        '''
        res = self._client._call('GoogleMaps', 'minLongitude', {  })
        return float(res)
class GoogleStreetView:
    '''
    The GoogleStreetView Service provides access to the Google Street View Image API
    For more information, check out https://developers.google.com/maps/documentation/streetview/intro
    
    Terms of use: https://developers.google.com/maps/terms
    '''
    def __init__(self, client):
        self._client = client
    def get_info(self, latitude: float, longitude: float, fieldofview: float, heading: float, pitch: float) -> dict:
        '''
        Get Street View metadata of a location using coordinates.
        
        Status explanation:
        
        - OK - No errors occurred.
        - ZERO_RESULTS - No image could be found near the provided location.
        - NOT_FOUND - The location provided could not be found.
        
        :latitude: Latitude coordinate of location
        
        :longitude: Longitude coordinate of location
        
        :fieldofview: Field of View of image, maximum of 120
        
        :heading: Heading of view
        
        :pitch: Pitch of view, 90 to point up, -90 to point down
        
        :returns: Metadata infromation about the requested Street View.
        '''
        res = self._client._call('GoogleStreetView', 'getInfo', { 'latitude': latitude, 'longitude': longitude, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
        return dict(res)
    def get_info_from_address(self, location: str, fieldofview: float, heading: float, pitch: float) -> dict:
        '''
        Get Street View metadata of a location using a location query.
        
        Status explanation:
        
        - OK - No errors occurred.
        - ZERO_RESULTS - No image could be found near the provided location.
        - NOT_FOUND - The location provided could not be found.
        
        :location: Address or Name of location
        
        :fieldofview: Field of View of image, maximum of 120
        
        :heading: Heading of view
        
        :pitch: Pitch of view, 90 to point up, -90 to point down
        
        :returns: Metadata infromation about the requested Street View.
        '''
        res = self._client._call('GoogleStreetView', 'getInfoFromAddress', { 'location': location, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
        return dict(res)
    def get_view(self, latitude: float, longitude: float, width: float, height: float, fieldofview: float, heading: float, pitch: float) -> Any:
        '''
        Get Street View image of a location using coordinates
        
        :latitude: Latitude coordinate of location
        
        :longitude: Longitude coordinate of location
        
        :width: Width of image
        
        :height: Height of image
        
        :fieldofview: Field of View of image, maximum of 120
        
        :heading: Heading of view
        
        :pitch: Pitch of view, 90 to point up, -90 to point down
        
        :returns: Image of requested location with specified size and orientation
        '''
        return self._client._call('GoogleStreetView', 'getView', { 'latitude': latitude, 'longitude': longitude, 'width': width, 'height': height, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
    def get_view_from_address(self, location: str, width: float, height: float, fieldofview: float, heading: float, pitch: float) -> Any:
        '''
        Get Street View image of a location from a location string
        
        :location: Address or Name of location
        
        :width: Width of image
        
        :height: Height of image
        
        :fieldofview: Field of View of image, maximum of 120
        
        :heading: Heading of view
        
        :pitch: Pitch of view, 90 to point up, -90 to point down
        
        :returns: Image of requested location with specified size and orientation
        '''
        return self._client._call('GoogleStreetView', 'getViewFromAddress', { 'location': location, 'width': width, 'height': height, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
    def is_available(self, latitude: float, longitude: float, fieldofview: float, heading: float, pitch: float) -> bool:
        '''
        Check for availability of imagery at a location using coordinates
        
        :latitude: Latitude coordinate of location
        
        :longitude: Longitude coordinate of location
        
        :fieldofview: Field of View of image, maximum of 120
        
        :heading: Heading of view
        
        :pitch: Pitch of view, 90 to point up, -90 to point down
        
        :returns: true if imagery is available
        '''
        res = self._client._call('GoogleStreetView', 'isAvailable', { 'latitude': latitude, 'longitude': longitude, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
        return bool(res)
    def is_available_from_address(self, location: str, fieldofview: float, heading: float, pitch: float) -> bool:
        '''
        Check for availability of imagery at a location using an address
        
        :location: Address or Name of location
        
        :fieldofview: Field of View of image, maximum of 120
        
        :heading: Heading of view
        
        :pitch: Pitch of view, 90 to point up, -90 to point down
        
        :returns: true if imagery is available
        '''
        res = self._client._call('GoogleStreetView', 'isAvailableFromAddress', { 'location': location, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
        return bool(res)
class Hangman:
    '''
    The Hangman Service provides helpers for mediating a distributed game of hangman.
    '''
    def __init__(self, client):
        self._client = client
    def get_currently_known_word(self) -> str:
        '''
        Get current word for the game
        
        :returns: Current word in use
        '''
        res = self._client._call('Hangman', 'getCurrentlyKnownWord', {  })
        return str(res)
    def get_wrong_count(self) -> int:
        '''
        Get number of wrong guesses made
        
        :returns: Number of wrong guesses
        '''
        res = self._client._call('Hangman', 'getWrongCount', {  })
        return int(res)
    def guess(self, letter: str):
        '''
        Make a guess in the game
        
        :letter: Letter to guess
        '''
        return self._client._call('Hangman', 'guess', { 'letter': letter })
    def is_word_guessed(self) -> bool:
        '''
        Get if word has been guessed
        
        :returns: State of word
        '''
        res = self._client._call('Hangman', 'isWordGuessed', {  })
        return bool(res)
    def set_word(self, word: str):
        '''
        Set current word for the game
        
        :word: New word to use
        '''
        return self._client._call('Hangman', 'setWord', { 'word': word })
class HistoricalTemperature:
    '''
    Access to Berkeley Earth data.
    See http://berkeleyearth.org/data/ for additional details.
    
    These RPCs take a region argument, which can either be a country
    or one of the following special values:
    
    - all land - get data for all landmasses around the world
    - global - get data for the entire Earth (including oceans)
    - northern hemisphere - only northern landmasses
    - southern hemisphere - only southern landmasses
    '''
    def __init__(self, client):
        self._client = client
    def annual_anomaly(self, region: str) -> List[list]:
        '''
        Get the 12 month averaged anomaly data for a region
        
        :region: Name of region/country
        
        :returns: Monthly data points
        '''
        return self._client._call('HistoricalTemperature', 'annualAnomaly', { 'region': region })
    def five_year_anomaly(self, region: str) -> List[list]:
        '''
        Get the 5-year averaged anomaly data for a region
        
        :region: Name of region/country
        
        :returns: Monthly data points
        '''
        return self._client._call('HistoricalTemperature', 'fiveYearAnomaly', { 'region': region })
    def monthly_anomaly(self, region: str) -> List[list]:
        '''
        Get the monthly anomaly data for a region
        
        :region: Name of region/country
        
        :returns: Monthly data points
        '''
        return self._client._call('HistoricalTemperature', 'monthlyAnomaly', { 'region': region })
    def ten_year_anomaly(self, region: str) -> List[list]:
        '''
        Get the 10-year averaged anomaly data for a region
        
        :region: Name of region/country
        
        :returns: Monthly data points
        '''
        return self._client._call('HistoricalTemperature', 'tenYearAnomaly', { 'region': region })
    def twenty_year_anomaly(self, region: str) -> List[list]:
        '''
        Get the 20-year averaged anomaly data for a region
        
        :region: Name of region/country
        
        :returns: Monthly data points
        '''
        return self._client._call('HistoricalTemperature', 'twentyYearAnomaly', { 'region': region })
class HumanMortalityDatabase:
    '''
    This service accesses data from the human mortality database which tabulates
    death rates broken down by age group and gender for various countries.
    
    For more information, see https://www.mortality.org/.
    
    Note: for countries that don't report separate male and female death counts,
    the gender breakdowns are just the total multiplied by a rough estimate
    of the percent of people in that country who are male/female.
    '''
    def __init__(self, client):
        self._client = client
    def get_all_data(self) -> list:
        '''
        Get all the mortality data. This is potentially a lot of data.
        Only use this if you truly need access to all data.
        
        This is returned as structured data organized by country, then by date (mm/dd/yyyy), then by gender, then by category.
        
        :returns: all available data
        '''
        return self._client._call('HumanMortalityDatabase', 'getAllData', {  })
    def get_all_data_for_country(self, country: str) -> list:
        '''
        Get all the data associated with the given country.
        This is an object organized by year, then by week, then broken down by gender.
        
        :country: Name of the country to look up
        
        :returns: the requested data
        '''
        return self._client._call('HumanMortalityDatabase', 'getAllDataForCountry', { 'country': country })
    def get_categories(self) -> list:
        '''
        Get a list of all the categories represented in the data.
        These can be used in a query.
        
        :returns: the requested data
        '''
        return self._client._call('HumanMortalityDatabase', 'getCategories', {  })
    def get_countries(self) -> list:
        '''
        Get a list of all the countries represented in the data.
        These are not the country names, but a unique identifier for them.
        
        :returns: the requested data
        '''
        return self._client._call('HumanMortalityDatabase', 'getCountries', {  })
    def get_genders(self) -> list:
        '''
        Get a list of all the valid genders represented in the data.
        These can be used in a query.
        
        :returns: the requested data
        '''
        return self._client._call('HumanMortalityDatabase', 'getGenders', {  })
    def get_time_series(self, country: str, gender: Optional[str] = None, category: Optional[str] = None) -> list:
        '''
        Get the time series data for the given country, filtered to the specified gender and category
        in month/day/year format.
        
        :country: name of the country to look up
        
        :gender: gender group for filtering. Defaults to both.
        
        :category: category for filtering. Defaults to deaths total.
        
        :returns: the requested data
        '''
        return self._client._call('HumanMortalityDatabase', 'getTimeSeries', { 'country': country, 'gender': gender, 'category': category })
class HurricaneData:
    '''
    The HurricaneData service provides access to the revised Atlantic hurricane
    database (HURDAT2) from the National Hurricane Center (NHC).
    
    For more information, check out https://www.aoml.noaa.gov/hrd/data_sub/re_anal.html
    '''
    def __init__(self, client):
        self._client = client
    def get_hurricane_data(self, name: str, year: float) -> List[dict]:
        '''
        Get hurricane data including location, maximum winds, and central pressure.
        
        :name: name of the hurricane
        
        :year: year that the hurricane occurred in
        
        :returns: All recorded data for the given hurricane
        '''
        res = self._client._call('HurricaneData', 'getHurricaneData', { 'name': name, 'year': year })
        return _common.vectorize(dict)(res)
    def get_hurricanes_in_year(self, year: float) -> List[str]:
        '''
        Get the names of all hurricanes occurring in the given year.
        
        :year: 
        
        :returns: names
        '''
        res = self._client._call('HurricaneData', 'getHurricanesInYear', { 'year': year })
        return _common.vectorize(str)(res)
    def get_years_with_hurricane_named(self, name: str) -> List[float]:
        '''
        Get the years in which a hurricane with the given name occurred.
        
        :name: name of the hurricane to find the year(s) of
        
        :returns: years - list with all of the years that a particular name has been used for a hurricane
        '''
        res = self._client._call('HurricaneData', 'getYearsWithHurricaneNamed', { 'name': name })
        return _common.vectorize(float)(res)
class IceCoreData:
    '''
    Access to NOAA Paleoclimatology ice core data.
    
    For more information, check out
    https://www.ncdc.noaa.gov/data-access/paleoclimatology-data/datasets/ice-core.
    
    Original datasets are available at:
    
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/antarctica2015co2composite.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/antarctica2015co2law.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/antarctica2015co2wais.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/vostok/co2nat.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/vostok/deutnat.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/epica_domec/edc3deuttemp2007.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/greenland/summit/grip/isotopes/gripd18o.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/vostok/gt4nat.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/law/law2012d18o.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/wdc05a2013d18o.txt
    '''
    def __init__(self, client):
        self._client = client
    def get_carbon_dioxide_data(self, core: str, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get CO2 in ppm (parts per million) by year from the ice core.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :core: Core to get data from
        
        :startyear: first year of data to include
        
        :endyear: last year of data to include
        
        :returns: the requested data
        '''
        return self._client._call('IceCoreData', 'getCarbonDioxideData', { 'core': core, 'startyear': startyear, 'endyear': endyear })
    def get_data_availability(self) -> Any:
        '''
        Get a table showing the amount of available data for each ice core.
        
        :returns: data availability table
        '''
        return self._client._call('IceCoreData', 'getDataAvailability', {  })
    def get_delta18_odata(self, core: str, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get delta-O-18 in per mil (parts per thousand) by year from the ice core.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :core: Ice core to get data from
        
        :startyear: first year of data to include
        
        :endyear: last year of data to include
        
        :returns: the requested data
        '''
        return self._client._call('IceCoreData', 'getDelta18OData', { 'core': core, 'startyear': startyear, 'endyear': endyear })
    def get_deuterium_data(self, core: str, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get deuterium in per mil (parts per thousand) by year from the ice core.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :core: Ice core to get data from
        
        :startyear: first year of data to include
        
        :endyear: last year of data to include
        
        :returns: the requested data
        '''
        return self._client._call('IceCoreData', 'getDeuteriumData', { 'core': core, 'startyear': startyear, 'endyear': endyear })
    def get_ice_core_metadata(self, core: str) -> dict:
        '''
        Get metadata about an ice core including statistics about the available data.
        
        :core: Name of core to get metadata of
        
        :returns: ice core metadata
        '''
        res = self._client._call('IceCoreData', 'getIceCoreMetadata', { 'core': core })
        return dict(res)
    def get_ice_core_names(self) -> List[str]:
        '''
        Get names of ice cores with data available.
        
        :returns: list of ice core names
        '''
        res = self._client._call('IceCoreData', 'getIceCoreNames', {  })
        return _common.vectorize(str)(res)
    def get_temperature_data(self, core: str, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get temperature difference in Celsius by year from the ice core.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :core: Ice core to get data from
        
        :startyear: first year of data to include
        
        :endyear: last year of data to include
        
        :returns: the requested data
        '''
        return self._client._call('IceCoreData', 'getTemperatureData', { 'core': core, 'startyear': startyear, 'endyear': endyear })
class IoTScape:
    '''
    The IoTScape Service enables remote devices to provide custom services. Custom
    Services can be found under the "Community/Devices" section using the call <RPC>
    block.
    '''
    def __init__(self, client):
        self._client = client
    def get_devices(self, service: str):
        '''
        List IDs of devices associated for a service
        
        :service: Name of service to get device IDs for
        '''
        return self._client._call('IoTScape', 'getDevices', { 'service': service })
    def get_message_types(self, service: str):
        '''
        List the message types associated with a service
        
        :service: Name of service to get events for
        '''
        return self._client._call('IoTScape', 'getMessageTypes', { 'service': service })
    def get_services(self):
        '''
        List all IoTScape services registered with the server
        '''
        return self._client._call('IoTScape', 'getServices', {  })
    def send(self, service: str, id: str, command: str):
        '''
        Make a call to a device as a text command
        
        :service: Name of service to make call to
        
        :id: ID of device to make call to
        
        :command: Input to RPC
        '''
        return self._client._call('IoTScape', 'send', { 'service': service, 'id': id, 'command': command })
class KeyValueStore:
    '''
    The KeyValueStore Service provides basic storage functionality using a hierarchical
    key-value storage (similar to CloudVariables).
    '''
    def __init__(self, client):
        self._client = client
    def child(self, key: str, password: Optional[str] = None) -> List[str]:
        '''
        Get the IDs of the child keys.
        
        :key: 
        
        :password: Password (if password-protected)
        
        :returns: list of child key ids
        '''
        res = self._client._call('KeyValueStore', 'child', { 'key': key, 'password': password })
        return _common.vectorize(str)(res)
    def delete(self, key: str, password: Optional[str] = None):
        '''
        Delete the stored value for a key.
        
        :key: Key to remove from store
        
        :password: Password (if password-protected)
        '''
        return self._client._call('KeyValueStore', 'delete', { 'key': key, 'password': password })
    def get(self, key: str, password: Optional[str] = None) -> Any:
        '''
        Get the stored value for a key.
        
        :key: Fetch value for the given key
        
        :password: Password (if password-protected)
        
        :returns: the stored value
        '''
        return self._client._call('KeyValueStore', 'get', { 'key': key, 'password': password })
    def parent(self, key: str) -> str:
        '''
        Get the ID of the parent key.
        
        :key: key to get the parent of
        
        :returns: the parent key
        '''
        res = self._client._call('KeyValueStore', 'parent', { 'key': key })
        return str(res)
    def put(self, key: str, value: Any, password: Optional[str] = None):
        '''
        Set the stored value for a key.
        
        :key: Key to use for retrieving the variable
        
        :value: Value to associated with key
        
        :password: Password (if password-protected)
        '''
        return self._client._call('KeyValueStore', 'put', { 'key': key, 'value': value, 'password': password })
class MaunaLoaCO2Data:
    '''
    Access to NOAA Earth System Research Laboratory data collected from Mauna Loa, Hawaii.
    
    See https://www.esrl.noaa.gov/gmd/ccgg/trends/ for additional details.
    '''
    def __init__(self, client):
        self._client = client
    def get_co2_trend(self, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get the mole fraction of CO2 (in parts per million) by year with the seasonal
        cycle removed.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :startyear: first year of data to include
        
        :endyear: last year of data to include
        
        :returns: 
        '''
        return self._client._call('MaunaLoaCO2Data', 'getCO2Trend', { 'startyear': startyear, 'endyear': endyear })
    def get_raw_co2(self, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get the mole fraction of CO2 (in parts per million) by year. Missing measurements
        are interpolated.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :startyear: first year of data to include
        
        :endyear: last year of data to include
        
        :returns: 
        '''
        return self._client._call('MaunaLoaCO2Data', 'getRawCO2', { 'startyear': startyear, 'endyear': endyear })
class MetMuseum:
    '''
    Access the Metropolitan Museum of Art's collection.
    For explanation on the different attributes for each object,
    visit https://metmuseum.github.io.
    '''
    def __init__(self, client):
        self._client = client
    def advanced_search(self, field: str, query: str, skip: Optional[float] = None, limit: Optional[float] = None) -> list:
        '''
        Search the Metropolitan Museum of Art
        
        :field: field to search in
        
        :query: text query to look for
        
        :skip: used to paginate the results, number of records to skip from the begining
        
        :limit: limit the number of returned results (maximum of 50)
        
        :returns: results
        '''
        return self._client._call('MetMuseum', 'advancedSearch', { 'field': field, 'query': query, 'skip': skip, 'limit': limit })
    def fields(self) -> list:
        '''
        Get a list of available attributes for museum's objects
        
        :returns: available headers
        '''
        return self._client._call('MetMuseum', 'fields', {  })
    def get_image_urls(self, id: float) -> list:
        '''
        Retrieves the image links for a public domain object
        Note: use costume loader library to load the images.
        
        :id: object id
        
        :returns: List of images
        '''
        return self._client._call('MetMuseum', 'getImageUrls', { 'id': id })
    def get_info(self, id: float) -> list:
        '''
        Retrieves extended information about a single object
        
        :id: object id
        
        :returns: List of images
        '''
        return self._client._call('MetMuseum', 'getInfo', { 'id': id })
    def search_by_artist_display_bio(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByArtistDisplayBio', { 'query': query })
    def search_by_artist_display_name(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByArtistDisplayName', { 'query': query })
    def search_by_classification(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByClassification', { 'query': query })
    def search_by_country(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByCountry', { 'query': query })
    def search_by_credit_line(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByCreditLine', { 'query': query })
    def search_by_department(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByDepartment', { 'query': query })
    def search_by_dimensions(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByDimensions', { 'query': query })
    def search_by_is_highlight(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByIsHighlight', { 'query': query })
    def search_by_medium(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByMedium', { 'query': query })
    def search_by_object_date(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByObjectDate', { 'query': query })
    def search_by_object_name(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByObjectName', { 'query': query })
    def search_by_repository(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByRepository', { 'query': query })
    def search_by_title(self, query: Any):
        '''
        :query: 
        '''
        return self._client._call('MetMuseum', 'searchByTitle', { 'query': query })
class MovieDB:
    '''
    The MovieDB Service provides access to movie data using TMDB (The MovieDB API).
    For more information, check out https://www.themoviedb.org/
    
    Terms of use: https://www.themoviedb.org/documentation/api/terms-of-use
    '''
    def __init__(self, client):
        self._client = client
    def get_image(self, path: str) -> Any:
        '''
        Get an image from a path.
        
        :path: location of the image
        
        :returns: the requested image
        '''
        return self._client._call('MovieDB', 'getImage', { 'path': path })
    def movie_backdrop_path(self, id: str) -> str:
        '''
        Get the image path for a given movie backdrop.
        
        :id: Movie ID
        
        :returns: the image path
        '''
        res = self._client._call('MovieDB', 'movieBackdropPath', { 'id': id })
        return str(res)
    def movie_budget(self, id: str):
        '''
        Get the budget for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieBudget', { 'id': id })
    def movie_cast_characters(self, id: str):
        '''
        Get the cast characters for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieCastCharacters', { 'id': id })
    def movie_cast_names(self, id: str):
        '''
        Get the cast names for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieCastNames', { 'id': id })
    def movie_cast_person_ids(self, id: str):
        '''
        Get the cast IDs for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieCastPersonIDs', { 'id': id })
    def movie_cast_profile_paths(self, id: str):
        '''
        Get the cast profile paths for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieCastProfilePaths', { 'id': id })
    def movie_crew_jobs(self, id: str):
        '''
        Get the crew jobs for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieCrewJobs', { 'id': id })
    def movie_crew_names(self, id: str):
        '''
        Get the crew names for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieCrewNames', { 'id': id })
    def movie_crew_person_ids(self, id: str):
        '''
        Get the crew IDs for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieCrewPersonIDs', { 'id': id })
    def movie_crew_profile_paths(self, id: str):
        '''
        Get the crew profile paths for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieCrewProfilePaths', { 'id': id })
    def movie_genres(self, id: str):
        '''
        Get the genres of a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieGenres', { 'id': id })
    def movie_original_language(self, id: str):
        '''
        Get the original language of a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieOriginalLanguage', { 'id': id })
    def movie_original_title(self, id: str):
        '''
        Get the original title of a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieOriginalTitle', { 'id': id })
    def movie_overview(self, id: str):
        '''
        Get an overview for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieOverview', { 'id': id })
    def movie_popularity(self, id: str):
        '''
        Get the popularity for a given movie.
        
        For more information, check out https://developers.themoviedb.org/3/getting-started/popularity
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'moviePopularity', { 'id': id })
    def movie_poster_path(self, id: str):
        '''
        Get the poster path for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'moviePosterPath', { 'id': id })
    def movie_production_companies(self, id: str):
        '''
        Get the production companies for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieProductionCompanies', { 'id': id })
    def movie_production_countries(self, id: str):
        '''
        Get the countries in which a given movie was produced.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieProductionCountries', { 'id': id })
    def movie_release_date(self, id: str):
        '''
        Get the release data for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieReleaseDate', { 'id': id })
    def movie_revenue(self, id: str):
        '''
        Get the revenue for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieRevenue', { 'id': id })
    def movie_runtime(self, id: str):
        '''
        Get the runtime for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieRuntime', { 'id': id })
    def movie_spoken_languages(self, id: str):
        '''
        Get the spoken languages for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieSpokenLanguages', { 'id': id })
    def movie_tagline(self, id: str):
        '''
        Get the tagline for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieTagline', { 'id': id })
    def movie_title(self, id: str):
        '''
        Get the title for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieTitle', { 'id': id })
    def movie_vote_average(self, id: str):
        '''
        Get the average vote for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieVoteAverage', { 'id': id })
    def movie_vote_count(self, id: str):
        '''
        Get the vote count for a given movie.
        
        :id: Movie ID
        '''
        return self._client._call('MovieDB', 'movieVoteCount', { 'id': id })
    def person_biography(self, id: str):
        '''
        Get the biography for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personBiography', { 'id': id })
    def person_birthday(self, id: str):
        '''
        Get the birthday of a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personBirthday', { 'id': id })
    def person_cast_characters(self, id: str):
        '''
        Get the characters played by a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCastCharacters', { 'id': id })
    def person_cast_movie_ids(self, id: str):
        '''
        Get the movies in which a given person was cast.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCastMovieIDs', { 'id': id })
    def person_cast_original_titles(self, id: str):
        '''
        Get the original titles in which a given person was cast.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCastOriginalTitles', { 'id': id })
    def person_cast_poster_paths(self, id: str):
        '''
        Get the cast poster paths for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCastPosterPaths', { 'id': id })
    def person_cast_release_dates(self, id: str):
        '''
        Get the cast release dates for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCastReleaseDates', { 'id': id })
    def person_cast_titles(self, id: str):
        '''
        Get the cast titles for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCastTitles', { 'id': id })
    def person_crew_jobs(self, id: str):
        '''
        Get the crew jobs for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCrewJobs', { 'id': id })
    def person_crew_movie_ids(self, id: str):
        '''
        Get the movie IDs for which a given person was a member of the crew.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCrewMovieIDs', { 'id': id })
    def person_crew_original_titles(self, id: str):
        '''
        Get the original titles for which a given person was a member of the crew.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCrewOriginalTitles', { 'id': id })
    def person_crew_poster_paths(self, id: str):
        '''
        Get the poster paths for movies in which a given person was a member of the crew.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCrewPosterPaths', { 'id': id })
    def person_crew_release_dates(self, id: str):
        '''
        Get the release dates for movies in which a given person was a member of the crew.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCrewReleaseDates', { 'id': id })
    def person_crew_titles(self, id: str):
        '''
        Get the crew titles for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personCrewTitles', { 'id': id })
    def person_deathday(self, id: str):
        '''
        Get the death date of a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personDeathday', { 'id': id })
    def person_gender(self, id: str):
        '''
        Get the gender of a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personGender', { 'id': id })
    def person_image_aspect_ratios(self, id: str):
        '''
        Get the image aspect ratios for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personImageAspectRatios', { 'id': id })
    def person_image_file_paths(self, id: str):
        '''
        Get the image paths for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personImageFilePaths', { 'id': id })
    def person_image_heights(self, id: str):
        '''
        Get the image heights for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personImageHeights', { 'id': id })
    def person_image_vote_counts(self, id: str):
        '''
        Get the image vote counts for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personImageVoteCounts', { 'id': id })
    def person_image_widths(self, id: str):
        '''
        Get the image widths for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personImageWidths', { 'id': id })
    def person_name(self, id: str):
        '''
        Get the name of a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personName', { 'id': id })
    def person_place_of_birth(self, id: str):
        '''
        Get the place of birth for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personPlaceOfBirth', { 'id': id })
    def person_popularity(self, id: str):
        '''
        Get the popularity of a given person.
        
        For more information, check out https://developers.themoviedb.org/3/getting-started/popularity
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personPopularity', { 'id': id })
    def person_profile_path(self, id: str):
        '''
        Get the profile path for a given person.
        
        :id: Person ID
        '''
        return self._client._call('MovieDB', 'personProfilePath', { 'id': id })
    def search_movie(self, title: str):
        '''
        Search for a given movie and return movie IDs.
        
        :title: Title of movie
        '''
        return self._client._call('MovieDB', 'searchMovie', { 'title': title })
    def search_person(self, name: str):
        '''
        Search for a given actor and return person IDs.
        
        :name: Name of person to search for
        '''
        return self._client._call('MovieDB', 'searchPerson', { 'name': name })
class NASA:
    '''
    The NASA Service provides access to planetary pictures and mars weather data.
    For more information, check out https://api.nasa.gov/.
    '''
    def __init__(self, client):
        self._client = client
    def apod(self):
        '''
        Fetch the "Astronomy Picture of the Day" from NASA
        '''
        return self._client._call('NASA', 'apod', {  })
    def apod_details(self):
        '''
        Fetch additional information about the "Astronomy Picture of the Day"
        '''
        return self._client._call('NASA', 'apodDetails', {  })
    def apod_media(self) -> str:
        '''
        NASA's 'Astronomy Picture of the Day' media
        
        :returns: 
        '''
        res = self._client._call('NASA', 'apodMedia', {  })
        return str(res)
class NPlayer:
    '''
    The NPlayer Service provides helpers RPCs for ensuring round-robin turn taking
    among the roles in the project's room.
    
    Each role will receive a "start game" message at the start and then "start turn"
    message when it is the given role's turn to act.
    '''
    def __init__(self, client):
        self._client = client
    def end_turn(self, next: Optional[str] = None):
        '''
        End your current turn.
        
        :next: Specify the player to go next
        '''
        return self._client._call('NPlayer', 'endTurn', { 'next': next })
    def get_active(self) -> str:
        '''
        Get the player whose turn it currently is.
        
        :returns: role id of the active player, or empty string if there are no players
        '''
        res = self._client._call('NPlayer', 'getActive', {  })
        return str(res)
    def get_n(self) -> int:
        '''
        Get the number of detected players in the game.
        
        :returns: number of players
        '''
        res = self._client._call('NPlayer', 'getN', {  })
        return int(res)
    def get_next(self) -> str:
        '''
        Get the player who will be active next.
        
        :returns: role id of the next player, or empty string if there are no players
        '''
        res = self._client._call('NPlayer', 'getNext', {  })
        return str(res)
    def get_previous(self) -> str:
        '''
        Get the player who played last.
        
        :returns: role id of the previous player, or empty string if no previous player
        '''
        res = self._client._call('NPlayer', 'getPrevious', {  })
        return str(res)
    def start(self) -> bool:
        '''
        Start a new turn-based game.
        
        :returns: true on successful start
        '''
        res = self._client._call('NPlayer', 'start', {  })
        return bool(res)
class NewYorkPublicLibrary:
    '''
    The New York Public Library (NYPL) Service provides access to NYPL's online repository of historical items.
    '''
    def __init__(self, client):
        self._client = client
    def get_details(self, uuid: str) -> list:
        '''
        Get details about the item.
        This requires the uuid for the object, which can be retrieved from NewYorkPublicLibrary.search.
        
        :uuid: uuid of the object
        
        :returns: Item details
        '''
        return self._client._call('NewYorkPublicLibrary', 'getDetails', { 'uuid': uuid })
    def get_image(self, item_id: str) -> Any:
        '''
        Get an image of the object.
        This requires the itemID for the object, which can be retrieved from NewYorkPublicLibrary.search.
        
        :item_id: itemID of the object
        
        :returns: An image of the object, if one is available
        '''
        return self._client._call('NewYorkPublicLibrary', 'getImage', { 'itemID': item_id })
    def search(self, term: str, per_page: Optional[float] = None, page: Optional[float] = None) -> List[dict]:
        '''
        Search the New York Public Library collection and return matching items.
        Because there may be many matching items, search results are arranged in pages.
        You can specify the number of items in each page and the page number to retrieve.
        
        This returns a list of up to perPage matches.
        Each item in the list is structured data containing details about the object.
        This includes:
        
        - uuid - a general identifier for the object, needed for NewYorkPublicLibrary.getDetails
        - itemID - another identifier, needed for NewYorkPublicLibrary.getImage
        - title - the title of the object
        - dateDigitized - a timestamp of when the object was added to the database
        
        :term: Search term
        
        :per_page: Maximum number of items in a page of results (default 50)
        
        :page: Page number of results to get (default 1)
        
        :returns: An list of up to perPage matching objects
        '''
        res = self._client._call('NewYorkPublicLibrary', 'search', { 'term': term, 'perPage': per_page, 'page': page })
        return _common.vectorize(dict)(res)
class NewYorkTimes:
    '''
    The NewYorkTimes service provides access to the New York Times API including access
    to Moview Reviews, Top Stories, and their Semantic API.
    '''
    def __init__(self, client):
        self._client = client
    def get_article_sections(self) -> List[str]:
        '''
        Get a list of all valid article sections.
        
        :returns: 
        '''
        res = self._client._call('NewYorkTimes', 'getArticleSections', {  })
        return _common.vectorize(str)(res)
    def get_articles_with_concept(self, concept: dict) -> list:
        '''
        Fetch up to 10 articles containing the given concept.
        
        :concept: 
          - :name: (str) 
          - :type: (str) 
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'getArticlesWithConcept', { 'concept': concept })
    def get_best_seller_lists(self) -> List[str]:
        '''
        Get the best seller list names.
        
        :returns: 
        '''
        res = self._client._call('NewYorkTimes', 'getBestSellerLists', {  })
        return _common.vectorize(str)(res)
    def get_best_sellers(self, list: str, date: Optional[str] = None) -> list:
        '''
        Get the best selling books for a given list and date.
        
        :list: 
        
        :date: 
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'getBestSellers', { 'list': list, 'date': date })
    def get_concept_info(self, concept: dict) -> Any:
        '''
        Get additional information about a concept such as links to other concepts and
        geocodes.
        
        :concept: 
          - :name: (str) 
          - :type: (str) 
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'getConceptInfo', { 'concept': concept })
    def get_concept_types(self) -> List[str]:
        '''
        Get a list of all concept types.
        
        :returns: 
        '''
        res = self._client._call('NewYorkTimes', 'getConceptTypes', {  })
        return _common.vectorize(str)(res)
    def get_critics_picks(self, offset: Optional[float] = None) -> list:
        '''
        Get 20 movie reviews picked by critics starting at "offset".
        
        :offset: Must be a multiple of 20
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'getCriticsPicks', { 'offset': offset })
    def get_latest_articles(self, section: str) -> List[str]:
        '''
        Get the latest articles in a given section.
        
        :section: 
        
        :returns: 
        '''
        res = self._client._call('NewYorkTimes', 'getLatestArticles', { 'section': section })
        return _common.vectorize(str)(res)
    def get_most_emailed_articles(self, period: str) -> list:
        '''
        Get the most emailed articles over the past day, week, or month.
        
        :period: 
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'getMostEmailedArticles', { 'period': period })
    def get_most_shared_articles(self, period: str) -> list:
        '''
        Get the articles shared most on Facebook over the past day, week, or month.
        
        :period: 
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'getMostSharedArticles', { 'period': period })
    def get_most_viewed_articles(self, period: str) -> list:
        '''
        Get the most viewed articles over the past day, week, or month.
        
        :period: 
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'getMostViewedArticles', { 'period': period })
    def get_movie_critic_info(self, name: str) -> list:
        '''
        Get information about a given movie critic.
        
        :name: 
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'getMovieCriticInfo', { 'name': name })
    def get_movie_critics(self) -> List[str]:
        '''
        Get a list of movie critics.
        
        :returns: 
        '''
        res = self._client._call('NewYorkTimes', 'getMovieCritics', {  })
        return _common.vectorize(str)(res)
    def get_movie_reviews(self, offset: Optional[float] = None) -> list:
        '''
        Get 20 movie reviews starting at "offset".
        
        :offset: Must be a multiple of 20
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'getMovieReviews', { 'offset': offset })
    def get_movie_reviews_by_critic(self, critic: str, offset: Optional[float] = None) -> list:
        '''
        Get 20 movie reviews by a given critic starting at "offset".
        
        :critic: 
        
        :offset: Must be a multiple of 20
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'getMovieReviewsByCritic', { 'critic': critic, 'offset': offset })
    def get_top_best_sellers(self, date: str) -> list:
        '''
        Get the top 5 books for all the best seller lists for a given date.
        
        :date: 
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'getTopBestSellers', { 'date': date })
    def get_top_stories(self, section: str) -> List[str]:
        '''
        Get the top stories for a given section.
        
        :section: 
        
        :returns: 
        '''
        res = self._client._call('NewYorkTimes', 'getTopStories', { 'section': section })
        return _common.vectorize(str)(res)
    def search_articles(self, query: str, offset: Optional[float] = None) -> list:
        '''
        Search for articles given a query. Up to 10 articles will be returned.
        More articles can be retrieved by specifying the "offset" or number of
        results to skip before returning the results.
        
        :query: 
        
        :offset: Must be a multiple of 10
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'searchArticles', { 'query': query, 'offset': offset })
    def search_best_sellers(self, title: Optional[str] = None, author: Optional[str] = None, offset: Optional[float] = None) -> list:
        '''
        Search for books on current or previous best seller lists.
        
        :title: 
        
        :author: 
        
        :offset: 
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'searchBestSellers', { 'title': title, 'author': author, 'offset': offset })
    def search_concepts(self, query: str) -> list:
        '''
        Search for concepts of interest.
        
        :query: 
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'searchConcepts', { 'query': query })
    def search_movie_reviews(self, query: str, offset: Optional[float] = None) -> list:
        '''
        Search for movie reviews starting at "offset". Returns up to 20 results.
        
        :query: 
        
        :offset: Must be a multiple of 20
        
        :returns: 
        '''
        return self._client._call('NewYorkTimes', 'searchMovieReviews', { 'query': query, 'offset': offset })
class OceanData:
    '''
    The OceanData service provides access to scientific ocean data including
    temperature and sea level.
    
    For more information, check out:
    
    - http://www.columbia.edu/~mhs119/Sensitivity+SL+CO2/
    - https://www.paleo.bristol.ac.uk/~ggdjl/warm_climates/hansen_etal.pdf.
    '''
    def __init__(self, client):
        self._client = client
    def get_deep_ocean_temp(self, start_year: Optional[float] = None, end_year: Optional[float] = None) -> list:
        '''
        Get historical deep ocean temperatures in Celsius by year.
        
        If startYear or endYear is provided, only measurements within the given range will be returned.
        
        :start_year: earliest year to include in results
        
        :end_year: latest year to include in results
        
        :returns: a list of deep ocean temperatures by year
        '''
        return self._client._call('OceanData', 'getDeepOceanTemp', { 'startYear': start_year, 'endYear': end_year })
    def get_oxygen_ratio(self, start_year: Optional[float] = None, end_year: Optional[float] = None) -> list:
        '''
        Get historical oxygen isotope ratio values by year.
        
        If startYear or endYear is provided, only measurements within the given range will be returned.
        
        :start_year: earliest year to include in results
        
        :end_year: latest year to include in results
        
        :returns: a list of oxygen isotope ratios by year
        '''
        return self._client._call('OceanData', 'getOxygenRatio', { 'startYear': start_year, 'endYear': end_year })
    def get_sea_level(self, start_year: Optional[float] = None, end_year: Optional[float] = None) -> list:
        '''
        Get historical sea level in meters by year.
        
        If startYear or endYear is provided, only measurements within the given range will be returned.
        
        :start_year: earliest year to include in results
        
        :end_year: latest year to include in results
        
        :returns: a list of change in sea level (in meters) by year
        '''
        return self._client._call('OceanData', 'getSeaLevel', { 'startYear': start_year, 'endYear': end_year })
    def get_surface_temp(self, start_year: Optional[float] = None, end_year: Optional[float] = None) -> list:
        '''
        Get historical surface ocean temperatures in Celsius by year.
        
        If startYear or endYear is provided, only measurements within the given range will be returned.
        
        :start_year: earliest year to include in results
        
        :end_year: latest year to include in results
        
        :returns: a list of surface ocean temperatures by year
        '''
        return self._client._call('OceanData', 'getSurfaceTemp', { 'startYear': start_year, 'endYear': end_year })
class PaleoceanOxygenIsotopes:
    '''
    Access to NOAA Global Pliocene-Pleistocene Benthic d18O Stack.
    
    For more information, check out
    https://www.ncdc.noaa.gov/paleo-search/study/5847
    
    Original datasets are available at:
    https://www1.ncdc.noaa.gov/pub/data/paleo/contributions_by_author/lisiecki2005/lisiecki2005.txt.
    '''
    def __init__(self, client):
        self._client = client
    def get_average_sedimentation_rates(self, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get average sedimentation rate value (unit: centimeter per kiloyear).
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :startyear: first year of data to include
        
        :endyear: least year of data to include
        
        :returns: a list of average sedimentation rate by year
        '''
        return self._client._call('PaleoceanOxygenIsotopes', 'getAverageSedimentationRates', { 'startyear': startyear, 'endyear': endyear })
    def get_delta18_o(self, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get delta 18O value (unit: per mill. It is a parts per thousand unit, often used directly to 
        refer to isotopic ratios and calculated by calculating the ratio of isotopic concentrations in 
        a sample and in a standard, subtracting one and multiplying by one thousand).
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :startyear: first year of data to include
        
        :endyear: least year of data to include
        
        :returns: a list of delta 18O values by year
        '''
        return self._client._call('PaleoceanOxygenIsotopes', 'getDelta18O', { 'startyear': startyear, 'endyear': endyear })
    def get_delta18_oerror(self, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get delta 18O error value (unit: per mill).
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :startyear: first year of data to include
        
        :endyear: least year of data to include
        
        :returns: a list of delta 18O error values by year
        '''
        return self._client._call('PaleoceanOxygenIsotopes', 'getDelta18OError', { 'startyear': startyear, 'endyear': endyear })
    def get_normalized_sedimentation_rates(self, startyear: Optional[float] = None, endyear: Optional[float] = None) -> list:
        '''
        Get normalized sedimentation rate value (unit: dimensionless).
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        
        :startyear: first year of data to include
        
        :endyear: least year of data to include
        
        :returns: a list of normalized sedimentation rate by year
        '''
        return self._client._call('PaleoceanOxygenIsotopes', 'getNormalizedSedimentationRates', { 'startyear': startyear, 'endyear': endyear })
class ParallelDots:
    '''
    Uses ParallelDots AI to process or compare text for a variety of features.
    See the API documentation, at 
    http://apis.paralleldots.com/text_docs/index.html
    
    Terms of use: https://www.paralleldots.com/terms-and-conditions
    '''
    def __init__(self, client):
        self._client = client
    def get_abuse(self, text: str) -> dict:
        '''
        Classify the given text as abusive, hate_speech, or neither.
        The returned structured data has confidence levels for each of these categories.
        
        :text: text to analyze
        
        :returns: structured data containing the confidence levels
        '''
        res = self._client._call('ParallelDots', 'getAbuse', { 'text': text })
        return dict(res)
    def get_emotion(self, text: str) -> dict:
        '''
        Find the emotion in the given text.
        This is returned as structured data containing confidence levels for each of the following emotions:
        excited, angry, bored, fear, sad, and happy.
        
        :text: text to analyze
        
        :returns: structured data with confidence levels for each emotion
        '''
        res = self._client._call('ParallelDots', 'getEmotion', { 'text': text })
        return dict(res)
    def get_intent(self, text: str) -> dict:
        '''
        Get the intent of the given text along with the confidence score.
        This is returned as structed data with confidence levels for each of the following intents:
        news, query, spam, marketing, and feedback.
        
        :text: text to analyze
        
        :returns: structed data with confidence levels for each intent
        '''
        res = self._client._call('ParallelDots', 'getIntent', { 'text': text })
        return dict(res)
    def get_keywords(self, text: str) -> list:
        '''
        Extract keywords from the given text along with their confidence score.
        
        :text: text to analyze
        
        :returns: information about keywords in the text
        '''
        return self._client._call('ParallelDots', 'getKeywords', { 'text': text })
    def get_named_entities(self, text: str) -> list:
        '''
        Identify named entities in the given text.
        
        :text: text to analyze
        
        :returns: speculated information about named entities in the text, including the confidence level
        '''
        return self._client._call('ParallelDots', 'getNamedEntities', { 'text': text })
    def get_sarcasm_probability(self, text: str) -> float:
        '''
        Compute the probability of sarcasm for the given text.
        
        :text: text to analyze
        
        :returns: predicted likelihood that the text is sarcastic
        '''
        res = self._client._call('ParallelDots', 'getSarcasmProbability', { 'text': text })
        return float(res)
    def get_sentiment(self, text: str) -> dict:
        '''
        Find the overall sentiment of the given text along with the confidence score.
        The returned structured data hasa confidence level for each of the following sentiment categories:
        negative, neutral, and positive.
        
        :text: text to analyze
        
        :returns: structured data with confidence level for each category
        '''
        res = self._client._call('ParallelDots', 'getSentiment', { 'text': text })
        return dict(res)
    def get_similarity(self, text1: str, text2: str) -> float:
        '''
        Get the level of similarity between two snippets of text.
        Note that the two pieces of text should be long, like full sentences (not just 2 words).
        
        :text1: the first piece of text
        
        :text2: a second piece of text
        
        :returns: the computed similarity level
        '''
        res = self._client._call('ParallelDots', 'getSimilarity', { 'text1': text1, 'text2': text2 })
        return float(res)
    def get_taxonomy(self, text: str) -> list:
        '''
        Classify the given text into IAB categories.
        
        For more information about IAB categories, see
        https://www.iab.com/guidelines/iab-quality-assurance-guidelines-qag-taxonomy/
        
        :text: text to analyze
        
        :returns: information about the category breakdown, along with confidence scores
        '''
        return self._client._call('ParallelDots', 'getTaxonomy', { 'text': text })
class PhoneIoT:
    '''
    PhoneIoT is a service in NetsBlox <https://netsblox.org/>_ that's meant to teach Internet of Things (IoT) topics as early as K-12 education.
    It allows you to programmatically access your smartphone's sensors and display.
    This includes accessing hardware sensors such as the accelerometer, gyroscope, microphone, camera, and many others depending on the device.
    PhoneIoT also allows you to control a customizable interactive display, enabling you to use your device as a custom remote control, or even create and run distributed (multiplayer) applications.
    The limits are up to your imagination!
    
    To get started using PhoneIoT, download the PhoneIoT app on your mobile device, available for Android <https://play.google.com/store/apps/details?id=org.netsblox.phoneiot>_ and iOS, and then go to the NetsBlox editor <https://editor.NetsBlox.org>_.
    In the top left of the editor, you should see a grid of several colored tabs.
    Under the Network tab, grab a call block and place it in the center script area.
    Click the first dropdown on the call block and select the PhoneIoT service.
    The second dropdown selects the specific *Remote Procedure Call* (RPC) to execute - see the table of contents  for information about the various RPCs.
    
    Inside the PhoneIoT app on your mobile device, click the button at the top left to open the menu, and then click connect.
    If you successfully connected, you should get a small popup message at the bottom of the screen.
    If you don't see this message, make sure you have either Wi-Fi or mobile data turned on and try again.
    Near the top of the menu, you should see an ID and password, which will be needed to connect to the device from NetsBlox.
    
    Back in NetsBlox, select the setCredentials RPC and give it your ID and password.
    For convenience, you might want to save the ID in a variable (e.g. device), as it will be referenced many times.
    If you click the call block to run it, you should get an OK result, meaning you successfully connected.
    If you don't see this, make sure you entered the ID and password correctly.
    
    You're now ready to start using the other RPCs in PhoneIoT to communicate with the device!
    '''
    def __init__(self, client):
        self._client = client
    def add_button(self, device: str, x: float, y: float, width: float, height: float, text: Optional[str] = None, options: Optional[dict] = None) -> str:
        '''
        Adds a button to the display with the given position and size.
        If not specified, the default text for a button is empty, which can be used to just make a colored, unlabeled button.
        The text can be modified later via PhoneIoT.setText.
        
        :device: id of the device
        
        :x: X position of the top left corner of the button (percentage)
        
        :y: Y position of the top left corner of the button (percentage)
        
        :width: Width of the button (percentage)
        
        :height: Height of the button (percentage)
        
        :text: text to display on the button (default empty)
        
        :options: Additional options
          - :id: (str) The id to use for the control. If not specified, a new one will be automatically generated.
          - :event: (str) The name of a message type to be sent each time the button is pressed. You must call PhoneIoT.listenToGUI to actually receive these messages. If not specified, no event is sent. Message fields: id.
          - :style: (str) The display style of the button on the screen. This can be rectangle (default), ellipse, square, or circle. If square or circle is used, the height of the control is ignored (height equals width).
          - :color: (int) The background color of the button.
          - :textColor: (int) The text color of the button.
          - :landscape: (bool) If set to true, rotates the button 90 degrees around its top left corner.
          - :fontSize: (float) The size of the font to use for text (default 1.0).
        
        :returns: id of the created control
        '''
        res = self._client._call('PhoneIoT', 'addButton', { 'device': device, 'x': x, 'y': y, 'width': width, 'height': height, 'text': text, 'options': options })
        return str(res)
    def add_image_display(self, device: str, x: float, y: float, width: float, height: float, options: Optional[dict] = None) -> str:
        '''
        Adds an image display wit hthe given position and size.
        If not specified, an image display is readonly, meaning that the user cannot modify its content.
        If (explicitly) not set to readonly, then the user can click on the image display to change the image to a new picture from the camera.
        
        :device: id of the device
        
        :x: X position of the top left corner of the image display (percentage).
        
        :y: Y position of the top left corner of the image display (percentage).
        
        :width: Width of the image display (percentage).
        
        :height: Height of the image display (percentage).
        
        :options: Additional options
          - :id: (str) The id to use for the control. If not specified, a new one will be automatically generated.
          - :event: (str) The name of a message type to be sent each time the user updates the content (only possible if readonly = false). You must call PhoneIoT.listenToGUI to actually receive these messages. If not specified, no event is sent. Message fields: id.
          - :readonly: (bool) Specifies if the user is allowed to change the content (defaults to true). Regardless of this setting, you can still modify the image programmatically via PhoneIoT.setImage. Defaults to true.
          - :landscape: (bool) If set to true, rotates the image display 90 degrees around its top left corner.
          - :fit: (str) The technique used to fit the image into the display, in case the image and the display have different aspect ratios. This can be fit (default), zoom, or stretch.
        
        :returns: id of the created control
        '''
        res = self._client._call('PhoneIoT', 'addImageDisplay', { 'device': device, 'x': x, 'y': y, 'width': width, 'height': height, 'options': options })
        return str(res)
    def add_joystick(self, device: str, x: float, y: float, width: float, options: Optional[dict] = None) -> str:
        '''
        Adds a joystick control to the canvas at the given position and size.
        No height parameter is given because joysticks are always circular (similar to passing style = circle to PhoneIoT.addButton).
        
        The position of the joystick is given by a vector [x, y], which is normalized to a length of 1.
        If you would prefer to not have this normalization and want rectangular coordinates instead of circular, consider using PhoneIoT.addTouchpad instead.
        
        :device: id of the device
        
        :x: X position of the top left corner of the joystick (percentage).
        
        :y: Y position of the top left corner of the joystick (percentage).
        
        :width: Width of the joystick (percentage).
        
        :options: Additional options
          - :id: (str) The id to use for the control. If not specified, a new one will be automatically generated.
          - :event: (str) The name of a message type to be sent each time the user moves the joystick. The messages also include a tag field which functions identically to the one in PhoneIoT.addTouchpad. You must call PhoneIoT.listenToGUI to actually receive these messages. If not specified, no event is sent. Message fields: id, x, y, tag.
          - :color: (int) The color of the joystick.
          - :landscape: (bool) If set to true, the x and y values of the joystick are altered so that it acts correctly when in landscape mode. Unlike other controls, this option does not affect where the control is displayed on the screen (no rotation).
        
        :returns: id of the created control
        '''
        res = self._client._call('PhoneIoT', 'addJoystick', { 'device': device, 'x': x, 'y': y, 'width': width, 'options': options })
        return str(res)
    def add_label(self, device: str, x: float, y: float, text: Optional[str] = None, options: Optional[dict] = None) -> str:
        '''
        Adds a label control to the canvas at the given position.
        If text is not specified, it default to empty, which can be used to hide the label when nothing needs to be displayed.
        The text can be modified later via PhoneIoT.setText.
        
        Labels do not have a size, so they also don't do text wrapping.
        Because of this, you should keep label text relatively short.
        If you need a large amount of text written, consider using PhoneIoT.addTextField with readonly = true.
        
        :device: id of the device
        
        :x: X position of the top left corner of the label (percentage).
        
        :y: Y position of the top left corner of the label (percentage).
        
        :text: The text to display on the label (defaults to empty)
        
        :options: Additional options
          - :id: (str) The id to use for the control. If not specified, a new one will be automatically generated.
          - :textColor: (int) The text color of the label.
          - :align: (str) The text alignment to use. If set to left, the text starts at the label position. If set to right, the text ends at the label position. If set to center, the text is centered on the label position.
          - :fontSize: (float) The size of the font to use for text (default 1.0).
          - :landscape: (bool) If set to true, rotates the label 90 degrees around the label position so the text appears upright when viewed in landscape.
        
        :returns: id of the created control
        '''
        res = self._client._call('PhoneIoT', 'addLabel', { 'device': device, 'x': x, 'y': y, 'text': text, 'options': options })
        return str(res)
    def add_radio_button(self, device: str, x: float, y: float, text: Optional[str] = None, options: Optional[dict] = None) -> str:
        '''
        Adds a radio button to the canvas.
        Radio buttons are like toggles (checkboxes), except that they are organized into groups
        and the user can check at most one radion button from any given group.
        These can be used to accept multiple-choice input from the user.
        
        :device: id of the device
        
        :x: X position of the top left corner of the radio button (percentage).
        
        :y: Y position of the top left corner of the radio button (percentage).
        
        :text: The text to display next to the checkbox (defaults to empty)
        
        :options: Additional options
          - :group: (str) The name of the group to associate this radio button with. You do not need this value to access the control later. If not specified, defaults to main.
          - :id: (str) The id to use for the control. If not specified, a new one will be automatically generated.
          - :event: (str) The name of an event to send every time the user clicks the radio button. Note that clicking a radio button always checks it, unlike toggles. You must call PhoneIoT.listenToGUI to actually receive these messages. If not specified, no event is sent. Message fields: id, state.
          - :checked: (bool) Defaults to false. If set to true, the radio button will be initially checked. Note that, while the user cannot check multiple radio buttons, you are free to do so programmatically.
          - :color: (int) The color of the radio button itself.
          - :textColor: (int) The text color of the radio button.
          - :fontSize: (float) The size of the font to use for text (default 1.0). Note that this will also scale up the size of the radio button itself (not just the text).
          - :landscape: (bool) If set to true, rotates the radio button 90 degrees around its top left corner.
          - :readonly: (bool) If set to true, prevents the user from clicking the radio button. However, you will still be free to update the state programmatically. Defaults to false.
        
        :returns: id of the created control
        '''
        res = self._client._call('PhoneIoT', 'addRadioButton', { 'device': device, 'x': x, 'y': y, 'text': text, 'options': options })
        return str(res)
    def add_slider(self, device: str, x: float, y: float, width: float, options: Optional[dict] = None) -> str:
        '''
        Adds a slider control to the display.
        Sliders can be moved around to input or display any value in the range [0, 1].
        If you need values outside of this range, you can do a little math to map them to [0, 1] or vice versa.
        
        You can read and write the value of a slider with PhoneIoT.getLevel and PhoneIoT.setLevel.
        Note that if the control is set to readonly, the user cannot change the value, but you can still do so from code.
        
        :device: id of the device
        
        :x: X position of the top left corner of the slider (percentage).
        
        :y: Y position of the top left corner of the slider (percentage).
        
        :width: Width (length) of the slider (percentage).
        
        :options: Additional options
          - :id: (str) The id to use for the control. If not specified, a new one will be automatically generated.
          - :event: (str) The name of a message type to be sent each time the user touches, slides, or lets go of the slider. The messages also include a tag field which functions identically to the one in PhoneIoT.addTouchpad. You must call PhoneIoT.listenToGUI to actually receive these messages. If not specified, no event is sent. Message fields: id, level, tag.
          - :color: (int) The color of the slider.
          - :value: (float) The initial value of the slider (default 0.0).
          - :style: (str) Controls the appearance of the slider. Allowed values are slider (default) or progress.
          - :landscape: (bool) true to rotate the control 90 degrees into landscape mode.
          - :readonly: (bool) true to disable the user from controlling the slider. This is especially usefull for progress bars.
        
        :returns: id of the created control
        '''
        res = self._client._call('PhoneIoT', 'addSlider', { 'device': device, 'x': x, 'y': y, 'width': width, 'options': options })
        return str(res)
    def add_text_field(self, device: str, x: float, y: float, width: float, height: float, options: Optional[dict] = None) -> str:
        '''
        Adds a text field to the canvas.
        These are typically used to display large blocks of text, or to accept input text from the user.
        If not set to readonly, the user can click on the text field to change its content.
        
        If you have a small amount of text you need to show and would otherwise make this control readonly, consider using PhoneIoT.addLabel instead.
        
        :device: id of the device
        
        :x: X position of the top left corner of the text field (percentage).
        
        :y: Y position of the top left corner of the text field (percentage).
        
        :width: Width of the text field (percentage).
        
        :height: Height of the text field (percentage).
        
        :options: Additional options
          - :id: (str) The id to use for the control. If not specified, a new one will be automatically generated.
          - :event: (str) The name of an event to send every time the user changes the text content (only possible if readonly = false). Note that this event is only sent once the user clicks accept on the new content (you do not get an event for every key press). You must call PhoneIoT.listenToGUI to actually receive these messages. If not specified, no event is sent. Message fields: id, text.
          - :text: (str) This can be used to set the initial text of the text field once created. Defaults to empty if not specified.
          - :color: (int) The color of the text field border.
          - :textColor: (int) The text color of the text field.
          - :readonly: (bool) If set to true, the user will not be able to edit the content. However, you will still be free to do so programmatically. Defaults to false.
          - :fontSize: (float) The size of the font to use for text (default 1.0).
          - :align: (str) The text alignment to use. This can be left (default), right, or center.
          - :landscape: (bool) If set to true, rotates the text field 90 degrees around its top left corner.
        
        :returns: id of the created control
        '''
        res = self._client._call('PhoneIoT', 'addTextField', { 'device': device, 'x': x, 'y': y, 'width': width, 'height': height, 'options': options })
        return str(res)
    def add_toggle(self, device: str, x: float, y: float, text: Optional[str] = None, options: Optional[dict] = None) -> str:
        '''
        Adds a toggle control to the canvas at the given location.
        The text parameter can be used to set the initial text shown for the toggle (defaults to empty),
        but this can be changed later with PhoneIoT.setText.
        
        :device: id of the device
        
        :x: X position of the top left corner of the toggle (percentage).
        
        :y: Y position of the top left corner of the toggle (percentage).
        
        :text: The text to display next to the toggle (defaults to empty)
        
        :options: Additional options
          - :style: (str) The visual style of the toggle control. This can be switch (default) for a mobile-style toggle, or checkbox for a desktop-style toggle.
          - :id: (str) The id to use for the control. If not specified, a new one will be automatically generated.
          - :event: (str) The name of a message to be sent every time the checkbox is toggled by the user. You must call PhoneIoT.listenToGUI to actually receive these messages. Message fields: id, state.
          - :checked: (bool) Defaults to false. If set to true, the toggle will be initially checked.
          - :color: (int) The color of the toggle itself.
          - :textColor: (int) The text color of the toggle.
          - :fontSize: (float) The size of the font to use for text (default 1.0). Note that this will also scale up the size of the toggle itself (not just the text).
          - :landscape: (bool) If set to true, rotates the toggle 90 degrees around its top left corner.
          - :readonly: (bool) If set to true, prevents the user from clicking the toggle. However, you will still be free to update the state programmatically. Defaults to false.
        
        :returns: id of the created control
        '''
        res = self._client._call('PhoneIoT', 'addToggle', { 'device': device, 'x': x, 'y': y, 'text': text, 'options': options })
        return str(res)
    def add_touchpad(self, device: str, x: float, y: float, width: float, height: float, options: Optional[dict] = None) -> str:
        '''
        Adds a touchpad control to the canvas at the given position and size.
        This control is similar to the joystick control, except that it is rectangular,
        the vector is not normalized to a distance of 1,
        the "stick" does not move back to (0, 0) upon letting go,
        and there is an additional "tag" value denoting if each event was a touch down, move, or up.
        
        Although the vector value is not normalized to a length of 1,
        each component (x and y individually) is in [-1, 1].
        
        :device: id of the device
        
        :x: X position of the top left corner of the touchpad (percentage).
        
        :y: Y position of the top left corner of the touchpad (percentage).
        
        :width: Width of the touchpad (percentage).
        
        :height: Height of the touchpad (percentage).
        
        :options: Additional options
          - :id: (str) The id to use for the control. If not specified, a new one will be automatically generated.
          - :event: (str) The name of a message type to be sent each time the user touches, slides, or lets go of the touchpad. A message field called tag is included to differentiate the different types of interactions; it is one of down (touch started), up (touch ended), or move (during continued/held touch). You must call PhoneIoT.listenToGUI to actually receive these messages. If not specified, no event is sent. Message fields: id, x, y, tag.
          - :color: (int) The color of the touchpad.
          - :style: (str) Controls the appearance of the touchpad. These are the same as for PhoneIoT.addButton except that only rectangle and square are allowed.
          - :landscape: (bool) true to rotate the control 90 degrees into landscape mode.
        
        :returns: id of the created control
        '''
        res = self._client._call('PhoneIoT', 'addTouchpad', { 'device': device, 'x': x, 'y': y, 'width': width, 'height': height, 'options': options })
        return str(res)
    def authenticate(self, device: str):
        '''
        This RPC simply checks that the connection to the device is still good.
        In particular, you can use this to check if the password is still valid.
        
        :device: id of the device
        '''
        return self._client._call('PhoneIoT', 'authenticate', { 'device': device })
    def clear_controls(self, device: str):
        '''
        Removes all controls from the device's canvas.
        If you would instead like to remove a specific control, see PhoneIoT.removeControl.
        
        :device: id of the device
        '''
        return self._client._call('PhoneIoT', 'clearControls', { 'device': device })
    def get_accelerometer(self, device: str) -> list:
        '''
        Gets the current output of the accelerometer sensor, if the device supports it.
        This is a vector representing the acceleration along the x, y, and z axes, relative to the device.
        When at rest, you can expect to measure the acceleration due to gravity.
        
        Sensor name: accelerometer
        
        Message fields: x, y, z, facingDir, device
        
        :device: id of the device
        
        :returns: current acceleration vector
        '''
        return self._client._call('PhoneIoT', 'getAccelerometer', { 'device': device })
    def get_altitude(self, device: str) -> float:
        '''
        Returns the current altitude of the device, expressed in meters above sea level.
        This is provided by the location service on the device, so you must have location turned on and give the app permission.
        
        Sensor name: location
        
        Message fields: latitude, longitude, bearing, altitude, device
        
        :device: id of the device
        
        :returns: current altitude in meters
        '''
        res = self._client._call('PhoneIoT', 'getAltitude', { 'device': device })
        return float(res)
    def get_bearing(self, device: str) -> float:
        '''
        Returns the current bearing (direction of travel) from the device.
        This is provided by the location sensor, so you must have location turned on and give the app permission.
        The bearing is expressed as the angle (in degrees) from North, going clockwise.
        Thus, you can directly use this value in a point in direction block to point a sprite in the direction of travel (assuming North is up).
        
        Sensor name: location
        
        Message fields: latitude, longitude, bearing, altitude, device
        
        :device: id of the device
        
        :returns: current bearing (in degrees)
        '''
        res = self._client._call('PhoneIoT', 'getBearing', { 'device': device })
        return float(res)
    def get_color(self, red: int, green: int, blue: int, alpha: Optional[int] = None) -> int:
        '''
        Many of the Display RPCs take one or more optional parameters for controlling display color, which is specified as an integer.
        This RPC is a convenience function for constructing a color code from red, green, blue, and alpha values (each is 0-255).
        
        The alpha value controls transparency, with 0 being invisible and 255 being opaque.
        If not specified, alpha will default to 255.
        
        :red: red level (0-255)
        
        :green: green level (0-255)
        
        :blue: blue level (0-255)
        
        :alpha: alpha level (0-255)
        
        :returns: Constructed color code (an integer)
        '''
        res = self._client._call('PhoneIoT', 'getColor', { 'red': red, 'green': green, 'blue': blue, 'alpha': alpha })
        return int(res)
    def get_compass_cardinal_direction(self, device: str) -> str:
        '''
        Equivalent to PhoneIoT.getCompassDirection, except that it only returns N, E, S, or W.
        
        If you are getting inconsistent values, try moving and rotating your device around in a figure-8 to recalibrate it.
        
        Sensor name: orientation
        
        Message fields: x, y, z, heading, dir, cardinalDir, device
        
        :device: id of the device
        
        :returns: the compass cardinal direction name
        '''
        res = self._client._call('PhoneIoT', 'getCompassCardinalDirection', { 'device': device })
        return str(res)
    def get_compass_direction(self, device: str) -> str:
        '''
        Returns the current compass direction of the device, which is one of N, NE, E, SE, S, SW, W, or NW.
        This is provided by the magnetic field sensor, so using this RPC on devices without a magnetometer will result in an error.
        The output of this RPC assumes the device is face-up.
        
        If you are getting inconsistent values, try moving and rotating your device around in a figure-8 to recalibrate it.
        
        Sensor name: orientation
        
        Message fields: x, y, z, heading, dir, cardinalDir, device
        
        :device: id of the device
        
        :returns: the current compass direction name
        '''
        res = self._client._call('PhoneIoT', 'getCompassDirection', { 'device': device })
        return str(res)
    def get_compass_heading(self, device: str) -> float:
        '''
        Gets the current compass heading from the device. This is similar to PhoneIoT.getBearing, except that it returns the angle from magnetic north, rather than the direction of travel.
        This is provided by the magnetic field sensor, so using this RPC on devices without a magnetometer will result in an error.
        The output of this RPC assumes the device is face-up.
        
        If you are getting inconsistent values, try moving and rotating your device around in a figure-8 to recalibrate it.
        
        Sensor name: orientation
        
        Message fields: x, y, z, heading, dir, cardinalDir, device
        
        :device: id of the device
        
        :returns: the compass heading (in degrees)
        '''
        res = self._client._call('PhoneIoT', 'getCompassHeading', { 'device': device })
        return float(res)
    def get_facing_direction(self, device: str) -> str:
        '''
        Attempts to determine the general orientation of the device based on the accelerometer output.
        This represents which direction the face of the device's screen is pointing.
        The possible values are:
        
        - up - the device is face up
        - down - the device is face down
        - vertical - the device is upright
        - upside down - the device is vertical, but upside down
        - left - the device is horizontal, lying on its left side (when facing the screen)
        - right - the device is horizontal, lying on its right side (when facing the screen)
        
        Sensor name: accelerometer
        
        Message fields: x, y, z, facingDir, device
        
        :device: id of the device
        
        :returns: name of the facing direction
        '''
        res = self._client._call('PhoneIoT', 'getFacingDirection', { 'device': device })
        return str(res)
    def get_gravity(self, device: str) -> list:
        '''
        Attempts to get the gravity acceleration angle, divorced from any linear acceleration the device might be experiencing.
        For example, even if you start running, this vector should always have roughly the same value.
        This is provided by a hybrid sensor, and is not available on all devices.
        
        The counterpart to this RPC is PhoneIoT.getLinearAcceleration.
        
        Sensor name: gravity
        
        Message fields: x, y, z, device
        
        :device: id of the device
        
        :returns: gravitational acceleration vector
        '''
        return self._client._call('PhoneIoT', 'getGravity', { 'device': device })
    def get_gyroscope(self, device: str) -> list:
        '''
        Gets the current output of the gyroscope sensor, which measures rotational acceleration (in degress/s²) along the three axes of the device.
        
        Sensor name: gyroscope
        
        Message fields: x, y, z, device
        
        :device: id of the device
        
        :returns: rotational acceleration vector
        '''
        return self._client._call('PhoneIoT', 'getGyroscope', { 'device': device })
    def get_image(self, device: str, id: str) -> dict:
        '''
        Gets the displayed image of an image-like control with the given ID.
        This can be used on any control that displays images, which is currently only image displays.
        
        This can be used to retrieve images from the mobile device's camera, by having the user store an image in an image display that has readonly = false.
        See the readonly optional parameter of PhoneIoT.addImageDisplay.
        
        :device: id of the device
        
        :id: id of the image display
        
        :returns: the displayed image
        '''
        res = self._client._call('PhoneIoT', 'getImage', { 'device': device, 'id': id })
        return dict(res)
    def get_level(self, device: str, id: str) -> float:
        '''
        Get the current value (a single number) of a value-like control.
        Currently, the only supported control is a slider, which returns a value in [0, 1].
        
        Instead of calling this in a loop, it is likely better to use the event optional parameter of PhoneIoT.addSlider.
        
        If you want to get the cursor position of a joystick or touchpad, use PhoneIoT.getPosition instead.
        
        :device: id of the device
        
        :id: id of the control to read
        
        :returns: current value
        '''
        res = self._client._call('PhoneIoT', 'getLevel', { 'device': device, 'id': id })
        return float(res)
    def get_light_level(self, device: str) -> float:
        '''
        Gets the current light level from the device.
        This is represented as a number with higher values being brighter.
        
        Sensor name: lightLevel
        
        Message fields: value, device
        
        :device: id of the device
        
        :returns: current light level
        '''
        res = self._client._call('PhoneIoT', 'getLightLevel', { 'device': device })
        return float(res)
    def get_linear_acceleration(self, device: str) -> list:
        '''
        This RPC attempts to get the linear acceleration vector, divorced from the constant gravitational acceleration.
        Theoretically, if the device is at rest this RPC would report a nearly-zero vector (nothing is ever perfectly still).
        This is provided by a hybrid sensor, and is not available on all devices.
        
        The counterpart to this RPC is PhoneIoT.getGravity.
        
        Sensor name: linearAcceleration
        
        Message fields: x, y, z, device
        
        :device: id of the device
        
        :returns: current linear acceleration vector
        '''
        return self._client._call('PhoneIoT', 'getLinearAcceleration', { 'device': device })
    def get_location(self, device: str) -> list:
        '''
        Gets the current location of the device, specified as latitude and longitude coordinates (in degrees).
        This is provided by the location service on the device, so you must have location turned on and give the app permission.
        
        Sensor name: location
        
        Message fields: latitude, longitude, bearing, altitude, device
        
        :device: id of the device
        
        :returns: a list containing the latitude and longitude
        '''
        return self._client._call('PhoneIoT', 'getLocation', { 'device': device })
    def get_magnetic_field(self, device: str) -> list:
        '''
        Gets the current ouput of the magnetic field sensor, measured in μT (micro Tesla) along each axis of the device.
        This is provided by the magnetic field sensor, so using this RPC on devices without a magnetometer will result in an error.
        
        Notably, this RPC can be used as a compass (measuring Earth's magnetic field).
        
        Sensor name: magneticField
        
        Message fields: x, y, z, device
        
        :device: id of the device
        
        :returns: magnetic field vector
        '''
        return self._client._call('PhoneIoT', 'getMagneticField', { 'device': device })
    def get_microphone_level(self, device: str) -> list:
        '''
        Gets the current level (volume) of the microphone on the device.
        This is specified as a number where 0.0 denotes silence and 1.0 is the maximum volume the microphone can record.
        
        Sensor name: microphoneLevel
        
        Message fields: volume, device
        
        :device: id of the device
        
        :returns: the current volume level
        '''
        return self._client._call('PhoneIoT', 'getMicrophoneLevel', { 'device': device })
    def get_orientation(self, device: str) -> list:
        '''
        Gets the current output of the orientation sensor, relative to Earth's magnetic reference frame.
        This is given as a vector (list) with three angular components (in degrees):
        
        - azimuth (effectively the compass heading) [-180, 180]
        - pitch (vertical tilt) [-90, 90]
        - roll [-180, 180]
        
        If you are getting inconsistent values for the first (azimuth) angle,
        try moving and rotating your device around in a figure-8 to recalibrate it.
        
        Sensor name: orientation
        
        Message fields: x, y, z, heading, dir, cardinalDir, device
        
        :device: id of the device
        
        :returns: the current orientation vector
        '''
        return self._client._call('PhoneIoT', 'getOrientation', { 'device': device })
    def get_position(self, device: str, id: str) -> list:
        '''
        Gets the current x and y values for the current position of a positional control.
        This does *not* give the location of the control on the screen.
        Positional controls are controls whose primary interaction is through position.
        For instance, this is used for both joystick and touchpad controls.
        
        For a joystick, this always returns a vector normalized to a length of 1.0.
        If the user is not touching the joystick, it will automatically go back to the center, [0, 0].
        
        For a touchpad, this will either give you the current location of the touch (a list of [x, y])
        or an error if the user is not touching the screen.
        
        If you want to get the value of a slider, use PhoneIoT.getLevel instead.
        
        Instead of calling this in a loop, it is likely better to use the event optional parameter of
        PhoneIoT.addJoystick or PhoneIoT.addTouchpad.
        
        :device: id of the device
        
        :id: id of the control to read
        
        :returns: a list of [x, y] for the current position, or a string explaining that there is no current position
        '''
        return self._client._call('PhoneIoT', 'getPosition', { 'device': device, 'id': id })
    def get_proximity(self, device: str) -> float:
        '''
        Gets the current output of the proximity (distance) sensor, measured in cm.
        Phones typically have this sensor for turning off the display when you put it to your ear, but tablets typically do not.
        In any case, the distances are not typically very long, and some devices only have binary (near/far) sensors.
        
        Sensor name: proximity
        
        Message fields: distance, device
        
        :device: id of the device
        
        :returns: current proximity sensor output
        '''
        res = self._client._call('PhoneIoT', 'getProximity', { 'device': device })
        return float(res)
    def get_sensors(self) -> list:
        '''
        This RPC returns a list containing the name of every sensor supported by PhoneIoT.
        Note that your specific device might not support all of these sensors, depending on the model.
        
        See Sensors for more information.
        
        :returns: A list of sensor names
        '''
        return self._client._call('PhoneIoT', 'getSensors', {  })
    def get_step_count(self, device: str) -> float:
        '''
        Gets the current step count from the device's step counter sensor.
        Not all devices have a step counter sensor, but you can manually emulate one by using the accelerometer.
        
        Sensor name: stepCount
        
        Message fields: count, device
        
        :device: id of the device
        
        :returns: current step count
        '''
        res = self._client._call('PhoneIoT', 'getStepCount', { 'device': device })
        return float(res)
    def get_text(self, device: str, id: str) -> str:
        '''
        Gets the current text content of the text-like control with the given ID.
        This can be used on any control that has text, such as a button, label, or text field.
        
        :device: id of the device
        
        :id: id of the control to read
        
        :returns: currently displayed text
        '''
        res = self._client._call('PhoneIoT', 'getText', { 'device': device, 'id': id })
        return str(res)
    def get_toggle_state(self, device: str, id: str) -> bool:
        '''
        Gets the toggle state of a toggleable control.
        This can be used on any toggleable control, such as toggles and radio buttons.
        
        :device: id of the device
        
        :id: id of the control to read
        
        :returns: true for checked, otherwise false
        '''
        res = self._client._call('PhoneIoT', 'getToggleState', { 'device': device, 'id': id })
        return bool(res)
    def is_pressed(self, device: str, id: str) -> bool:
        '''
        Checks if the pressable control with the given ID is currently pressed.
        This can be used on any pressable control, which currently includes buttons, joysticks, and touchpads.
        
        By calling this RPC in a loop, you could perform some action every second while a button is held down.
        If you would instead like to receive click events, see the event optional parameter of PhoneIoT.addButton.
        
        :device: id of the device
        
        :id: id of the control to read
        
        :returns: true for pressed, otherwise false
        '''
        res = self._client._call('PhoneIoT', 'isPressed', { 'device': device, 'id': id })
        return bool(res)
    def listen_to_gui(self, device: str):
        '''
        This RPC requests that you receive any events from the *Graphical User Interface* (GUI) on the phone's display.
        This is needed to receive any type of GUI event, including button clicks, joystick movements, and textbox update events.
        You only need to call this RPC once, which you can do at the start of your program (but after calling PhoneIoT.setCredentials).
        
        See the Display section for more information.
        
        :device: id of the device
        '''
        return self._client._call('PhoneIoT', 'listenToGUI', { 'device': device })
    def listen_to_sensors(self, device: str, sensors: Optional[dict] = None):
        '''
        This RPC requests that you receive periodic sensor update events from the device.
        The sensors input is a list of pairs (lists of length 2), where each pair is a sensor name and an update period in milliseconds.
        You can have different update periods for different sensors.
        You will receive a message of the same name as the sensor at most once per whatever update period you specified.
        Any call to this RPC will invalidate all previous calls - thus, calling it with an empty list will stop all updates.
        
        This method of accessing sensor data is often easier, as it doesn't require loops or error-checking code.
        If a networking error occurs, you simply miss that single message.
        
        The PhoneIoT.getSensors RPC can be used to get a list of the valid sensor names.
        See the Sensors section for more information, esp. the required fields for each message type.
        
        :device: id of the device
        
        :sensors: structured data representing the minimum time in milliseconds between updates for each sensor type to listen for
          - :gravity: (float) gravity period
          - :gyroscope: (float) gyroscope period
          - :orientation: (float) orientation period
          - :accelerometer: (float) accelerometer period
          - :magneticField: (float) magneticField period
          - :rotation: (float) rotation period
          - :linearAcceleration: (float) linearAcceleration period
          - :gameRotation: (float) gameRotation sensor period
          - :lightLevel: (float) lightLevel period
          - :microphoneLevel: (float) microphoneLevel period
          - :proximity: (float) proximity period
          - :stepCount: (float) stepCount period
          - :location: (float) location period
        '''
        return self._client._call('PhoneIoT', 'listenToSensors', { 'device': device, 'sensors': sensors })
    def magnitude(self, vec: List[float]) -> float:
        '''
        Given a list of numbers representing a vector, this RPC returns the magnitude (length) of the vector.
        This can be used to get the total acceleration from the accelerometer (which gives a vector).
        
        :vec: the vector value
        
        :returns: magnitude of the vector (a non-negative number)
        '''
        res = self._client._call('PhoneIoT', 'magnitude', { 'vec': vec })
        return float(res)
    def normalize(self, vec: List[float]) -> List[float]:
        '''
        Given a list of numbers representing a vector, returns the normalized vector (same direction but with a magnitude of 1.0).
        This is identical to dividing each component by the magnitude.
        
        :vec: the vector value
        
        :returns: the normalized vector
        '''
        res = self._client._call('PhoneIoT', 'normalize', { 'vec': vec })
        return _common.vectorize(float)(res)
    def remove_control(self, device: str, id: str):
        '''
        Removes a control with the given ID if it exists.
        If the control does not exist, does nothing (but still counts as success).
        If you would instead like to remove all controls, see PhoneIoT.clearControls.
        
        :device: id of the device
        
        :id: id of the control to remove
        '''
        return self._client._call('PhoneIoT', 'removeControl', { 'device': device, 'id': id })
    def set_credentials(self, device: str, password: str):
        '''
        This is the first RPC you should *always* call when working with PhoneIoT.
        It sets the login credentials (password) to use for all future interactions with the device.
        
        :device: id of the device
        
        :password: the password to use for accessing the device
        '''
        return self._client._call('PhoneIoT', 'setCredentials', { 'device': device, 'password': password })
    def set_image(self, device: str, id: str, img: Any):
        '''
        Sets the displayed image of an image-like control with the given ID.
        This can be used on any control that displays images, which is currently only image displays.
        
        :device: id of the device
        
        :id: the id of the control to modify
        
        :img: the new image to display
        '''
        return self._client._call('PhoneIoT', 'setImage', { 'device': device, 'id': id, 'img': img })
    def set_level(self, device: str, id: str, value: float) -> float:
        '''
        Set the current value (a single number) of a value-like control.
        Currently, the only supported control is a slider, which sets the displayed value.
        
        Note that you can use this RPC even if the control is set to readonly mode (it's only readonly to the user).
        
        :device: id of the device
        
        :id: id of the control to read
        
        :value: new value to set
        
        :returns: current value
        '''
        res = self._client._call('PhoneIoT', 'setLevel', { 'device': device, 'id': id, 'value': value })
        return float(res)
    def set_text(self, device: str, id: str, text: Optional[str] = None):
        '''
        Sets the text content of the text-like control with the given ID.
        This can be used on any control that has text, such as a button, label, or text field.
        
        :device: id of the device
        
        :id: id of the control to modify
        
        :text: The new text to display (defaults to empty)
        '''
        return self._client._call('PhoneIoT', 'setText', { 'device': device, 'id': id, 'text': text })
    def set_toggle_state(self, device: str, id: str, state: bool):
        '''
        Sets the toggle state of a toggleable control with the given ID.
        This can be used on any toggleable control, such as toggles and radio buttons.
        If state is true, the toggleable becomes checked, otherwise it is unchecked.
        
        If used on a radio button, it sets the state independent of the control's group.
        That is, although the user can't select multiple radio buttons in the same group, you can do so programmatically through this RPC.
        
        :device: id of the device
        
        :id: id of the control to modify
        
        :state: new value for the toggle state
        '''
        return self._client._call('PhoneIoT', 'setToggleState', { 'device': device, 'id': id, 'state': state })
class ProjectGutenberg:
    '''
    The Project Gutenberg service provides access to public domain books. For more information, check out https://project-gutenberg.org/.
    '''
    def __init__(self, client):
        self._client = client
    def get_info(self, id: str) -> list:
        '''
        Get information about a given book including title and author.
        
        :id: Book ID
        
        :returns: 
        '''
        return self._client._call('ProjectGutenberg', 'getInfo', { 'ID': id })
    def get_text(self, id: str) -> str:
        '''
        Get the URL for the full text of a given book.
        
        :id: Book ID
        
        :returns: 
        '''
        res = self._client._call('ProjectGutenberg', 'getText', { 'ID': id })
        return str(res)
    def search(self, field: str, text: str) -> List[str]:
        '''
        Search for a book given title text and optional advanced options. Returns a list of up to 100 book IDs.
        
        :field: 
        
        :text: 
        
        :returns: 
        '''
        res = self._client._call('ProjectGutenberg', 'search', { 'field': field, 'text': text })
        return _common.vectorize(str)(res)
class PublicRoles:
    '''
    The PublicRoles Service provides access to the user's public role
    ID programmatically. This enables communication between projects.
    '''
    def __init__(self, client):
        self._client = client
    def get_public_role_id(self) -> str:
        '''
        Get the public role ID for the current role.
        
        :returns: the public role id
        '''
        res = self._client._call('PublicRoles', 'getPublicRoleId', {  })
        return str(res)
class RoboScape:
    
    def __init__(self, client):
        self._client = client
    def beep(self, robot: str, msec: float, tone: float) -> bool:
        '''
        Beeps with the speaker.
        
        :robot: name of the robot (matches at the end)
        
        :msec: duration in milliseconds
        
        :tone: frequency of the beep in Hz
        
        :returns: true if the robot was found
        '''
        res = self._client._call('RoboScape', 'beep', { 'robot': robot, 'msec': msec, 'tone': tone })
        return bool(res)
    def drive(self, robot: str, left: float, right: float) -> bool:
        '''
        Drives the whiles for the specified ticks.
        
        :robot: name of the robot (matches at the end)
        
        :left: distance for left wheel in ticks
        
        :right: distance for right wheel in ticks
        
        :returns: true if the robot was found
        '''
        res = self._client._call('RoboScape', 'drive', { 'robot': robot, 'left': left, 'right': right })
        return bool(res)
    def get_range(self, robot: str) -> float:
        '''
        Ranges with the ultrasound sensor
        
        :robot: name of the robot (matches at the end)
        
        :returns: range in centimeters
        '''
        res = self._client._call('RoboScape', 'getRange', { 'robot': robot })
        return float(res)
    def get_robots(self) -> list:
        '''
        Returns the MAC addresses of all authorized robots.
        
        :returns: 
        '''
        return self._client._call('RoboScape', 'getRobots', {  })
    def get_ticks(self, robot: str) -> list:
        '''
        Returns the current number of wheel ticks (1/64th rotations)
        
        :robot: name of the robot (matches at the end)
        
        :returns: the number of ticks for the left and right wheels
        '''
        return self._client._call('RoboScape', 'getTicks', { 'robot': robot })
    def infra_light(self, robot: str, msec: float, pwr: float) -> bool:
        '''
        Turns on the infra red LED.
        
        :robot: name of the robot (matches at the end)
        
        :msec: duration in milliseconds
        
        :pwr: power level
        
        :returns: true if the robot was found
        '''
        res = self._client._call('RoboScape', 'infraLight', { 'robot': robot, 'msec': msec, 'pwr': pwr })
        return bool(res)
    def is_alive(self, robot: str) -> bool:
        '''
        Returns true if the given robot is alive, sent messages in the
        last two seconds.
        
        :robot: name of the robot (matches at the end)
        
        :returns: true if the robot is alive
        '''
        res = self._client._call('RoboScape', 'isAlive', { 'robot': robot })
        return bool(res)
    def listen(self, robots: list):
        '''
        Registers for receiving messages from the given robots.
        
        :robots: one or a list of robots
        '''
        return self._client._call('RoboScape', 'listen', { 'robots': robots })
    def send(self, robot: str, command: str) -> str:
        '''
        Sends a textual command to the robot
        
        :robot: name of the robot (matches at the end)
        
        :command: textual command
        
        :returns: textual response
        '''
        res = self._client._call('RoboScape', 'send', { 'robot': robot, 'command': command })
        return str(res)
    def set_client_rate(self, robot: str, rate: float, penalty: float) -> bool:
        '''
        Sets the client message limit and penalty for the given robot.
        
        :robot: name of the robot (matches at the end)
        
        :rate: number of messages per seconds
        
        :penalty: number seconds of penalty if rate is violated
        
        :returns: true if the robot was found
        '''
        res = self._client._call('RoboScape', 'setClientRate', { 'robot': robot, 'rate': rate, 'penalty': penalty })
        return bool(res)
    def set_led(self, robot: str, led: float, command: float) -> bool:
        '''
        Sets one of the LEDs of the given robots.
        
        :robot: name of the robot (matches at the end)
        
        :led: the number of the LED (0 or 1)
        
        :command: false/off/0, true/on/1, or toggle/2
        
        :returns: true if the robot was found
        '''
        res = self._client._call('RoboScape', 'setLed', { 'robot': robot, 'led': led, 'command': command })
        return bool(res)
    def set_speed(self, robot: str, left: float, right: float) -> bool:
        '''
        Sets the wheel speed of the given robots.
        
        :robot: name of the robot (matches at the end)
        
        :left: speed of the left wheel in [-128, 128]
        
        :right: speed of the right wheel in [-128, 128]
        
        :returns: true if the robot was found
        '''
        res = self._client._call('RoboScape', 'setSpeed', { 'robot': robot, 'left': left, 'right': right })
        return bool(res)
    def set_total_rate(self, robot: str, rate: float) -> bool:
        '''
        Sets the total message limit for the given robot.
        
        :robot: name of the robot (matches at the end)
        
        :rate: number of messages per seconds
        
        :returns: true if the robot was found
        '''
        res = self._client._call('RoboScape', 'setTotalRate', { 'robot': robot, 'rate': rate })
        return bool(res)
class ServiceCreation:
    '''
    The ServiceCreation Service enables users to create custom services. Custom
    Services can be found under the "Community" section using the call <RPC>
    block.
    '''
    def __init__(self, client):
        self._client = client
    def create_service_from_table(self, name: str, data: list, options: Optional[dict] = None):
        '''
        Create a service using a given dataset.
        
        :name: Service name
        
        :data: 2D list of data
        
        :options: Options (for details, check out ServiceCreation.getCreateFromTableOptions)
        '''
        return self._client._call('ServiceCreation', 'createServiceFromTable', { 'name': name, 'data': data, 'options': options })
    def delete_service(self, name: str):
        '''
        Delete an existing service.
        
        :name: Service name
        '''
        return self._client._call('ServiceCreation', 'deleteService', { 'name': name })
    def get_create_from_table_options(self, data: list):
        '''
        Get the default settings for a given dataset.
        
        :data: 2D list of data
        '''
        return self._client._call('ServiceCreation', 'getCreateFromTableOptions', { 'data': data })
class SimpleHangman:
    '''
    The SimpleHangman Service provides RPCs for playing single player hangman.
    The service will choose a word for the player to guess using the given RPCs.
    '''
    def __init__(self, client):
        self._client = client
    def get_currently_known_word(self) -> str:
        '''
        Get the current word with where unknown letters are replaced with "_".
        
        :returns: current word with blanks
        '''
        res = self._client._call('SimpleHangman', 'getCurrentlyKnownWord', {  })
        return str(res)
    def get_wrong_count(self) -> int:
        '''
        Get the current number of incorrect guesses.
        
        :returns: number of wrong guesses
        '''
        res = self._client._call('SimpleHangman', 'getWrongCount', {  })
        return int(res)
    def guess(self, letter: str):
        '''
        Guess a letter in the current word.
        
        :letter: 
        '''
        return self._client._call('SimpleHangman', 'guess', { 'letter': letter })
    def is_word_guessed(self) -> bool:
        '''
        Check if the current word has been guessed correctly.
        
        :returns: true if word was guessed correctly
        '''
        res = self._client._call('SimpleHangman', 'isWordGuessed', {  })
        return bool(res)
    def restart(self, word: Optional[str] = None) -> bool:
        '''
        Restart the current game.
        
        :word: New word to guess
        
        :returns: true on successful restart
        '''
        res = self._client._call('SimpleHangman', 'restart', { 'word': word })
        return bool(res)
class Smithsonian:
    '''
    The Smithsonian Service provides access to the Smithsonan open-access EDAN database,
    containing catalogued information on millions of historical items.
    '''
    def __init__(self, client):
        self._client = client
    def get_image(self, id: str) -> Any:
        '''
        Get an image associated with the given object, if available.
        This requires the id of the object, as provided by Smithsonian.search or Smithsonian.searchImageContent.
        
        :id: id of the object
        
        :returns: an image of the object
        '''
        return self._client._call('Smithsonian', 'getImage', { 'id': id })
    def search(self, term: str, count: Optional[float] = None, skip: Optional[float] = None) -> list:
        '''
        Search and return a list of up to count items that match the search term.
        Because there may be a large number of matching items, you can also provide a number of items to skip.
        
        Each item in the returned array is structured data about that matching item.
        The fields for this data include:
        
        - id - the id of the matching item, needed by Smithsonian.getImage.
        - title - the title/name of the matching item
        - types - a list of categories the item falls under (e.g., Vases, Paintings)
        - authors - a list of authors/creators of the item or digitized version
        - topics - a list of topic names for the item (e.g., Anthropology, Ethnology)
        - notes - a list of extra notes about the object, in no particular organization
        - physicalDescription - a list of pairs of [label, content] regarding the physical description of the object
        - sources - a list of pairs of [label, content] describing the source of the item or digitization
        - hasImage - true if the image is listed as having image content in the database. Only items with this field being true can expect Smithsonian.getImage to succeed.
        
        If you would like to search for only items which have image content available,
        you can perform manual filtering on the hasImage field of the results,
        or you can use Smithsonian.searchImageContent, which does the same thing for you.
        
        :term: Term to search for
        
        :count: Maximum number of items to return (default 100)
        
        :skip: Number of items to skip from beginning
        
        :returns: Up to count matches
        '''
        return self._client._call('Smithsonian', 'search', { 'term': term, 'count': count, 'skip': skip })
    def search_image_content(self, term: str, count: Optional[float] = None, skip: Optional[float] = None) -> list:
        '''
        Equivalent to Smithsonian.search except that only images with image content (hasImage = true) are returned.
        
        The filtering of returned matches is done after pulling data from the database.
        Thus, you should treat count as the max number of *unfiltered* items to return,
        and similarly skip as the number of *unfiltered* items to skip.
        
        :term: Term to search for
        
        :count: Maximum number of items to return
        
        :skip: Number of items to skip from beginning
        
        :returns: Up to count matches
        '''
        return self._client._call('Smithsonian', 'searchImageContent', { 'term': term, 'count': count, 'skip': skip })
class StarMap:
    '''
    The StarMap Service provides access to astronomy data using Sloan Digital Sky Survey.
    For more information, check out http://skyserver.sdss.org/dr14/en/home.aspx
    '''
    def __init__(self, client):
        self._client = client
    def arc_hour_min_sec_to_deg(self, arc_hour: float, arc_min: float, arc_sec: float):
        '''
        Convert arc to degree.
        
        :arc_hour: 
        
        :arc_min: 
        
        :arc_sec: 
        '''
        return self._client._call('StarMap', 'arcHourMinSecToDeg', { 'arcHour': arc_hour, 'arcMin': arc_min, 'arcSec': arc_sec })
    def find_object(self, name: str):
        '''
        Search for significant object in the sky.
        
        :name: 
        '''
        return self._client._call('StarMap', 'findObject', { 'name': name })
    def get_image(self, right_ascension: float, declination: float, arcseconds_per_pixel: float, options: str, width: Optional[float] = None, height: Optional[float] = None):
        '''
        Get an image of the sky at the given coordinates.
        
        :right_ascension: 
        
        :declination: 
        
        :arcseconds_per_pixel: 
        
        :options: 
        
        :width: 
        
        :height: 
        '''
        return self._client._call('StarMap', 'getImage', { 'right_ascension': right_ascension, 'declination': declination, 'arcseconds_per_pixel': arcseconds_per_pixel, 'options': options, 'width': width, 'height': height })
class Thingspeak:
    '''
    The ThingSpeak Service provides access to the ThingSpeak IoT analytics platform.
    For more information, check out https://thingspeak.com/.
    
    Terms of use: https://thingspeak.com/pages/terms
    '''
    def __init__(self, client):
        self._client = client
    def channel_details(self, id: float) -> dict:
        '''
        Get various details about the channel, including location, fields, tags and name.
        
        :id: channel ID
        
        :returns: Channel details.
        '''
        res = self._client._call('Thingspeak', 'channelDetails', { 'id': id })
        return dict(res)
    def channel_feed(self, id: str, num_result: float):
        '''
        Get channel feed.
        
        :id: 
        
        :num_result: 
        '''
        return self._client._call('Thingspeak', 'channelFeed', { 'id': id, 'numResult': num_result })
    def private_channel_feed(self, id: str, num_result: float, api_key: str):
        '''
        Request data from a private channel
        
        :id: ID of the private channel feed
        
        :num_result: Number of results to fetch
        
        :api_key: Thingspeak API key
        '''
        return self._client._call('Thingspeak', 'privateChannelFeed', { 'id': id, 'numResult': num_result, 'apiKey': api_key })
    def search_by_location(self, latitude: float, longitude: float, distance: Optional[float] = None, limit: Optional[float] = None):
        '''
        Search for channels by location.
        
        :latitude: 
        
        :longitude: 
        
        :distance: 
        
        :limit: 
        '''
        return self._client._call('Thingspeak', 'searchByLocation', { 'latitude': latitude, 'longitude': longitude, 'distance': distance, 'limit': limit })
    def search_by_tag(self, tag: str, limit: Optional[float] = None):
        '''
        Search for ThingSpeak channels by tag.
        
        :tag: 
        
        :limit: 
        '''
        return self._client._call('Thingspeak', 'searchByTag', { 'tag': tag, 'limit': limit })
    def search_by_tag_and_location(self, tag: str, latitude: float, longitude: float, distance: Optional[float] = None, limit: Optional[float] = None):
        '''
        Search for channels by tag and location.
        
        :tag: 
        
        :latitude: 
        
        :longitude: 
        
        :distance: 
        
        :limit: 
        '''
        return self._client._call('Thingspeak', 'searchByTagAndLocation', { 'tag': tag, 'latitude': latitude, 'longitude': longitude, 'distance': distance, 'limit': limit })
class ThisXDoesNotExist:
    '''
    This service uses Artificial Intelligence (AI) to make random, realistic images.
    For a list of example websites, see https://thisxdoesnotexist.com/.
    These are typically made by a Generative Adversarial neural Network (GAN).
    Put simply, this involves two AIs: one to make images and another to guess if they're real or fake, and making them compete to mutually improve.
    For more information, see https://en.wikipedia.org/wiki/Generative_adversarial_network.
    '''
    def __init__(self, client):
        self._client = client
    def get_artwork(self) -> Any:
        '''
        Gets an image of an artwork that does not exist
        
        :returns: a random image of the given type
        '''
        return self._client._call('ThisXDoesNotExist', 'getArtwork', {  })
    def get_cat(self) -> Any:
        '''
        Gets an image of a cat that does not exist
        
        :returns: a random image of the given type
        '''
        return self._client._call('ThisXDoesNotExist', 'getCat', {  })
    def get_congress_person(self) -> Any:
        '''
        Gets an image of a congress person that does not exist
        
        :returns: a random image of the given type
        '''
        return self._client._call('ThisXDoesNotExist', 'getCongressPerson', {  })
    def get_fursona(self) -> Any:
        '''
        Gets an image of a fursona that does not exist
        
        :returns: a random image of the given type
        '''
        return self._client._call('ThisXDoesNotExist', 'getFursona', {  })
    def get_home_interior(self) -> Any:
        '''
        Gets an image of a home interior that does not exist
        
        :returns: a random image of the given type
        '''
        return self._client._call('ThisXDoesNotExist', 'getHomeInterior', {  })
    def get_horse(self) -> Any:
        '''
        Gets an image of a horse that does not exist
        
        :returns: a random image of the given type
        '''
        return self._client._call('ThisXDoesNotExist', 'getHorse', {  })
    def get_person(self) -> Any:
        '''
        Gets an image of a person that does not exist
        
        :returns: a random image of the given type
        '''
        return self._client._call('ThisXDoesNotExist', 'getPerson', {  })
    def get_pony(self) -> Any:
        '''
        Gets an image of a pony that does not exist
        
        :returns: a random image of the given type
        '''
        return self._client._call('ThisXDoesNotExist', 'getPony', {  })
    def get_waifu(self) -> Any:
        '''
        Gets an image of a waifu that does not exist
        
        :returns: a random image of the given type
        '''
        return self._client._call('ThisXDoesNotExist', 'getWaifu', {  })
class Traffic:
    '''
    The Traffic Service provides access to real-time traffic data using the Bing Traffic API.
    For more information, check out https://msdn.microsoft.com/en-us/library/hh441725.aspx
    '''
    def __init__(self, client):
        self._client = client
    def search(self, west_longitude: float, north_latitude: float, east_longitude: float, south_latitude: float):
        '''
        Search for traffic accidents in a given region. Results are sent as messages in the format:
        
        Message type: Traffic
        fields: latitude, longitude, type
        
        :west_longitude: 
        
        :north_latitude: 
        
        :east_longitude: 
        
        :south_latitude: 
        '''
        return self._client._call('Traffic', 'search', { 'westLongitude': west_longitude, 'northLatitude': north_latitude, 'eastLongitude': east_longitude, 'southLatitude': south_latitude })
    def stop(self):
        '''
        Stop any pending requested messages (search results).
        '''
        return self._client._call('Traffic', 'stop', {  })
class Translation:
    '''
    Uses Microsoft's Azure Cognitive Services API to translate text.
    For more information, check out https://azure.microsoft.com/en-us/pricing/details/cognitive-services/translator-text-api/.
    
    Terms of use: https://www.microsoft.com/en-us/servicesagreement
    '''
    def __init__(self, client):
        self._client = client
    def detect_language(self, text: str) -> str:
        '''
        Attempt to detect language of input text
        
        :text: Text in an unknown language
        
        :returns: Abbreviation for name of language detected in text
        '''
        res = self._client._call('Translation', 'detectLanguage', { 'text': text })
        return str(res)
    def get_supported_languages(self) -> list:
        '''
        Attempt to detect language of input text
        
        :returns: List of languages supported by the translator
        '''
        return self._client._call('Translation', 'getSupportedLanguages', {  })
    def to_english(self, text: str) -> str:
        '''
        Translate text to English
        
        :text: Text in another language
        
        :returns: Text translated to English
        '''
        res = self._client._call('Translation', 'toEnglish', { 'text': text })
        return str(res)
    def translate(self, text: str, to: str, _from: Optional[str] = None) -> str:
        '''
        Translate text between languages
        
        :text: Text in another language
        
        :to: Language to translate to
        
        :_from: Language to translate from (auto-detects if not specified)
        
        :returns: Text translated to requested language
        '''
        res = self._client._call('Translation', 'translate', { 'text': text, 'to': to, 'from': _from })
        return str(res)
class Trivia:
    '''
    The Trivia Service provides access to trivia questions using the jservice API.
    For more information, check out https://jservice.io.
    '''
    def __init__(self, client):
        self._client = client
    def get_random_question(self) -> dict:
        '''
        Get a random trivia question.
        This includes the question, answer, and additional information.
        
        :returns: structured data representing the trivia question
        '''
        res = self._client._call('Trivia', 'getRandomQuestion', {  })
        return dict(res)
class TwentyQuestions:
    '''
    The TwentyQuestions Service aids in the creation of a multiplayer
    game of twenty questions.
    '''
    def __init__(self, client):
        self._client = client
    def answer(self, answer: str):
        '''
        Answer a yes or no question about the secret word or phrase.
        
        :answer: yes or no response to previous question
        '''
        return self._client._call('TwentyQuestions', 'answer', { 'answer': answer })
    def game_started(self) -> bool:
        '''
        Check if the game has been started.
        
        :returns: true if the game has started
        '''
        res = self._client._call('TwentyQuestions', 'gameStarted', {  })
        return bool(res)
    def guess(self, guess: str) -> bool:
        '''
        Guess the word or phrase.
        
        :guess: word or phrase to guess
        
        :returns: true if the guess was correct, otherwise false
        '''
        res = self._client._call('TwentyQuestions', 'guess', { 'guess': guess })
        return bool(res)
    def restart(self):
        '''
        Restart the game.
        '''
        return self._client._call('TwentyQuestions', 'restart', {  })
    def start(self, answer: str) -> bool:
        '''
        Start a new game of twenty questions.
        
        :answer: The word or phrase to guess
        
        :returns: true on successful start
        '''
        res = self._client._call('TwentyQuestions', 'start', { 'answer': answer })
        return bool(res)
class Twitter:
    '''
    The Twitter Service provides access to posts and profile information from Twitter.
    For more information, check out https://twitter.com.
    
    Terms of use: https://twitter.com/en/tos
    '''
    def __init__(self, client):
        self._client = client
    def favorites(self, screen_name: str, count: int) -> list:
        '''
        Get the most recent tweets that a user has favorited
        
        :screen_name: Name of user
        
        :count: Number of tweets to retrieve
        
        :returns: Most recent tweets that a user has favorited
        '''
        return self._client._call('Twitter', 'favorites', { 'screenName': screen_name, 'count': count })
    def favorites_count(self, screen_name: str) -> int:
        '''
        Get the number of favorites someone has on Twitter
        
        :screen_name: Name of user
        
        :returns: Number of favorites user has
        '''
        res = self._client._call('Twitter', 'favoritesCount', { 'screenName': screen_name })
        return int(res)
    def followers(self, screen_name: str) -> int:
        '''
        Get the number of users following someone on Twitter
        
        :screen_name: Name of user
        
        :returns: Number of followers user has
        '''
        res = self._client._call('Twitter', 'followers', { 'screenName': screen_name })
        return int(res)
    def recent_tweets(self, screen_name: str, count: int) -> list:
        '''
        Get tweets from a user
        
        :screen_name: Name of user
        
        :count: Number of tweets to retrieve
        
        :returns: Tweets from user
        '''
        return self._client._call('Twitter', 'recentTweets', { 'screenName': screen_name, 'count': count })
    def search(self, keyword: str, count: int) -> list:
        '''
        Searches the most recent tweets
        
        :keyword: Keyword to search for
        
        :count: Number of tweets to retrieve
        
        :returns: Most recent tweets matching keyword
        '''
        return self._client._call('Twitter', 'search', { 'keyword': keyword, 'count': count })
    def tweets(self, screen_name: str) -> int:
        '''
        Get the number of tweets someone has made on Twitter
        
        :screen_name: Name of user
        
        :returns: Number of tweets user has
        '''
        res = self._client._call('Twitter', 'tweets', { 'screenName': screen_name })
        return int(res)
    def tweets_per_day(self, screen_name: str) -> float:
        '''
        Get how many tweets per day the user averages (most recent 200)
        
        :screen_name: Name of user
        
        :returns: How many tweets per day the user averages
        '''
        res = self._client._call('Twitter', 'tweetsPerDay', { 'screenName': screen_name })
        return float(res)
class WaterWatch:
    '''
    The WaterWatch Service provides access to real-time water data.
    For more information, check out https://waterservices.usgs.gov/
    '''
    def __init__(self, client):
        self._client = client
    def gage_height(self, min_latitude: float, max_latitude: float, min_longitude: float, max_longitude: float) -> Any:
        '''
        Get the water data for sites within a bounding box.
        For help interpreting this data, see https://help.waterdata.usgs.gov/tutorials/surface-water-data/how-do-i-interpret-gage-height-and-streamflow-values
        
        :min_latitude: Minimum latitude of bounding box
        
        :max_latitude: Maximum latitude of bounding box
        
        :min_longitude: Minimum longitude of bounding box
        
        :max_longitude: Maximum longitude of bounding box
        
        :returns: Messages sent of data
        '''
        return self._client._call('WaterWatch', 'gageHeight', { 'minLatitude': min_latitude, 'maxLatitude': max_latitude, 'minLongitude': min_longitude, 'maxLongitude': max_longitude })
    def stop(self) -> int:
        '''
        Stop sending messages from this service.
        
        :returns: Number of messages stopped.
        '''
        res = self._client._call('WaterWatch', 'stop', {  })
        return int(res)
    def stream_flow(self, min_latitude: float, max_latitude: float, min_longitude: float, max_longitude: float) -> Any:
        '''
        Get stream flow data for sites within a bounding box.
        For help interpreting this data, see https://help.waterdata.usgs.gov/tutorials/surface-water-data/how-do-i-interpret-gage-height-and-streamflow-values
        
        :min_latitude: Minimum latitude of bounding box
        
        :max_latitude: Maximum latitude of bounding box
        
        :min_longitude: Minimum longitude of bounding box
        
        :max_longitude: Maximum longitude of bounding box
        
        :returns: Messages sent of data
        '''
        return self._client._call('WaterWatch', 'streamFlow', { 'minLatitude': min_latitude, 'maxLatitude': max_latitude, 'minLongitude': min_longitude, 'maxLongitude': max_longitude })
    def water_temp(self, min_latitude: float, max_latitude: float, min_longitude: float, max_longitude: float) -> Any:
        '''
        Get the water temperature data for sites within a bounding box.
        
        :min_latitude: Minimum latitude of bounding box
        
        :max_latitude: Maximum latitude of bounding box
        
        :min_longitude: Minimum longitude of bounding box
        
        :max_longitude: Maximum longitude of bounding box
        
        :returns: Messages sent of data
        '''
        return self._client._call('WaterWatch', 'waterTemp', { 'minLatitude': min_latitude, 'maxLatitude': max_latitude, 'minLongitude': min_longitude, 'maxLongitude': max_longitude })
class Weather:
    '''
    The Weather Service provides access to real-time weather data using OpenWeatherMap.
    For more information, check out https://openweathermap.org/.
    
    Terms of Service: https://openweathermap.org/terms
    '''
    def __init__(self, client):
        self._client = client
    def description(self, latitude: float, longitude: float):
        '''
        Get a short description of the current weather for a given location.
        
        :latitude: 
        
        :longitude: 
        '''
        return self._client._call('Weather', 'description', { 'latitude': latitude, 'longitude': longitude })
    def humidity(self, latitude: float, longitude: float):
        '''
        Get the current humidity for a given location.
        
        :latitude: 
        
        :longitude: 
        '''
        return self._client._call('Weather', 'humidity', { 'latitude': latitude, 'longitude': longitude })
    def icon(self, latitude: float, longitude: float):
        '''
        Get a small icon of the current weather for a given location.
        
        :latitude: 
        
        :longitude: 
        '''
        return self._client._call('Weather', 'icon', { 'latitude': latitude, 'longitude': longitude })
    def temperature(self, latitude: float, longitude: float):
        '''
        Get the current temperature for a given location.
        
        :latitude: 
        
        :longitude: 
        '''
        return self._client._call('Weather', 'temperature', { 'latitude': latitude, 'longitude': longitude })
    def wind_angle(self, latitude: float, longitude: float):
        '''
        Get the current wind direction for a given location.
        
        :latitude: 
        
        :longitude: 
        '''
        return self._client._call('Weather', 'windAngle', { 'latitude': latitude, 'longitude': longitude })
    def wind_speed(self, latitude: float, longitude: float):
        '''
        Get the current wind speed for a given location.
        
        :latitude: 
        
        :longitude: 
        '''
        return self._client._call('Weather', 'windSpeed', { 'latitude': latitude, 'longitude': longitude })