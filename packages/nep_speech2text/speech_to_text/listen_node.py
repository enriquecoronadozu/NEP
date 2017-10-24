#!/usr/bin/env python

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# NOTE: this program requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import time
# -*- coding: utf-8 -*-


class listen_node():

        def __init__(self):
                self.r = sr.Recognizer()
                
        def get_audio(self):
                try:
                        """ obtain audio from the microphone"""
                        t0 = time.clock()
                        with sr.Microphone() as source:
                            print("Recording!..")
                            audio = self.r.listen(source,3)
                        t1 = time.clock()
                        print ('time recorded:'  + str(t1 - t0) + "\n")
                        return audio, True
                except:
                    print("No voice detected in the audio")
                    return "none", False

        def adapt_to_environment(self):
                """ Listen for 1 second to calibrate the energy threshold for ambient noise level"""
                with sr.Microphone() as source:
                    print("Calibrating environment!..")
                    self.r.adjust_for_ambient_noise(source)

        def recognize_speech(self, in_language = "en-US"):
                """Obtain audio and convert that audio to text"""
                audio, success = self.get_audio()
                t0 = time.clock()
                text = ""

                if success:
                        # recognize speech using Google Speech Recognition
                        try:
                            # for testing purposes, we're just using the default API key
                            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                            # instead of `r.recognize_google(audio)`
                            text = self.r.recognize_google(audio, language = in_language)
                            print("** Google SR thinks you said ** \n" + text )
                        except sr.UnknownValueError:
                            print("Google Speech Recognition could not understand audio")
                        except sr.RequestError as e:
                            print("Could not request results from Google Speech Recognition service; {0}".format(e))

                t1 = time.clock()
                print ('time required for recognition:'  + str(t1 - t0) + "\n")
                return text



if __name__ == '__main__':
        main()







