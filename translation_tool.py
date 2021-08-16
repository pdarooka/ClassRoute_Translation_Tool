# import moviepy.editor as mp
# import speech_recognition as sr
# import os
# import subprocess
# from pydub import AudioSegment
# from fastai.imports import *

# # my_clip = mp.VideoFileClip(r"Force.mp4")

# # my_clip.audio.write_audiofile(r"my_result.mp3")

# r = sr.Recognizer()

# # Reading Audio file as source
# # listening the audio file and store in audio_text variable

# with sr.AudioFile('my_result.wav') as source:
#     r.adjust_for_ambient_noise(source, duration=0.2)
#     audio_text = r.listen(source)

# # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
#     try:

#         # using google speech recognition
#         text = r.recognize_google(audio_text)
#         print('Converting audio transcripts into text ...')
#         print(text)

#     except:
#          print('Sorry.. run again...')


import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "

                whole_text += text
    # return the text for all chunks detected
    return whole_text

my_clip = mp.VideoFileClip(r"Force.mp4")
my_clip.audio.write_audiofile(r"my_result.mp3")

text = get_large_audio_transcription("my_result.mp3")
f = open("text_converted.txt", "a")
f.write(text)
f.close()


# importing libraries
# import speech_recognition as sr

# import os

# from pydub import AudioSegment
# from pydub.silence import split_on_silence

# # a function that splits the audio file into chunks
# # and applies speech recognition
# def silence_based_conversion(path = "alice-medium.wav"):

#     # open the audio file stored in
#     # the local system as a wav file.
#     song = AudioSegment.from_wav(path)

#     # open a file where we will concatenate
#     # and store the recognized text
#     fh = open("recognized.txt", "w+")

#     # split track where silence is 0.5 seconds
#     # or more and get chunks
#     chunks = split_on_silence(song,
#         # must be silent for at least 0.5 seconds
#         # or 500 ms. adjust this value based on user
#         # requirement. if the speaker stays silent for
#         # longer, increase this value. else, decrease it.
#         min_silence_len = 500,

#         # consider it silent if quieter than -16 dBFS
#         # adjust this per requirement
#         silence_thresh = -16
#     )

#     # create a directory to store the audio chunks.
#     try:
#         os.mkdir('audio_chunks')
#     except(FileExistsError):
#         pass

#     # move into the directory to
#     # store the audio files.
#     os.chdir('audio_chunks')

#     i = 0
#     # process each chunk
#     for chunk in chunks:

#         # Create 0.5 seconds silence chunk
#         chunk_silent = AudioSegment.silent(duration = 10)

#         # add 0.5 sec silence to beginning and
#         # end of audio chunk. This is done so that
#         # it doesn't seem abruptly sliced.
#         audio_chunk = chunk_silent + chunk + chunk_silent

#         # export audio chunk and save it in
#         # the current directory.
#         print("saving chunk{0}.wav".format(i))
#         # specify the bitrate to be 192 k
#         audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")

#         # the name of the newly created chunk
#         filename = 'chunk'+str(i)+'.wav'

#         print("Processing chunk "+str(i))

#         # get the name of the newly created chunk
#         # in the AUDIO_FILE variable for later use.
#         file = filename

#         # create a speech recognition object
#         r = sr.Recognizer()

#         # recognize the chunk
#         with sr.AudioFile(file) as source:
#             # remove this if it is not working
#             # correctly.
#             r.adjust_for_ambient_noise(source)
#             audio_listened = r.listen(source)

#         try:
#             # try converting it to text
#             rec = r.recognize_google(audio_listened)
#             # write the output to the file.
#             fh.write(rec+". ")

#         # catch any errors.
#         except sr.UnknownValueError:
#             print("Could not understand audio")

#         except sr.RequestError as e:
#             print("Could not request results. check your internet connection")

#         i += 1

#     os.chdir('..')


# if __name__ == '__main__':

#     print('Enter the audio file path')

#     path = input()

#     silence_based_conversion(path)
