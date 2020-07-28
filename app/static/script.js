
var firebaseConfig = {
    apiKey: "AIzaSyCNtuLp9_8dTKGHGnYTQDvtc4sjdG6Al8Q",
    authDomain: "pdochealth.firebaseapp.com",
    databaseURL: "https://pdochealth.firebaseio.com",
    projectId: "pdochealth",
    storageBucket: "pdochealth.appspot.com",
    messagingSenderId: "781169590792",
    appId: "1:781169590792:web:247b3e1249dac8e0e8c7bd",
    measurementId: "G-56VD6RED0L"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
if (!location.hash) {
  location.hash = location.hash = window.location.pathname.split("/")[window.location.pathname.split("/").length-1];
}
const roomHash = window.location.pathname.split("/")[window.location.pathname.split("/").length-1];

// TODO: Replace with your own channel ID
const drone = new ScaleDrone('2xmbUiTsqTzukyf7');
// Room name needs to be prefixed with 'observable-'
const roomName = 'observable-' + roomHash;
const configuration = {
  iceServers: [{
    urls: 'stun:stun.l.google.com:19302'
  }]
};
let room;
let pc;


function onSuccess() {};
function onError(error) {
  console.error(error);
};

var database = firebase.database();
ref = database.ref("meeting/"+roomHash+"/");
$("#summary").keyup(function(){
    summary = $(this).val();
    ref.update({"summary":summary})
});



drone.on('open', error => {
  if (error) {
    return console.error(error);
  }
  room = drone.subscribe(roomName);
  room.on('open', error => {
    if (error) {
      onError(error);
    }
  });
  // We're connected to the room and received an array of 'members'
  // connected to the room (including us). Signaling server is ready.
  room.on('members', members => {
    console.log('MEMBERS', members);
    // If we are the second user to connect to the room we will be creating the offer
    const isOfferer = members.length === 2;
    startWebRTC(isOfferer);
  });
});

// Send signaling data via Scaledrone
function sendMessage(message) {
  drone.publish({
    room: roomName,
    message
  });
}

function startWebRTC(isOfferer) {
  pc = new RTCPeerConnection(configuration);

  // 'onicecandidate' notifies us whenever an ICE agent needs to deliver a
  // message to the other peer through the signaling server
  pc.onicecandidate = event => {
    if (event.candidate) {
      sendMessage({'candidate': event.candidate});
    }
  };

  // If user is offerer let the 'negotiationneeded' event create the offer
  if (isOfferer) {
    pc.onnegotiationneeded = () => {
      pc.createOffer().then(localDescCreated).catch(onError);
    }
  }

  // When a remote stream arrives display it in the #remoteVideo element
  pc.onaddstream = event => {
    remoteVideo.srcObject = event.stream;
  };

  navigator.mediaDevices.getUserMedia({
    audio: true,
    video: true
  }).then(stream => {
    // Display your local video in #localVideo element
    localVideo.srcObject = stream;
    // Add your stream to be sent to the conneting peer
    pc.addStream(stream);
  }, onError);

  // Listen to signaling data from Scaledrone
  room.on('data', (message, client) => {
    // Message was sent by us
    if (client.id === drone.clientId) {
      return;
    }

    if (message.sdp) {
      // This is called after receiving an offer or answer from another peer
      pc.setRemoteDescription(new RTCSessionDescription(message.sdp), () => {
        // When receiving an offer lets answer it
        if (pc.remoteDescription.type === 'offer') {
          pc.createAnswer().then(localDescCreated).catch(onError);
        }
      }, onError);
    } else if (message.candidate) {
      // Add the new ICE candidate to our connections remote description
      pc.addIceCandidate(
        new RTCIceCandidate(message.candidate), onSuccess, onError
      );
    }
  });
}

function localDescCreated(desc) {
  pc.setLocalDescription(
    desc,
    () => sendMessage({'sdp': pc.localDescription}),
    onError
  );
}

$("#end").click(function(){
  if (confirm("End Meeting?")) {
    $.ajax({
        url: "/appointment-close/",
        data : {
            'appointment':roomHash,
        },
        type: 'GET',
        dataType: 'json',
        success: function(res) {
            window.location="/patient-dashboard/";
        }
    });

  }
})

function sendSignalingMessage(message) {
  drone.publish({
    room: roomName,
    message
  });
}

$(document).on("change",'.medicine',function(){
    medicine_name = $(this).val();
    m = $(this).parent().parent().find(".med-time").children(".M-medicine").is(':checked');
    l = $(this).parent().parent().find(".med-time").children(".L-medicine").is(':checked');
    s = $(this).parent().parent().find(".med-time").children(".S-medicine").is(':checked');
    d = $(this).parent().parent().find(".med-time").children(".D-medicine").is(':checked');
    aftFood = $(this).parent().parent().find(".aftFood-medicine").is(':checked');
    befFood = $(this).parent().parent().find(".befFood-medicine").is(':checked');
    quantity = $(this).parent().parent().find(".quantity-medicine").val();
    period = $(this).parent().parent().find(".period-medicine").val();
    remark = $(this).parent().parent().find(".remark-medicine").val();
    medicine_object = {[medicine_name] : {"m":m,"l":l,"s":s,"d":"d","aftFood":aftFood,"befFood":befFood,"quantity":quantity,"period":period,"remark":remark}}
    database.ref("meeting/"+roomHash+"/medicines/").update(medicine_object);
});

if(doctor!="True"){
database.ref("meeting/"+roomHash).on("value", function(snapshot) {
    data = snapshot.val()
    summary = data["summary"];
    console.log(data["medicines"]);
    for(medicine in data["medicines"])
    {

        aftFood = data["medicines"][medicine]["aftFood"];
        befFood = data["medicines"][medicine]["befFood"];
        d = data["medicines"][medicine]["d"];
        l = data["medicines"][medicine]["l"];
        s = data["medicines"][medicine]["s"];
        m = data["medicines"][medicine]["m"];
        quantity = data["medicines"][medicine]["quantity"]
        period = data["medicines"][medicine]["period"]
        remark = data["medicines"][medicine]["remark"]
        temp = '<div class="row no-gutters mt-1 mb-1 med-det"> \
                                    <div class="col-md-4 col-sm-12 my-auto"> \
                                        <input type="text" class="form-control medicine" value="'+medicine+'" placeholder="Enter Medicine Name"> \
                                    </div> \
                                    <div class="col-md-4 col-sm-12">M-<input type="checkbox" name="" id="" class="M-medicine">&nbsp;&nbsp;'

        temp = temp + 'L-<input type="checkbox" name="" id="" class="L-medicine"';
        if (l != false){temp = temp+'checked'};
        temp = temp + '>&nbsp;&nbsp;'
        temp = temp + 'S-<input type="checkbox" name="" id="" class="S-medicine"'
        if (s != false){temp = temp+'checked'};
        temp = temp + '>&nbsp;&nbsp;'
        temp = temp + 'D-<input type="checkbox" name="" id="" class="D-medicine"'
        if (d != false){temp = temp+'checked'};
        temp = temp + '><br><div class="custom-control custom-radio custom-control-inline"> \
        <input type="radio" id="customRadioInline1" name="customRadioInline1" class="custom-control-input aftFood-medicine" '
        if (aftFood != false){temp = temp+'checked'};
        temp = temp + '><label class="custom-control-label" for="customRadioInline1">Aft Food</label> \
        </div> \
        <div class="custom-control custom-radio custom-control-inline">'
        temp = temp + '<input type="radio" id="customRadioInline2" name="customRadioInline1" class="custom-control-input befFood-medicine"'
        if (befFood != false){temp = temp+'checked'};
        temp = temp+'><label class="custom-control-label" for="customRadioInline2">Bef Food</label> \
    </div> \
    </div> \
    <div class="col-6 col-md-2 col-sm-6 my-auto"> \
        <input type="text" class="form-control quantity-medicine" value="'+quantity+'" placeholder="Quantity"> \
    </div> \
    <div class="col-6 col-md-2 col-sm-6 col-xs-3 my-auto"> \
        <input type="text" class="form-control period-medicine" value="'+period+'" placeholder="Period"> \
    </div> \
    <div class="col-md-12 col-sm-12 my-auto"> \
        <input type="text" class="form-control remark-medicine" value="'+remark+'" placeholder="Remark"> \
    </div> \
    </div> \
                                    '
        $(".med-repo").append(temp);
    }
    console.log(summary);
    $("textarea#summary-patient").val(summary);

}, function (errorObject) {
  console.log("The read failed: " + errorObject.code);
});

}

$("#prescribe-submit").click(function(){
    console.log('clicked!!!!');
    summary = $("#summary").val();
    medicines = [];
    $('.medicine').each(function() {
        medicine = $(this).val();
        m = $(this).parent().parent().find(".med-time").children(".M-medicine").is(':checked');
        l = $(this).parent().parent().find(".med-time").children(".L-medicine").is(':checked');
        s = $(this).parent().parent().find(".med-time").children(".S-medicine").is(':checked');
        d = $(this).parent().parent().find(".med-time").children(".D-medicine").is(':checked');
        aftFood = $(this).parent().parent().find(".aftFood-medicine").is(':checked');
        befFood = $(this).parent().parent().find(".befFood-medicine").is(':checked');
        quantity = $(this).parent().parent().find(".quantity-medicine").val();
        period = $(this).parent().parent().find(".period-medicine").val();
        remark = $(this).parent().parent().find(".remark-medicine").val();

        medicines.push({"medicine":medicine,"m":m,"l":l,"s":s,"d":d,"aftFood":aftFood,"befFood":befFood,"quantity":quantity,"period":period,"remark":remark});
        });

        $.ajax({
        url: "/prescription-submit/",
        data : {
            'summary':summary,
            'medicines':JSON.stringify(medicines),
            'roomhash':roomHash,
        },
        type: 'GET',
        dataType: 'json',
        success: function(res) {
            console.log(res);
        }
    });

});
