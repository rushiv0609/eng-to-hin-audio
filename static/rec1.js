// This example uses MediaRecorder to record from a live audio stream,
// and uses the resulting blob as a source for an audio element.
//
// The relevant functions in use are:
//
// navigator.mediaDevices.getUserMedia -> to get audio stream from microphone
// MediaRecorder (constructor) -> create MediaRecorder instance for a stream
// MediaRecorder.ondataavailable -> event to listen to when the recording is ready
// MediaRecorder.start -> start recording
// MediaRecorder.stop -> stop recording (this will generate a blob of data)
// URL.createObjectURL -> to create a URL from a blob, which we can use as audio src

var recordButton, stopButton, recorder,saveButton,subButton;
const chunks =[];

var normImg = "static/rec-btn-normal.png";
var holdImg = "static/rec-btn-hold.png";

if(performance.navigation.type == 2){
   location.reload(true);
}

function mousedown() {
  var el = document.getElementById("record");
  el.setAttribute("src", holdImg)
}

function resetImage() {
  var el = document.getElementById("record");
  el.setAttribute("src", normImg)
}


window.onload = function () {
  recordButton = document.getElementById('record');
  subButton = document.getElementById('submit');
  subButton.disabled=true;

  subButton.addEventListener('click', function(){$('#loading').show();});
  // get audio stream from user's mic
  navigator.mediaDevices.getUserMedia({
    audio: true
  })
  .then(function (stream) {
    recordButton.disabled = false;
    recordButton.addEventListener("mousedown", startRecording);
    recordButton.addEventListener("mouseup", stopRecording);
    subButton.addEventListener('click', submitRecording);
    recorder = new MediaRecorder(stream);

    // listen to dataavailable, which gets triggered whenever we have
    // an audio blob available
    recorder.ondataavailable = e => {
    chunks.push(e.data);
    }
});
};

function startRecording() {
  console.log("down");
  recorder.start();
}

function stopRecording() {
  console.log("up");
  recorder.stop();
  subButton.disabled = false;
  // Stopping the recorder will eventually trigger the `dataavailable` event and we can complete the recording process
  window.setTimeout(onRecordingReady, 500);
}

function saveRecording() {
  console.log('save data');
  var blob = chunks[chunks.length - 1];
  console.log(blob);
  var oReq = new XMLHttpRequest();
oReq.open("POST", "http://127.0.0.1:5000/save", true);
x=oReq.send(blob);
subButton.disabled = false
/*
  console.log('form data')
  document.getElementById('upload').binary = blob;
  console.log(document.getElementById('upload').binary);
  document.getElementById("myForm").submit(); 
    */
}

function submitRecording() {
  saveRecording();
  window.setTimeout(function(){window.location.href = "http://127.0.0.1:5000/submit";}, 1000);
  //window.location.href = "http://127.0.0.1:5000/submit"
}

function onRecordingReady() {
  var audio = document.getElementById('audio');
  // e.data contains a blob representing the recording
  var temp = chunks[chunks.length-1];
  console.log(temp);
  uri = URL.createObjectURL(temp);
  console.log(uri);
  audio.src = uri ;
  //audio.src = chunks[chunks.length-1];
  
  audio.play();
}


