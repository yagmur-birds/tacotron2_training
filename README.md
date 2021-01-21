# Automatization of Dataset Preparation

The given script automatizes the data preparation for Tacotron-2's training. 

The script:

1) Converts audio files that are not wav files in wav.
2) Resamples them to 22050
3) Splits the given audio from silence points
4) Applies speech recognition to audio files.
5) Saves the transcriptions in train and val filelists.
