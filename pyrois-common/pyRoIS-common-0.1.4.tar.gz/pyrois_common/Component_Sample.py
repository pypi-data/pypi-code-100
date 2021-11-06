# Component_Sample.py
# 
# Copyright 2019 Ryota Higashi

from pyrois import RoIS_Common
import time

class Component_Sample():
    def __init__(self):
        self.c_status = RoIS_Common.Component_Status.READY.value

    def Speech_Synthesis(self, speech_text, SSML_text, volume, languages, character):
        self.c_status = RoIS_Common.Component_Status.BUSY.value
        
        print("コンポーネントを実行")
        time.sleep(1)
        if speech_text is not "":
            print("Speech_Text:%s"%(speech_text))
            time.sleep(1)
            if SSML_text is not "":
                print("SSML_Text:%s"%(SSML_text))
                time.sleep(1)
                if volume is not "":
                    print("Volume:%s"%(volume))
                    time.sleep(1)
                    if languages is not "":
                        print("Language:%s"%(languages))
                        time.sleep(1)
                        if character is not "":
                            print("Character:%s"%(character))
                            self.c_status = RoIS_Common.Component_Status.READY.value
                        else:
                            print("Argument_of_[character]_does_not_be_specified")
                            self.c_status = RoIS_Common.Component_Status.ERROR.value
                    else:
                        print("Argument_of_[languages]_does_not_be_specified")
                        self.c_status = RoIS_Common.Component_Status.ERROR.value        
                else:
                    print("Argument_of_[volume]_does_not_be_specified")
                    self.c_status = RoIS_Common.Component_Status.ERROR.value
            else:
                print("Argument_of_[SSML_text]_does_not_be_specified")
                self.c_status = RoIS_Common.Component_Status.ERROR.value
        else:
            print("Argument_of_[speech_text]_does_not_be_specified")
            self.c_status = RoIS_Common.Component_Status.ERROR.value
        return(self.c_status)

# if __name__ == "__main__":
#     test1 = Component_Sample()
#     test1.moji()