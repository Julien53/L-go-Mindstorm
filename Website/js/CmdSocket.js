// -----------------------------------------------------------------------------------------
// Declaration of usefull functions
function PM(m) { postMessage(m); }

// -----------------------------------------------------------------------------------------
// Declaration of global variables
var CmdSocket;

// -----------------------------------------------------------------------------------------
// Socket initialisation function 
function initSocket() {
    // -----------------------------------------------------------------------------------------
    // Initialize Command socket

    CmdSocket= new WebSocket("ws://" + location.hostname + ":443");

    // -----------------------------------------------------------------------------------------
    // Creating socket handlers
    // --------------------------------------------------------------------
    // Opened connection handler

    CmdSocket.onopen = function () {
        PM('[CMD][INFO] successfully connected to server');
        this.send("begin");
    };

    // --------------------------------------------------------------------
    // Incoming message handler

    CmdSocket.onmessage = function (e) {
        PM("[CMD]" + e.data);
        this.send(e.data);
    };

    // --------------------------------------------------------------------
    // Closed connection handler

    CmdSocket.onclose = function (e) {
        if (e.wasClean) {
            PM(`[CMD][CLOSE] Connection closed cleanly, code=${e.code} reason=${e.reason}`);
        } else {
            PM("[CMD][CLOSE] Connection died");
        }
        return "closed";
    };

    // --------------------------------------------------------------------
    // Error handler

    CmdSocket.onerror = function (e) {
        PM(`[CMD][ERROR] Socket state: ${["CONNECTING", "OPEN", "CLOSING", "CLOSED"][e.target.readyState]}`);
    }
}


// -----------------------------------------------------------------------------------------
// Thread input

onmessage = function (e) {
    m = e.data
    if (m == "close") {
        CmdSocket.close();
    } else if (m == "open") {
        if (initSocket() == "closed") {
            CmdSocket = undefined;
        }
    } else {
        if (CmdSocket != null) {
            CmdSocket.send(m);
        }
    }
}