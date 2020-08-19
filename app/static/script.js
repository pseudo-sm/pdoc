var end = false;
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
  location.hash = location.hash = window.location.pathname.split("/")[window.location.pathname.split("/").length - 1];
}
var temp_roomHash;
const roomHash = window.location.pathname.split("/")[window.location.pathname.split("/").length - 1];
temp_roomHash = roomHash;
// TODO: Replace with your own channel ID
const drone = new ScaleDrone('2xmbUiTsqTzukyf7');
// Room name needs to be prefixed with 'observable-'
const roomName = 'observable-' + roomHash;
const configuration = {
  iceServers: [
    {url:'stun:stun01.sipphone.com'},
    {url:'stun:stun.ekiga.net'},
    {url:'stun:stun.fwdnet.net'},
    {url:'stun:stun.ideasip.com'},
    {url:'stun:stun.iptel.org'},
    {url:'stun:stun.rixtelecom.se'},
    {url:'stun:stun.schlund.de'},
    {url:'stun:stun.l.google.com:19302'},
    {url:'stun:stun1.l.google.com:19302'},
    {url:'stun:stun2.l.google.com:19302'},
    {url:'stun:stun3.l.google.com:19302'},
    {url:'stun:stun4.l.google.com:19302'},
    {url:'stun:stunserver.org'},
    {url:'stun:stun.softjoys.com'},
    {url:'stun:stun.voiparound.com'},
    {url:'stun:stun.voipbuster.com'},
    {url:'stun:stun.voipstunt.com'},
    {url:'stun:stun.voxgratia.org'},
    {url:'stun:stun.xten.com'},
    {
    url: 'turn:numb.viagenie.ca',
    credential: 'muazkh',
    username: 'webrtc@live.com'
    },
    {
        url: 'turn:192.158.29.39:3478?transport=udp',
        credential: 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
        username: '28224511:1379330808'
    },
    {
        url: 'turn:192.158.29.39:3478?transport=tcp',
        credential: 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
        username: '28224511:1379330808'
    }
    ]
};
let room;
let pc;


function onSuccess() {};

function onError(error) {
  console.error(error);
};
var database = firebase.database();
database.ref('meeting/' + roomHash).set({
  "summary": "Diagnosis summary"
});
ref = database.ref("meeting/" + roomHash);
ref.on("child_changed", function (snapshot) {
  console.log(snapshot.val());
}, function (errorObject) {
  console.log("The read failed: " + errorObject.code);
});


