import joblib
import pickle
import numpy as np
import librosa
import argparse
import os
import time

def get_feat(file_path):
    arr,sr = librosa.load(file_path,duration=10)
    mfcc = librosa.feature.mfcc(arr,sr)
    mean = mfcc.mean(axis=1)
    std = mfcc.std(axis=1)
    return np.append(mean,std)

def predict(path):
    out_path = os.path.join(os.getcwd(),'tmp.mp3')
    #path = os.path.abspath(path)
    cmd = os.popen('ffmpeg -i "'+path+'" -loglevel 0 -ar 44100 -acodec mp3 -y "%s"'%(out_path))
    cmd.read()
    #print(out_path)
    os.system('ffmpeg -i '+path+' -loglevel 0 -ar 44100 -acodec mp3 -y %s'%(out_path))
    print('ffmpeg -i '+path+' -loglevel 0 -ar 44100 -acodec mp3 -y %s'%(out_path))
    X = get_feat(out_path)
    os.system('rm %s'%(out_path))
    model = joblib.load('rf_model_eng-hin.joblib') 
    pred= model.predict([X])
    id2lang = pickle.load(open('id2lang.pkl','rb'))
    return id2lang[pred[0]]

