let led = ID("led").style;
let batteryPercent = document.getElementById("BatterieLevel").style;
let control = document.getElementById("console");
let activeArrow = -1;

var actions = {
    1: ID("front"),
    2: ID("left"),
    3: ID("frontLeft"),
    4: ID("back"),
    6: ID("backleft"),
    8: ID("right"),
    9: ID("frontright"),
    12: ID("backright"),
}

function ChangeLed(status){
    let color;
    switch(status){
        case 'open':
            color = 'green';
            break
        case 'close':
            color = 'red';
            break;
        case 'pause':
            color = 'yellow';
            break;
        default:
            color = 'red'
            break;
    }
    led.backgroundColor = color;
    led.boxShadow = 'rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #441313 0 -1px 9px, ' + color + ' 0 2px 12px'
}

function UpdateBatteryLevel(percent){
    let color;
    percent = Number(percent);
    if(percent != 100){
        batteryPercent.borderTopRightRadius = '0px';
        batteryPercent.borderBottomRightRadius = '0px';
    }
    else{
        batteryPercent.borderRadius = '10px';

    }
    if(percent >= 80){
        color = 'rgb(100,242,36)';
    }
    else if(percent < 80 && percent >= 60){
        color = 'rgb(167,232,52)';
    }
    else if(percent < 60 && percent >= 40){
        color = "rgb(210,210,38)";

    }
    else if(percent < 40 && percent >= 20){
        color = "rgb(255,164,27)";
    }
    else if(percent < 20 && percent >= 0){
        color = "rgb(255,22,17)";
    }
    else{
        console.log("Mauvais pourcentage");
        return 0;
    }

    batteryPercent.width = percent + '%';
    console.log(String(percent) + "%;");

    batteryPercent.backgroundColor = color;
}

function addCommand(commandlist){

    commandlist.forEach(c => {
        let p = document.createElement('p');
        p.innerText = ' | code: ' + c;
        control.appendChild(p);
    });
}

function ChangeDirection(command){
    let arrow = actions[Number(command)];
    
    if(arrow != -1){
        activeArrow.src = "./img/arrow.png";
    }
    if(arrow != null){
        arrow.src = "./img/active_arrow.png";
        activeArrow = arrow;
    }
}