ref = database.ref("meeting/" + roomHash + "/");
$("#summary").keyup(function () {
    end = false;
  summary = $(this).val();
  ref.update({
    "summary": summary
  })
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
var temp_stream;

function startWebRTC(isOfferer) {
  pc = new RTCPeerConnection(configuration);

  // 'onicecandidate' notifies us whenever an ICE agent needs to deliver a
  // message to the other peer through the signaling server
  pc.onicecandidate = event => {
    if (event.candidate) {
      sendMessage({
        'candidate': event.candidate
      });
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
    temp_stream = stream;
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
var dvs, dms, pvs, pms;
var stats_vc_dv = firebase.database().ref('Stats/' + customerID + '/VideoCalling/DoctorVideo/status');
stats_vc_dv.on("value", function (snapshot) {
  dvs = snapshot.val();
  //console.log(dvs + " " + dms + " " + pvs + " " + pms);
  statusCall(dvs, dms, pvs, pms);
});
var stats_vc_dm = firebase.database().ref('Stats/' + customerID + '/VideoCalling/DoctorMic/status');
stats_vc_dm.on("value", function (snapshot) {
  dms = snapshot.val();
  //console.log(dvs + " " + dms + " " + pvs + " " + pms);
  statusCall(dvs, dms, pvs, pms);
});
var stats_vc_pv = firebase.database().ref('Stats/' + customerID + '/VideoCalling/PatientVideo/status');
stats_vc_pv.on("value", function (snapshot) {
  pvs = snapshot.val();
  //console.log(dvs + " " + dms + " " + pvs + " " + pms);
  statusCall(dvs, dms, pvs, pms);
});
var stats_vc_pm = firebase.database().ref('Stats/' + customerID + '/VideoCalling/PatientMic/status');
stats_vc_pm.on("value", function (snapshot) {
  pms = snapshot.val();
  //console.log(dvs + " " + dms + " " + pvs + " " + pms);
  statusCall(dvs, dms, pvs, pms);
});

function statusCall(dvs, dms, pvs, pms) {
  if (dvs == "on" && dms == "on" && pvs == "on" && pms == "on") {
    $(".vc-av-status").html(" ");
    $(".vc-av-status").hide();
  }
  if (doctor != "True") {
    if (pms == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Audio is turned off.");
    }
    if (pvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Video is turned off.");
    }
    if (dms == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Doctor's Audio is turned off.");
    }
    if (dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Doctor's Video is turned off.");
    }
    if (pms == "off" && pvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Audio and Video is turned off.");
    }
    if (pms == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Audio and Doctor's Video is turned off.");
    }
    if (pms == "off" && dms == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Audio from Both Side is Turned off");
    }
    if (dms == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Doctor's Audio and Video is turned off.");
    }
    if (pvs == "off" && dms == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Video and Doctor's Audio is turned off.");
    }
    if (pvs == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Video from Both Side is Turned off");
    }
    if (pms == "off" && pvs == "off" && dms == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Audio and Video, and Doctor's Audio is turned off.");
    }
    if (pms == "off" && pvs == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Audio and Video, and Doctor's Video is turned off.");
    }
    if (pms == "off" && dms == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Audio and Doctor's Audio and Video is turned off.");
    }
    if (pvs == "off" && dms == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Video and Doctor's Audio and Video is turned off.");
    }
    if (pms == "off" && pvs == "off" && dms == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Audio and Video is turned off in Both Sides.");
    }
  }
  if (doctor == "True") {
    if (pms == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Patient's Audio is turned off.");
    }
    if (pvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Patient's Video is turned off.");
    }
    if (dms == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Audio is turned off.");
    }
    if (dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Video is turned off.");
    }
    if (pms == "off" && pvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Patient's Audio and Video is turned off.");
    }
    if (pms == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Patient's Audio and Your Video is turned off.");
    }
    if (pms == "off" && dms == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Audio from Both Side is Turned off");
    }
    if (dms == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Your Audio and Video is turned off.");
    }
    if (pvs == "off" && dms == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Patient's Video and Your Audio is turned off.");
    }
    if (pvs == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Video from Both Side is Turned off");
    }
    if (pms == "off" && pvs == "off" && dms == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Patient's Audio and Video, and Your Audio is turned off.");
    }
    if (pms == "off" && pvs == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Patient's Audio and Video, and Your Video is turned off.");
    }
    if (pms == "off" && dms == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Patient's Audio and Your Audio and Video is turned off.");
    }
    if (pvs == "off" && dms == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Patient's Video and Your Audio and Video is turned off.");
    }
    if (pms == "off" && pvs == "off" && dms == "off" && dvs == "off") {
      $(".vc-av-status").show();
      $(".vc-av-status").html(" ");
      $(".vc-av-status").html("Audio and Video is turned off in Both Sides.");
    }
  }
}
let mic_switch = true;
let video_switch = true;

if (doctor != "True") {
  database.ref('Stats/' + customerID + '/VideoCalling/PatientVideo').set({
    "status": "on"
  });
  database.ref('Stats/' + customerID + '/VideoCalling/PatientMic').set({
    "status": "on"
  });

  function toggleVideo() {
    //console.log("Vdo togggggggggggggggggglas");
    if (temp_stream != null && temp_stream.getVideoTracks().length > 0) {
      video_switch = !video_switch;
    }
    if (video_switch) {
      temp_stream.getVideoTracks()[0].enabled = video_switch;
      database.ref('Stats/' + customerID + '/VideoCalling/PatientVideo').set({
        "status": "on"
      });
      $("#pause-icon").removeClass("fa-play");
      $("#pause-icon").addClass("fa-pause");
      $("#pause-icon").closest( "button" ).css( "background-color", "#2e2e2e" );
    } else {
      temp_stream.getVideoTracks()[0].enabled = video_switch;
      database.ref('Stats/' + customerID + '/VideoCalling/PatientVideo').set({
        "status": "off"
      });
      $("#pause-icon").removeClass("fa-pause");
      $("#pause-icon").addClass("fa-play");
      $("#pause-icon").closest( "button" ).css( "background-color", "#df7373" );
    }
  }

  function toggleMic() {
    //console.log("mic togggggggggggggggggg");
    if (temp_stream != null && temp_stream.getAudioTracks().length > 0) {
      mic_switch = !mic_switch;

    }
    if (mic_switch) {
      temp_stream.getAudioTracks()[0].enabled = mic_switch;
      database.ref('Stats/' + customerID + '/VideoCalling/PatientMic').set({
        "status": "on"
      });
      $("#mute-icon").removeClass("fa-microphone");
      $("#mute-icon").addClass("fa-microphone-slash");
      $("#mute-icon").closest( "button" ).css( "background-color", "#2e2e2e" );

    } else {
      temp_stream.getAudioTracks()[0].enabled = mic_switch;
      database.ref('Stats/' + customerID + '/VideoCalling/PatientMic').set({
        "status": "off"
      });
      $("#mute-icon").removeClass("fa-microphone-slash");
      $("#mute-icon").addClass("fa-microphone");
      $("#mute-icon").closest( "button" ).css( "background-color", "#df7373" );
    }
  }
}
if (doctor != "False") {
  database.ref('Stats/' + customerID + '/VideoCalling/DoctorVideo').set({
    "status": "on"
  });
  database.ref('Stats/' + customerID + '/VideoCalling/DoctorMic').set({
    "status": "on"
  });

  function toggleVideo() {
    //console.log("Vdo togggggggggggggggggglas");
    if (temp_stream != null && temp_stream.getVideoTracks().length > 0) {
      video_switch = !video_switch;
    }
    if (video_switch) {
      temp_stream.getVideoTracks()[0].enabled = video_switch;
      database.ref('Stats/' + customerID + '/VideoCalling/DoctorVideo').set({
        "status": "on"
      });
      $("#pause-icon").removeClass("fa-play");
      $("#pause-icon").addClass("fa-pause");
      $("#pause-icon").closest( "button" ).css( "background-color", "#2e2e2e" );

    } else {
      temp_stream.getVideoTracks()[0].enabled = video_switch;
      database.ref('Stats/' + customerID + '/VideoCalling/DoctorVideo').set({
        "status": "off"
      });
      $("#pause-icon").removeClass("fa-pause");
      $("#pause-icon").addClass("fa-play");
      $("#pause-icon").closest( "button" ).css( "background-color", "#df7373" );
    }
  }

  function toggleMic() {
    //console.log("mic togggggggggggggggggg");
    if (temp_stream != null && temp_stream.getAudioTracks().length > 0) {
      mic_switch = !mic_switch;

    }
    if (mic_switch) {
      temp_stream.getAudioTracks()[0].enabled = mic_switch;
      database.ref('Stats/' + customerID + '/VideoCalling/DoctorMic').set({
        "status": "on"
      });
      $("#mute-icon").removeClass("fa-microphone");
      $("#mute-icon").addClass("fa-microphone-slash");
      $("#mute-icon").closest( "button" ).css( "background-color", "#2e2e2e" );

    } else {
      temp_stream.getAudioTracks()[0].enabled = mic_switch;
      database.ref('Stats/' + customerID + '/VideoCalling/DoctorMic').set({
        "status": "off"
      });
      $("#mute-icon").removeClass("fa-microphone-slash");
      $("#mute-icon").addClass("fa-microphone");
      $("#mute-icon").closest( "button" ).css( "background-color", "#df7373" );
    }
  }
}



function localDescCreated(desc) {
  pc.setLocalDescription(
    desc,
    () => sendMessage({
      'sdp': pc.localDescription
    }),
    onError
  );
}

$("#end").click(function () {
if(end | doctor=="False"){
  if (confirm("End Meeting?")) {
    $.ajax({
      url: "/appointment-close/",
      data: {
        'appointment': roomHash,
      },
      type: 'GET',
      dataType: 'json',
      success: function (res) {
        $.removeCookie("prescription");
        window.location = "/feedback/"+res.prescription;
      }
    });

  }
}
else {

    alert('Click prescribe first.');
}
})

function sendSignalingMessage(message) {
  drone.publish({
    room: roomName,
    message
  });
}

$(document).on("change", '.pushMed', function () {
    end = false;
  med_row = $(this).closest(".med-row");
  data_count = med_row.attr("data-count");
  medicine = med_row.find('.medicine');
  medicine_name = medicine.val();
  m = $("#m-" + data_count).is(":checked");
  l = $("#l-" + data_count).is(":checked");
  s = $("#s-" + data_count).is(":checked");
  d = $("#d-" + data_count).is(":checked");
  aftFood = medicine.parent().parent().find(".aftFood-medicine").is(':checked');
  befFood = medicine.parent().parent().find(".befFood-medicine").is(':checked');
  quantity = medicine.parent().parent().find(".quantity-medicine").val();
  period = medicine.parent().parent().find(".period-medicine").val();
  remark = medicine.parent().parent().find(".remark-medicine").val();
  medicine_object = {
    [data_count]: {
      "medicine": medicine_name,
      "m": m,
      "l": l,
      "s": s,
      "d": d,
      "aftFood": aftFood,
      "befFood": befFood,
      "quantity": quantity,
      "period": period,
      "remark": remark
    }
  }
  database.ref("meeting/" + roomHash + "/medicines/").update(medicine_object);
});

if (doctor != "True") {
  database.ref("meeting/" + roomHash).on("value", function (snapshot) {
    data = snapshot.val()
    summary = data["summary"];
    //console.log(data["medicines"]);
    $(".med-repo").empty();
    for (count in data["medicines"]) {
      medicine_name = data["medicines"][count]["medicine"];
      aftFood = data["medicines"][count]["aftFood"];
      befFood = data["medicines"][count]["befFood"];
      d = data["medicines"][count]["d"];
      l = data["medicines"][count]["l"];
      s = data["medicines"][count]["s"];
      m = data["medicines"][count]["m"];
      quantity = data["medicines"][count]["quantity"]
      period = data["medicines"][count]["period"]
      remark = data["medicines"][count]["remark"]
      temp = '<li><strong>' + medicine_name + '</strong><br><strong>Doses:</strong> ';
      if (m != false) {
        temp = temp + 'Morning, '
      };
      //firebase - m
      if (l != false) {
        temp = temp + 'Noon, '
      };
      //firebase - l
      if (s != false) {
        temp = temp + 'Evening, '
      };
      //firebase - s
      if (d != false) {
        temp = temp + 'Night'
      };
      //firebase - d
      if (aftFood != false) {
        temp = temp + ' <strong></|strong> After Food'
      };
      if (befFood != false) {
        temp = temp + ' <strong></|strong> Before Food'
      };
      temp = temp + "<br><strong>" + quantity + " " + period + "</strong>";
      if (remark != "") {
        temp = temp + '<br><strong>Remark: </strong>' + remark
      };
      temp = temp + '.</li>';


      $(".med-repo").append(temp);
    }
    console.log(summary);
    $("#summary-patient").html(summary);

  }, function (errorObject) {
    console.log("The read failed: " + errorObject.code);
  });

}

$("#prescribe-submit").click(function () {
  //console.log('clicked!!!!');
  end = true;
  summary = $("#summary").val();
  medicines = [];
  $('.medicine').each(function () {
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

    medicines.push({
      "medicine": medicine,
      "m": m,
      "l": l,
      "s": s,
      "d": d,
      "aftFood": aftFood,
      "befFood": befFood,
      "quantity": quantity,
      "period": period,
      "remark": remark
    });
  });
   if(!$.cookie('prescription'))
   {
        resave = false;
        prescription = "-1";
   }
   else{
        resave = true;
        prescription = $.cookie('prescription');
   }
   console.log("resave");
   console.log(resave);
  $.ajax({
    url: "/prescription-submit/",
    data: {
      'summary': summary,
      'medicines': JSON.stringify(medicines),
      'roomhash': roomHash,
      'resave': resave,
      'prescription': prescription,
    },
    type: 'GET',
    dataType: 'json',
    success: function (res) {
      $.cookie("prescription",res.prescription);
      alert('Saved');
    }
  });

});

