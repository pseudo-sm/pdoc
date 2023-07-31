
const groupname = ((window.location.href).split('/', -1)[4])
console.log((window.location.href).split('/', -1)[4])
var websocket = new WebSocket('ws://' + window.location.host + '/ws/video-calling/' + groupname);

document.querySelectorAll('input[type="text"]').forEach(input => {
    input.addEventListener('input', () => {
        sendValue(input.name, input.value);
    });
});

document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        sendValue(checkbox.name, checkbox.checked);
    });
});

document.querySelectorAll('textarea').forEach(textarea => {
    textarea.addEventListener('input', () => {
        sendValue(textarea.name, textarea.value);
    });
});

function sendValue(fieldName, value) {
    const data = {
        fieldName: fieldName,
        value: value
    };
    console.log('Sending data:', data); // Add a log here to see the data being sent
    websocket.send(JSON.stringify(data));
}

websocket.onmessage = function (event) {
    try {
        var data = JSON.parse(event.data);
        console.log('DATA RECEIVED BY DEVIDUTTA SAHOO', data);
    } catch (error) {
        console.error('Error parsing received data:', error);
    }
};



websocket.onopen = function () {
    console.log('Websocket Connection Open.')
}

websocket.onclose = function () {
    console.log("WebSocket connection closed.");
};

websocket.onerror = function (event) {
    console.error('WebSocket Error:', event);
};

