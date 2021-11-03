from pynput import keyboard
import os, pyaudio, wave, time, atexit, logging, random, datetime
logging.basicConfig(level = logging.DEBUG, format = "%(message)s")
random.seed(datetime.datetime.now())
class Audio:
    terminate = False
    started = False
    paused = False
    _terminate = False
    button = 0
    def help():
        logging.debug("Audio():")
        logging.debug("\t[1] self.__init__(self, filename)")
        logging.debug("\t[2] self.main(self) # play a single file.\n")
    def __init__(self, filename):
        self.filename = filename
        self.__load_wave()
        self.__to_pyaudio()
    def __on_press(self, key):
        if (key == keyboard.Key.f9):
            state = self.audio.is_active()
            self.button = 2 * (state) + 1 * (not state)
            while (state == self.audio.is_active()):
                time.sleep(0.01)
            self.button = 0
        elif (key == keyboard.Key.f10):
            self.button = 2
            while (True == self.audio.is_active()):
                time.sleep(0.01)
            self.button = 0
            self.terminate = True
            self._terminate = True
        elif (key == keyboard.Key.f8):
            self.button = 2
            while (True == self.audio.is_active()):
                time.sleep(0.01)
            self.button = 0
            self.terminate = True
    def __load_wave(self):
        self.audio1 = wave.open(self.filename, 'rb')
    def __call_back(self, in_data, frame_count, time_info, status):
        data = self.audio1.readframes(frame_count)
        return (data, pyaudio.paContinue)
    def __to_pyaudio(self):
        self.p = pyaudio.PyAudio()
        self.audio = self.p.open(format = self.p.get_format_from_width(self.audio1.getsampwidth()),
                                 channels = self.audio1.getnchannels(),
                                 rate = self.audio1.getframerate(),
                                 output = True,
                                 stream_callback = self.__call_back)
    def __play_audio(self):
        self.audio.start_stream()
        self.started, self.paused = True, False
    def __pause_audio(self):
        self.audio.stop_stream()
        self.started, self.paused = True, True
    def main(self):
        atexit.register(self.audio1.close)
        atexit.register(self.p.terminate)
        atexit.register(self.audio.close)
        self.listener = keyboard.Listener(on_press = self.__on_press)
        self.listener.start()
        atexit.register(self.listener.stop)
        while not (self.terminate or (self.paused == False and self.audio.is_active() == False)):
            if self.button == 1:
                if (self.audio.is_stopped()):
                    self.__play_audio()
            elif self.button == 2:
                if (self.audio.is_active()):
                    self.__pause_audio()
            time.sleep(0.01)
        return self._terminate
class AudioList:
    def help():
        logging.debug("AudioList(): __init__(self, audioList)")
        logging.debug("\t# audioList must be a list of strings.\n")
    def __init__(self, audioList):
        if ((type(audioList) == list) and all((type(x) == str) for x in audioList)):
            self.audioList = []
            for audio in audioList:
                if ((audio[-4:] == '.wav') and (os.path.isfile(audio))):
                    self.audioList.append(audio)
            logging.debug(f"Found a total of {len(self.audioList)} music file(s):")
            for index, audio in enumerate(self.audioList):
                logging.debug(f"\t[{index + 1}] \"{audio}\"")
            logging.debug("\n")
            if (len(self.audioList) == 0):
                self.audioList = None
        else:
            logging.warning("Error: audioList must be a list of strings.\n")
            self.audioList = None
class Album:
    def help():
        logging.debug("Album(): ")
        logging.debug("\t[1] self.__init__(self, audioList, loop = False, shuffle = False)")
        logging.debug("\t\t# audioList must be an AudioList() Object.")
        logging.debug("\t[2] self.play_audio(self) # to start playlist.")
        logging.debug("\t[3] Press [f8] to skip, [f9] to pause, [f10] to stop.\n")
    def __init__(self, audioList, loop = False, shuffle = False):
        self.audioList, self.loop = audioList.audioList, loop
        self.shuffle = shuffle
        if ((self.shuffle) and (self.audioList != None)):
            random.shuffle(self.audioList)
            logging.debug("Music files are successfully reshuffled.\n")
            self.__print_list()
    def __print_list(self):
        logging.debug("Order of music files to be played:")
        for index, audio in enumerate(self.audioList):
            logging.debug(f"\t[{index + 1}] \"{audio}\"")
        logging.debug("\n")
    def play_audio(self):
        if (self.audioList != None):
            while True:
                for audio in self.audioList:
                    logging.debug(f"Currently playing {audio}.\n")
                    audio = Audio(audio)
                    if (audio.main()):
                        self.loop = False
                        break
                if (self.loop == False):
                    break
        else:
            logging.debug("No playable albums are found.\n")