from pynput import keyboard
from traitlets.config.configurable import Configurable
import pyaudio, wave, os, time, atexit, traitlets, random, datetime
class ShareObject:
    
    def help():
        
        print("ShareObject(): ")
        
        print("\t[1] __init__(self, defVal)")
        
        print("\t[2] claim(self) # enable value editing")
        
        print("\t[3] get(self) # obtain target value")
        
        print("\t[4] alter(self, newVal) # request to edit value\n")
    
    def __init__(self, defVal):
        
        self.value = defVal
        
        self.ready = False
        
    def claim(self):
        
        self.ready = True
    
    def get(self):
        
        return self.value
        
    def alter(self, newVal):
        
        if (self.ready):
            
            self.value = newVal
            
            self.ready = False
            
class AudioPlayer(Configurable):
    
    _paused = traitlets.Bool(False).tag(config = True)
    
    def help():
        
        print("AudioPlayer(): ")
        
        print("\t[1] __init__(self, filename)")
        
        print("\t[2] play(self) # play wave file\n")
    
    def __init__(self, filename, * args, ** kwargs):
        
        super(AudioPlayer, self).__init__(*args, **kwargs)
        
        self.filename = self.__validate_filename(filename)
        
        self.terminate, self._terminate = False, 1
        
        if (self.filename != None):
            
            self.wavFile = wave.open(self.filename, "rb")
            
            atexit.register(self.wavFile.close)
            
            self._pyAudio = pyaudio.PyAudio()
            
            atexit.register(self._pyAudio.terminate)
            
            self.audio = self.__load_audio()
            
            atexit.register(self.audio.close)
            
            self.paused = ShareObject(False)
            
            self.audio.stop_stream()
            
    @traitlets.observe("_paused")
    def __display_state(self, change):
        
        print(f"\t[State] {'Paused' if change['new'] else 'Playing'}.")
        
    def __on_press(self, key):
        
        if (key == keyboard.Key.f9):
            
            self.paused.claim()
        
            while (self.paused.ready):
                
                time.sleep(0.05)
        
        elif (key == keyboard.Key.f10):
            
            self._terminate = 0
            
            self.terminate = True
        
        elif (key == keyboard.Key.f8):
            
            self._terminate = 1
            
            self.terminate = True
    
    def play(self):
        
        if (self.filename != None):
            
            print("\t[State] Playing.")
        
            self.audio.start_stream()
        
            k_listener = keyboard.Listener(on_press = self.__on_press)
            
            k_listener.start()
            
            while ((not self.terminate) and (self.paused.get() or self.audio.is_active())):
                
                if (self.paused.ready):
                    
                    ACTIVE = self.audio.is_active()
                    
                    if (ACTIVE):
                        
                        self.audio.stop_stream()
                        
                    else:
                        
                        self.audio.start_stream()
                    
                    self._paused = ACTIVE
                    
                    self.paused.alter(ACTIVE)
                    
                time.sleep(0.05)
            
            k_listener.stop()
            
            self.audio.close()
            
            self._pyAudio.terminate()
            
            self.wavFile.close()
            
        self._paused = True
            
        print("")
        
        return self._terminate
        
    def __validate_filename(self, filename):
        
        if (type(filename) != str):
            
            print(f"Warning [AudioPlayer]: {filename} is not a string.\n")
            
            filename = None
        
        elif ((len(filename) >= 5) and (filename[-4:] == ".wav") and (os.path.isfile(filename))):
            
            pass
        
        else:
        
            print(f"Warning [AudioPlayer]: {filename} is not an existent wav file.\n")
            
            filename = None
            
        return filename
    
    def __call_back(self, in_data, frame_count, time_info, status):
        
        data = self.wavFile.readframes(frame_count)
        
        return (data, pyaudio.paContinue)
    
    def __load_audio(self):

        return self._pyAudio.open(
            format = self._pyAudio.get_format_from_width(self.wavFile.getsampwidth()),
            channels = self.wavFile.getnchannels(),
            rate = self.wavFile.getframerate(),
            output = True,
            stream_callback = self.__call_back
        )

class AudioList:

    def help():

        print("AudioList(): ")
        
        print("\t[1] __init__(self, audioList)")

        print("\t\t# audioList must be a list of strings.\n")

    def __init__(self, audioList):

        if ((type(audioList) == list) and all((type(x) == str) for x in audioList)):

            self.audioList = []

            for audio in audioList:

                if ((audio[-4:] == '.wav') and (os.path.isfile(audio))):

                    self.audioList.append(audio)

            print(f"Found a total of {len(self.audioList)} music file(s):\n")

            for index, audio in enumerate(self.audioList):

                print(f"\t[{index + 1}] \"{audio}\"")
            print("")
            if (len(self.audioList) == 0):

                self.audioList = None

        else:

            print("Error: audioList must be a list of strings.\n")

            self.audioList = None

class Album:
    
    random = random.Random(datetime.datetime.now()) 

    def help():

        print("Album(): ")

        print("\t[1] self.__init__(self, audioList, loop = False, shuffle = False)")

        print("\t\t# audioList must be an AudioList() Object.")

        print("\t[2] self.play_audio(self) # to start playlist.")

        print("\t[3] Press [f8] to skip, [f9] to pause, [f10] to stop.\n")

    def __init__(self, audioList, loop = False, shuffle = False):

        self.audioList, self.loop = audioList.audioList, loop

        self.shuffle = shuffle

        if ((self.shuffle) and (self.audioList != None)):

            self.random.shuffle(self.audioList)

            print("Music files are successfully reshuffled.\n")

            self.__print_list()

    def __print_list(self):

        print("Order of music files to be played:\n")

        for index, audio in enumerate(self.audioList):

            print(f"\t[{index + 1}] \"{audio}\"")

        print("")

    def play_audio(self):

        if (self.audioList != None):

            while True:

                for audio in self.audioList:

                    print(f"Currently playing {audio}.\n")
                    
                    audio = AudioPlayer(audio)
                    
                    if (audio.play() == 0):
                        
                        self.loop = False
                        
                        break
                    
                if (self.loop == False):
                    
                    break
                
        else:
            
            print("No playable albums are found.\n")
   