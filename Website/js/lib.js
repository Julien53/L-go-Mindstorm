// -----------------------------------------------------------------------------------------
// Creating usefull functions

function ID(id) { return document.getElementById(id); }
function CLASS(CLASS) { return document.getElementsByClassName(CLASS); }
function CO(message, what='') { (e = ID(what + 'console')).innerHTML = message + "<br>" + e.innerHTML; }

function Send(message, what) { [ImgThread, CmdThread][what].postMessage(message); }