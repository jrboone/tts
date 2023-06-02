## :#!/usr/bin/env python
"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import datetime
import os
import sys
import argparse
from google.cloud import texttospeech
from datetime import date

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Need to set up the environment: 
#   https://cloud.google.com/text-to-speech/docs/libraries#client-libraries-install-python
# And Application Credentials: 
#   gcloud auth application-default login
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# Code taken from Googles example
# args (script, voice)
# splice the language code out of voice
def synthesis(filename, script_text):
    

    # Instantiates a client
    #client = texttospeech.TextToSpeechClient(project="cx-tts-376414 ")
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=script_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    # voices -:
    #       en - en-US-Neural2-F
    #       es - es-US-Neural2-A
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Neural2-F", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    
    # The response's audio_content is binary.
    with open(filename, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print("Audio content written.")
# END SYNTHESIS
       


def main():
    script_text = ""

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--voice")  # Speech voice
    parser.add_argument("-f", "--file")  # input file
    parser.add_argument("-o", "--outfile")
    parser.add_argument("text", nargs='*')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        print("Usage: " + sys.argv[0] + " [script file]")
        sys.exit(1)

    # test if a file with the first argument exists
    #
        
        
    #if args.voice:
    #    print("TODO")

    if args.file:
        print("From File")
        f = args.file
        print(f)
        if os.path.exists(f):
            text = open(args.file, "r")
            script_text = text.read()
            text.close()
        else:
            print("File does not exist")
            exit(0)
            

    #if args.outfile:
    #    print("TODO")

    if args.text:  # FIX ME -
        if args.file:
            print("Cannot use text and file")
            exit(1)
            
        # if the argument is not a file treat all arguments as text to synthesize
        for i in args.text:
            script_text += i + ' '
            
    filename = os.path.join("Recordings", datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.mp3"))
    synthesis(filename, script_text)


if __name__ == "__main__":
    main()
