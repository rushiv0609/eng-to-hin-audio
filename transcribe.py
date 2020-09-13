from __future__ import absolute_import, division, print_function
import argparse
import numpy as np
import shlex
import subprocess
import sys
import wave
from deepspeech import Model#, printVersions
from timeit import default_timer as timer

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

#try:
#    from shhlex import quote
#except ImportError:
#    from pipes import quote

# These constants control the beam search decoder

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_ALPHA = 0.75

# The beta hyperparameter of the CTC decoder. Word insertion bonus.
LM_BETA = 1.85


# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9

base_path='/home/rushi/models-0.4.1/'
model_path= base_path + 'output_graph.pbmm'
alphabet_path= base_path + 'alphabet.txt'
lm_path= base_path + 'lm.binary'
trie_path= base_path + 'trie'

model_load_start = timer()
ds = Model(model_path, N_FEATURES, N_CONTEXT, alphabet_path, BEAM_WIDTH)
model_load_end = timer() - model_load_start
#print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)

#print('Loading language model from files {} {}'.format(lm_path, trie_path), file=sys.stderr)
lm_load_start = timer()
ds.enableDecoderWithLM(alphabet_path, lm_path, trie_path, LM_ALPHA, LM_BETA)
lm_load_end = timer() - lm_load_start

def convert_samplerate(audio_path):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate 16000 --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path))
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use 16kHz files or install it: {}'.format(e.strerror))

    return 16000, np.frombuffer(output, np.int16)

'''
class VersionAction(argparse.Action):
    def __init__(self, *args, **kwargs):
        super(VersionAction, self).__init__(nargs=0, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        printVersions()
        exit(0)
'''

def transcribe(model_path,alphabet_path,lm_path,trie_path,audio_path):
    '''
    #print('Loading model from file {}'.format(model_path), file=sys.stderr)
    model_load_start = timer()
    ds = Model(model_path, N_FEATURES, N_CONTEXT, alphabet_path, BEAM_WIDTH)
    model_load_end = timer() - model_load_start
    #print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)

    #print('Loading language model from files {} {}'.format(lm_path, trie_path), file=sys.stderr)
    lm_load_start = timer()
    ds.enableDecoderWithLM(alphabet_path, lm_path, trie_path, LM_ALPHA, LM_BETA)
    lm_load_end = timer() - lm_load_start
    #print('Loaded language model in {:.3}s.'.format(lm_load_end), file=sys.stderr)
    '''
    fin = wave.open(audio_path, 'rb')
    fs = fin.getframerate()
    if fs != 16000:
        print('Warning: original sample rate ({}) is different than 16kHz. Resampling might produce erratic speech recognition.'.format(fs), file=sys.stderr)
        fs, audio = convert_samplerate(audio_path)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1/16000)
    fin.close()

    #print('Running inference.', file=sys.stderr)
    inference_start = timer()
    text = ds.stt(audio, fs)
    #print(text)
    inference_end = timer() - inference_start
    #print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)
    return text

if __name__ == '__main__':
    base_path='/home/rushi/models-0.4.1/'
    model_path= base_path + 'output_graph.pbmm'
    alphabet_path= base_path + 'alphabet.txt'
    lm_path= base_path + 'lm.binary'
    trie_path= base_path + 'trie'
    audio_path='1.wav'
    text=transcribe(model_path,alphabet_path,lm_path,trie_path,audio_path)
    print('Transcription : %s'%(text))
