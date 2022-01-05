// -----------------------------------------------------------------------------------------
// Thread creation
var ImgThread = new Worker('js/ImgSocket.js');
var CmdThread = new Worker('js/CmdSocket.js');

// -----------------------------------------------------------------------------------------
// Asyncronous ImgThread receiver
ImgThread.onmessage = async function (e) {
	m = e.data;

	if (m.startsWith("[IMG]")) {
		m = m.replace('[IMG]', '')
		CO(m, 'I')

		if (m.startsWith("[CLOSE]")) {
			ChangeSocketStatus('image', false);
			ID('img').src = 'img/noConnectionDark.gif';
			ImgThread.postMessage("open");

		} else if (m.startsWith("[INFO]")) {
			ChangeSocketStatus('image', true);
		}
	} else {
		ID('img').src = m;
	}
}

// -----------------------------------------------------------------------------------------
// Asyncronous CmdThread receiver
CmdThread.onmessage = async function (e) {
	m = e.data;

	if (m.startsWith("[CMD]")) {
		m = m.replace('[CMD]', '');
		
		if (m.startsWith('[ERROR]') || m.startsWith('[CLOSE]')) {
			CO(m, 'C');
			if (m.startsWith('[CLOSE]')) {
				ChangeSocketStatus('command', false);
				CmdThread.postMessage("open");
			}
		} else if (m.startsWith("[INFO]")) {
			CO(m, 'C');
			ChangeSocketStatus('command', true);
		}
	}
}

// -----------------------------------------------------------------------------------------
// Opening connection of CmdSocket and ImgSocket inside their respective thread
CmdThread.postMessage("open");
ImgThread.postMessage("open");

// -----------------------------------------------------------------------------------------
// Change status on socket state change

function ChangeSocketStatus(from, connected) {
	(elem = ID(from + 'Status')).className = (way = ((connected)?'connected':'disconnected'));
	elem.innerText = way[0].toUpperCase() + way.slice(1);

	invert = ((from == 'command')?'image':'command');

	if (ID(invert + 'Status').className == way) {
		(elem =  ID('ConnStatus')).className = way;
		elem.innerText = way[0].toUpperCase() + way.slice(1);
	} else {
		(elem =  ID('ConnStatus')).className = 'halfconn';
		elem.innerText = 'Only ' + ((connected)?from:invert) + ' socket is connected';
	}
}

// -----------------------------------------------------------------------------------------
// Sound stream control

var isStarted = false;
var streamer = ID('stream');
streamer.onplay = startStream;

function startStream() {
	console.log("something");
	// if (!isStarted) {
		CmdThread.postMessage("[L]");

		setTimeout(function () {
			if(Hls.isSupported()) {
				var hls = new Hls();
				hls.loadSource('/stream/stream.m3u8');
				hls.attachMedia(streamer);
				hls.on(Hls.Events.MANIFEST_PARSED,function() {
					streamer.play();
				});
			} else if (streamer.canPlayType('application/vnd.apple.mpegurl')) {
				streamer.src = '/stream/stream.m3u8';
				streamer.addEventListener('loadedmetadata',function() {
					streamer.play();
				});
			}
			setInterval(function() { if ( streamer.currentTime < streamer.duration - 1.5) { streamer.currentTime = streamer.duration; } });

			isStarted = true;
		}, 5000);
	// }
}


// -----------------------------------------------------------------------------------------
// Event handlers

//GAMEPAD
var previousControl = 0;
var inputMap = {
	"00"  : "0", //No input
	"0-1" : "1", //Foward 
	"01"  : "4", //BackWard
	"10"  : "8", // turn Right
	"-10" : "2", // turn left
	"1-1" : "9", //Turn right 45 deg
	"-1-1": "3", //Turn left 45 deg
	"11"  : "12", //Turn right backward 45 deg
	"-11" : "6" //Turn left backward 45 deg
}

window.addEventListener("gamepadconnected", function(e) {
	ControllerText(e.gamepad.id, "Connected");
	CmdThread.postMessage("[C]" + e.gamepad.id);
});

window.addEventListener("gamepaddisconnected", function(e) {
	ControllerText(e.gamepad.id, "Disconnected");
	CmdThread.postMessage("[C]" + "keyboard");
});

function resizeImg(obj) {
	obj = obj.parentNode;
	if (obj.className == "frame"){
		obj.className = "framefullscreen";
		ID('soundMenuRight').id = 'soundMenuBottom';
	} else {
		obj.className = "frame";
		ID('soundMenuBottom').id = 'soundMenuRight';
	}
}

function sendVoice() {
	var verif = true;

	[ (v = ID('voice')), (l = ID('lang')) ].forEach( e => {
		if (e.value == '') {
			e.style.border = '2px solid red';
			e.focus();
			verif = false;
		} else {
			e.border = '';
		}
	});

	if (!verif) { return; }

	CmdThread.postMessage('[V]' + l.value + "|" + v.value);
}

//KEYBOARD
var AntiBack = [true, true, true, true];

document.addEventListener('keydown', function (e) {
	switch (e.key) {
		case 'w':
			if (AntiBack[0]) {
				CmdThread.postMessage("[A]1");
				AntiBack[0] = false;
			}
			break;

		case 'a':
			if (AntiBack[1]) {
				CmdThread.postMessage("[A]2");
				AntiBack[1] = false;
			}
			break;

		case 's':
			if (AntiBack[2]) { 
				CmdThread.postMessage("[A]4");
				AntiBack[2] = false;
			}
			break;

		case 'd':
			if (AntiBack[3]) { 
				CmdThread.postMessage("[A]8");
				AntiBack[3] = false;
			}
			break;
	}
});



document.addEventListener('keyup', function (e) {
	switch (e.key) {
		case 'w':
			if (!AntiBack[0]) {
				CmdThread.postMessage("[D]1");
				AntiBack[0] = true;
			}
			break;

		case 'a':
			if (!AntiBack[1]) {
				CmdThread.postMessage("[D]2");
				AntiBack[1] = true;
			}
			break;

		case 's':
			if (!AntiBack[2]) {
				CmdThread.postMessage("[D]4");
				AntiBack[2] = true;
			}
			break;

		case 'd':
			if (!AntiBack[3]) {
				CmdThread.postMessage("[D]8");
				AntiBack[3] = true;
			}
			break;

		case 'q':
			CmdThread.postMessage("[D]15");
			break;
		

		case '1': case '2': case '3': case '4':
			ID("soundbtn" + e.key).click();
			break;
			
		case '5':
			ID('voice').click();
			break;
	}
});

