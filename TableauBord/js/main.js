const xhttp = new XMLHttpRequest();

var timer;

xhttp.onload = () => {
    console.log("Retour: " + xhttp.responseText);
    updateUI(xhttp.responseText);
    timer = setTimeout(sendRequest, 1000);
}



function sendRequest() {
    xhttp.open("GET", "php/TableauBackEnd.php", true);
    xhttp.send();
}

function updateUI(data){
    data = JSON.parse(data);
    if(data){
        ChangeLed("open");
        ID("client").innerText = data["client"];
        ID("controller").innerText = data["controller"];
        UpdateBatteryLevel(data["power"]);
        addCommand(data["commandList"]);
        ChangeDirection(data["commandList"][data["commandList"].length -1]);
    }
}

sendRequest();