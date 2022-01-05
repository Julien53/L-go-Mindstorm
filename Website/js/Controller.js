var previousControl = 0;
var inputMap = {
    "00" : "0", //No input
    "-10" : "1", //Foward 
    "10": "4", //BackWard
    "01" : "8", // turn Right
    "0-1" : "2", // turn left
    "-11": "9", //Turn right 45 deg
    "-1-1": "3", //Turn left 45 deg
    "11"  : "12", //Turn right backward 45 deg
    "1-1": "6" //Turn left backward 45 deg
}

async function GetInput(){
    setInterval (() => {
        const gamepad = navigator.getGamepads()[0]; // use the first gamepad
        if (gamepad != null) {

            var control = [Math.round(gamepad.axes[0]), Math.round(gamepad.axes[1])];
            
            //Check if same input
            var control =  inputMap[String(control[1]) + String(control[0])];
            var IsSame = previousControl == control;
            console.log(control);

            if (!IsSame) {
                CmdThread.postMessage("[A]" + control);
                if (previousControl != 0) {
                    CmdThread.postMessage("[D]" + previousControl);
                }
                previousControl = control;
            }
        }
    }, 10);
}

function ControllerText(id, status){
    let span = ID(id);

    if (span == null) {
        //Create new balise
        ID("StatusMenu").innerHTML += "<p>" + id +": <span class=\"nomController letterAnimationfade\" id=\""+ id +"\">Connected</span></p>";
        ID(id).style.color = "green";
    } else {
        span.hidden = true;
        span.innerText = status
        span.style.color = ((status == "Connected") ? 'green' : 'red');
        span.classList.remove('letterAnimationfade');
        setTimeout(() => { span.classList.add('letterAnimationfade'); span.hidden = false; }, 10); 
    }
}