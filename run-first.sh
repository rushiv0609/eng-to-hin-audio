pip install -r requirements.sh
mkdir upload
mkdir processed
mkdir hindi_audio
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.4.1/deepspeech-0.4.1-models.tar.gz
tar -xvzf deepspeech-0.4.0-models.tar.gz
mv models deepspeech_model
