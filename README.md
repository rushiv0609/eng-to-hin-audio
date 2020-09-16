# English to Hindi - Audio to Audio Translation

This project was developed just for fun in early 2019. I wanted to create an end-to-end machine learning pipeline and try something new as 
I was learning machine learning and deep learning.  

This system takes your speech as input and converts the spoken sentence -> English text -> Hindi Text -> Hindi Speech. The final output will be a similar interface to that we get
of Google Translate.  

You can watch the demo in following links
1. https://drive.google.com/file/d/1HJ0B0-8iz_8j6HwipfQ5kpbcBdG-ZFWK/view?usp=sharing
2. https://drive.google.com/file/d/1H9jYESDGzuKvyxcT-0w8gSYul533VsRb/view?usp=sharing  

I have only done the translation for a few short phrases. So do not expect it to work on all phrases.  
  
Python libraries or Tools used :
* **ffmpeg** - to change audio sampling rate and encoding
* **Mozilla Deepspeech** - offline speech-to-text engine
* **Tensorflow-nmt** - English to Hindi Translation
  
## Installation

**You will need Ubuntu 16.04 or higher and Python 3.6 or higher**

1. Clone the repo
2. Run `$ sh run_first.sh`. This will install all pre-requisites
3. Run `$ python app.py` This will start a flask server on localhost

### Play Around

# Thank You
