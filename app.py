import os
from flask import Flask, flash, request, redirect, render_template,url_for,session,jsonify
from werkzeug.utils import secure_filename
import detect
import transcribe
import subprocess
from datetime import datetime
from gtts import gTTS

counter = 'a'

UPLOAD_FOLDER = os.path.join(os.getcwd(),'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

if not os.path.exists('processed'):
    os.mkdir('processed')

base_path='models-0.4.1/'
model_path= base_path + 'output_graph.pbmm'
alphabet_path= base_path + 'alphabet.txt'
lm_path= base_path + 'lm.binary'
trie_path= base_path + 'trie'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

counter=5
ALLOWED_EXTENSIONS = set(['wav'])
app.config['hin_audio_file'] = '/static/hindi_audio/hin1.mp3'


def save_hindi_audio(text):
	tts=gTTS(text,lang='hi')
	global counter
	filename = 'hin'+str(counter)+'.mp3'
	counter+=1
	aud_file=os.path.join('static','hindi_audio',filename)
	tts.save(aud_file)
	session['hin_audio_file']='/'+aud_file


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def index():
	return render_template('record.html',error="")

@app.route('/error')
def index1():
	return render_template('record.html',error="Please Speak Again")


@app.route('/upload')
def upload_form():
	return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		print(request.files)
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if not allowed_file(file.filename):
			flash('Upload only wav files')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			upload_loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(upload_loc)
			print('file saved at %s'%(upload_loc))
			return redirect(url_for('process',filename=filename))
'''
@app.route('/record')
def record():
	return render_template('record.html')

@app.route('/save',methods=['POST'])
def save():
	if request.method == 'POST':
		print(request.files)
		fname = str(datetime.now()).split('.')[0].replace(' ','-')+'.ogg'
		f = open(os.path.join(app.config['UPLOAD_FOLDER'],fname), 'wb')
		f.write(request.data)
		
		f.close()
		print('written')
		return "written"
		#return redirect(url_for('process',filename=fname))
'''

@app.route('/save',methods=['POST'])
def save():
	if request.method == 'POST':
		fname = str(datetime.now()).split('.')[0].replace(' ','-')+'.ogg'
		f = open(os.path.join(app.config['UPLOAD_FOLDER'],fname), 'wb')
		f.write(request.data)
		f.close()
		print('written')
		session['fname']=fname
		print(session['fname'])
		return "written"
		#return redirect(url_for('process',filename=fname))

@app.route('/submit')
def submit():
	return redirect(url_for('process',filename=session['fname']))	


@app.route('/process/<filename>')
def process(filename):
	new_file = os.path.join(os.getcwd(),'processed',filename.split('.')[0]+'.wav')
	filename=os.path.join(app.config['UPLOAD_FOLDER'], filename)
	#print('ffmpeg -i %s -loglevel 0 -ac 1 -ar 16000 -acodec pcm_s16le -y %s'%(filename,new_file))
	os.popen('ffmpeg -i %s -loglevel 0 -ac 1 -ar 16000 -acodec pcm_s16le -y %s'%(filename,new_file))
	lang=detect.predict(new_file)
	text = transcribe.transcribe(model_path,alphabet_path,lm_path,trie_path,new_file)
	if text=="":
		return redirect(url_for('index1'))
	else:
		session['error']=''
		print(text)
		f = open('input.txt','w')
		f.write(text)
		f.close()
		cmd = 'python -m nmt.nmt.nmt --out_dir=../eng_hi_model --inference_input_file=input.txt --inference_output_file=translated.txt' 
		#print(cmd)
		FNULL = open(os.devnull, 'w')
		retcode = subprocess.call(cmd.split(' '), stdout=FNULL, stderr=subprocess.STDOUT)
		out_file = open('translated.txt',encoding='utf-8')
		trans = out_file.readline()
		if '<unk>' in trans:
			return redirect(url_for('index1'))
		out_file.close()
	print(trans)
	save_hindi_audio(trans)
	return render_template("next.html",lang=lang,text=text,trans=trans)	

@app.route('/get/hindi/audio',methods=['GET'])
def get_hin_file():
	return jsonify({'file':session['hin_audio_file']})


if __name__=='__main__':
    app.run(debug=True)


