import scipy
import librosa
import pydub
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import db_to_float
import speech_recognition as sr
import os
import soundfile as sf
import glob
import argparse
import subprocess
from datetime import datetime

now = datetime.now()

#check if given directory is valid
def dir_path(string):
    
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

parser = argparse.ArgumentParser(description='For file and directory names')
parser.add_argument('--audio_file', type=open, required=True, help='name of the audio wav file')
parser.add_argument('--directory_path', type=dir_path, help='path to the directory where the split audios will be saved')
args = parser.parse_args()

print(args.mult_files)
audio_file = args.audio_file.name


directory = args.directory_path
train_file = "filelists/" + directory + "_train_filelist.txt"
test_file = "filelists/" + directory + "_val_filelist.txt"

def convert_wav(file):
    
        print("Converting:", file)
        os.system("ffmpeg -i {0} audio-conv.wav".format(file))
        file = "audio-conv.wav"
        print("Converted:", file )
        return file


def resample_audio(file, rate):
    
        print("Resampling to:", rate)
        y, s = librosa.load(file, sr=22050)
        wavio.write(file, y, rate, sampwidth=2) 


#split audio from silence points
def split_audio(file):
    
        sound_file = AudioSegment.from_wav(file)
        average_loudness = sound_file.dBFS
        silence_threshold = average_loudness - 30 
        print(average_loudness)
        print(silence_threshold)

        audio_chunks = split_on_silence(sound_file, 
        
        min_silence_len=100,

        silence_thresh=silence_threshold
        )
        
        for i, chunk in enumerate(audio_chunks):
                out_file = "./" + directory + "/" + audio_file[:-4] + "-cut-{0}.wav".format(i)
                print("exporting", out_file)
                chunk.export(out_file, format="wav")


#append transcriptions to txt file
def append_line(file, text):
    with open(file, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text)


#speech recognition for splitted audio files
def speech_recognition(directory_name):
        i = 0
        for filename in glob.glob(os.path.join(directory_name, '*.wav')):

                x,_ = librosa.load(filename, 22050)
                sf.write(filename, x, 22050)
                audio_chunk = sr.AudioFile(filename)
                with audio_chunk as source:
                        audio = r.record(source)
                        text = r.recognize_google(audio, show_all= True)
                #if the audio does not contain speech delete it
                if not text:
                        os.remove(filename)
                        print("deleting empty file", filename)
                #take the most probable transcription
                else:
                        i = i + 1
                        first_alternative = text['alternative'][0]
                        transcription = first_alternative['transcript']
                        print(transcription)
                        filelist_transcription = filename + "|" + transcription
                        #split to test val with ratio 80% to 20%
                        if i % 5:
                                append_line(train_file, filelist_transcription)
                        else: 
                                append_line(test_file, filelist_transcription)



r = sr.Recognizer()

if not audio_file.endswith('.wav'):
	audio_file = convert_wav(audio_file)

y, s = librosa.load(audio_file) 
print("Sampling rate of the file is:" , s)
if s != 22050:
        resample_audio(audio_file, 22050)

print("Splitting audio file into chunks")
split_audio(audio_file)
print("Applying speech recognition")
speech_recognition(directory)
print("Data preparetion is done")

then = datetime.now()

print("Dataset preparetion took", then - now)





