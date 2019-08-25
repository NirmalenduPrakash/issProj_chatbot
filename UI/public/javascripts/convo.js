var botui = new BotUI('api-bot');

var socket = io.connect('http://localhost:8010');
//var socket = io.connect('https://96e49df1.ngrok.io');
// read the BotUI docs : https://docs.botui.org/

botui.message.add({
  content: 'Welcome to hawker bot',
  delay: 1500,
}).then(function () {
  botui.action.text({
    action: {
      placeholder: '', }
  }
).then(function (res) {
  socket.emit('fromClient', { client : res.value }); // sends the message typed to server
    console.log(res.value); // will print whatever was typed in the field.
  }).then(function () {
    socket.on('fromServer', function (data) { // recieveing a reply from server.
      console.log(data.server);
      if(data.server.indexOf('**')!==-1){
        addButtons(data.server);
      }
      else if(data.server.indexOf('http')!==-1){
        addHyperlink(data.server)
      }
      else if(data.server==''){
        addAction();
      }
      else{
        newMessage(data.server);
        addAction();
      }
      
  })
});
})

function addHyperlink (data) {
  var name=data.split('//')[1].split('.')[1];
  // botui.message.add({
  //   content: name+'('+data+')^',
  //   delay: 0,
  // })
  botui.action.button({
    action: [{'text':'Order','value':name},{'text':'cancel','value':'cancel'}]
  }).then(function (res) { 
    if(res.text=='Order'){
      window.open(data, '_blank');
    }
    addAction();
  });
  // botui.action.button({
  //   action: 'cancel'
  // }).then(function (res) { 
  //   addAction();
  // });
}

function newMessage (response) {
  botui.message.add({
    content: response,
    delay: 0,
  })
}

function addAction () {
  botui.action.text({
    action: {
      placeholder: 'enter response...', 
    }
  }).then(function (res) {
    socket.emit('fromClient', { client : res.value });
    console.log('client response: ', res.value);
  })
}

function addButtons(data){
  data=data.split('**');
  var arr=[]
  data.forEach(element => {
    if(element!='')
      arr.push({text:element,value:element});
  });

  botui.action.button({
    action: arr
  }).then(function (res) { 
    socket.emit('fromClient', { client : res.value });
    console.log('client response: ', res.value);
  });
}