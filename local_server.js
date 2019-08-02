const express = require('express')
const app = express()
var bodyParser = require('body-parser');
app.use(bodyParser.json());
var expressWs = require('express-ws')(app);
var fs = require('fs');
var socket;
var answer;

app.use(express.static('static'));


app.post('/skill',function(request,response){
  var offer = {}
  offer.type = 'offer'
  offer.sdp = request.body.value
  socket.send(JSON.stringify(offer));
  setTimeout(function() {
    response.send(answer);
    answer = null;
  }, 2000);
});

app.post('/event',function(request,response){
  console.log(request.body)
  var resp = {}
  resp.status = "ok"
  response.send(resp);
});


app.ws('/socket', function(ws, req) {
    console.log("Websocket Connected");
    socket = ws;
    ws.on('message', function(msg) {
      console.log("Message Recieved");
      answer = JSON.parse(msg);
    });
    ws.on('close', function(ws){
      console.log("Websocket Closed");
    });
});

 

app.listen(8000, () => console.log('App listening on port 8000!'))