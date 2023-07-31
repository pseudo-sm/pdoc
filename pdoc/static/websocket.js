const groupname = '{{ slug }}'
    var textboxes = document.querySelectorAll('.tinyarea');
    var typingTimer;
    var delay = 1000;

    Array.from(textboxes).forEach(function (box) {
      box.addEventListener('keyup', function () {
        clearTimeout(typingTimer)
        typingTimer = setTimeout(function () {
          sendMedicineDetails();
        })
      })
    })

    function sendMedicineDetails() {
      var textBoxes = document.getElementsByClassName('tinyarea');
      Array.from(textBoxes).forEach(function (textBox) {
        var textBoxContents = textBox.value;
        console.log('Text Box Contents=====>', textBoxContents);
        websocket.send(textBoxContents)
      });

    }

    var websocket = new WebSocket('ws://' + window.location.host + '/ws/video-calling/' + '{{ slug }}');


    websocket.onmessage = function (event) {
    //   var message = event.data
    //   console.log('On Message=====>', message)
    //   var prescriptionBox = document.getElementById('summary-patient')
    //   prescriptionBox.innerHTML = message
    //   console.log(message)
    };

    websocket.onopen = function () {
      console.log('Websocket Connection Open.')
    }

    websocket.onclose = function () {
      console.log("WebSocket connection closed.");
    };