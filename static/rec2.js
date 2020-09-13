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

var recordButton, stopButton, recorder;
var chunks = [];
window.onload = function () {
  recordButton = document.getElementById('record');
  stopButton = document.getElementById('stop');
  saveButton = document.getElementById('save');
  // get audio stream from user's mic
  navigator.mediaDevices.getUserMedia({
    audio: true
  })
  .then(function (stream) {
    recordButton.disabled = false;
    recordButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
    recorder = new MediaRecorder(stream);

    // listen to dataavailable, which gets triggered whenever we have
    // an audio blob available

    recorder.ondataavailable = e => {
    chunks.push(e.data);
}
  });
};

function startRecording() {
  recordButton.disabled = true;
  stopButton.disabled = false;
  saveButton.disabled = true;
  recorder.start();
}

function stopRecording() {
  recordButton.disabled = false;
  stopButton.disabled = true;
  saveButton.disabled = false;
  // Stopping the recorder will eventually trigger the `dataavailable` event and we can complete the recording process
  recorder.stop();
  console.log(chunks)
  const audioBlob = new Blob(chunks, { type: 'audio/wav' });
  console.log(audioBlob)
}

