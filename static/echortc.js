var ws
var hostname = window.location.host
if (window.location.protocol == "https:"){
    var proto = "wss://"
}
else{
    var proto = 'ws://'
}

let pc;
let config = { iceServers: [{urls: "stun:global.stun.twilio.com:3478"}], iceTransportPolicy: 'all', iceCandidatePoolSize: 2}

var constraints = {
    mandatory: {
        OfferToReceiveAudio:true,
        OfferToReceiveVideo:true,
    }
};
let answerTimeout;

var mediaConstraints = {
  audio: true, // We want an audio track
  video: true // ...and we want a video track
};


function setupRTC(){
 pc = new RTCPeerConnection(config);
 pc.onicecandidate = iceCallback
 pc.onicegatheringstatechange = gatheringStateChange;
}

function iceCallback(event) {
  if (event.candidate) {
    console.log(event.candidate);
  }
}

function gatheringStateChange() {
  console.log(pc.iceGatheringState);
  if (pc.iceGatheringState === 'complete') {
    if (answerTimeout != null){
      window.clearTimeout(answerTimeout);
      console.log('ICE Complete')
      sendAnswer();
    }
    else {
      console.log('Answer already sent');
    }
  }
  
}

function sendAnswer(){
  timeoutID = null;
  var answer =pc.currentLocalDescription;
  ws.send(JSON.stringify(answer));
  console.log("ANSWER");
  console.log(answer.sdp);
}

function createOffer(){
  pc.createOffer(constraints
  ).then(
     gotDescription,
     errorHandler
 );
}

function answerOffer(msg){
  var sig = JSON.parse(msg);
  //console.log(sig);
  var offer = new RTCSessionDescription(sig);
  pc.setRemoteDescription(offer);
  
  pc.createAnswer(function (answer) {
    console.log("OFFER");
    console.log(sig.sdp);
    pc.setLocalDescription(answer);
    answerTimeout = window.setTimeout(sendAnswer, 2000);   
  }, errorHandler, constraints);
  pc.ontrack = remoteMedia;
}
    
    
function gotDescription(offer) {
  //console.log(offer.sdp);
  pc.setLocalDescription(offer);
  //ws.send(offer)
}

function errorHandler(error) {
  console.error('Error creating offer: ', error);
}


function connectWS() {
    ws = new WebSocket(proto + hostname + "/socket");
    //ws = new WebSocket("wss://sammachin.ngrok.io/socket");
    ws.onopen = function() {
        console.log("CONNECTED");
        setupRTC();
        localMedia();
    };  
    ws.onmessage = function(event) {
        answerOffer(event.data);
    };
}


function localMedia(){
navigator.mediaDevices.getUserMedia(mediaConstraints)
    .then(function(localStream) {
      document.getElementById("local").srcObject = localStream;
      localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
    })
    .catch(errorHandler);
}

function remoteMedia(event) {
  console.log(event);
  document.getElementById("remote").srcObject = event.streams[0];
  //var remote = document.getElementById("remote");
  //if (remote.srcObject !== event.streams[0]) {
  //  remote.srcObject = event.streams[0];
  //  console.log('received remote stream', event);
  //}
}
