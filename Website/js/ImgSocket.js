// -----------------------------------------------------------------------------------------
// Declaration of usefull functions
function PM(m) { postMessage(m); }

// -----------------------------------------------------------------------------------------
// Declaration of global variables
var ImgSocket;

// -----------------------------------------------------------------------------------------
// Socket initialisation function
function initSocket() {
    // -----------------------------------------------------------------------------------------
    // Initialize Image socket 
    
    ImgSocket = new WebSocket("ws://" + location.hostname + ":443")
    
    // -----------------------------------------------------------------------------------------
    // Creating socket handlers
    // --------------------------------------------------------------------
    // Opened connection handler

    ImgSocket.onopen = function () {
        PM('[IMG][INFO] successfully connected to server');
        this.send("i");
    };

    // --------------------------------------------------------------------
    // Incoming message handler

    ImgSocket.onmessage = function (e) {
        PM(a = "data:image/jpeg;base64, " + e.data.substring(2, e.data.length-1));
        setTimeout(this.send("i"), 333);
    };

    // --------------------------------------------------------------------
    // Closed connection handler

    ImgSocket.onclose = function (e) {
        if (e.wasClean) {
            PM(`[IMG][CLOSE] Connection closed cleanly, code=${e.code} reason=${e.reason}`);
        } else {
            PM("[IMG][CLOSE] Connection died");
        }
        return "closed";
    };

    // --------------------------------------------------------------------
    // Error handler

    ImgSocket.onerror = function (e) {
        PM(`[IMG][ERROR] Socket state: ${["CONNECTING", "OPEN", "CLOSING", "CLOSED"][e.target.readyState]}`);
    }
}

// -----------------------------------------------------------------------------------------
// Thread input

onmessage = function (e) {
    m = e.data
    if (m == "close") {
        ImgSocket.close();
    } else if (m == "open") {
        if (initSocket() == "closed") {
            ImgSocket = undefined;
        }
    }
}