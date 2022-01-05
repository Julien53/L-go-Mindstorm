<?php
    error_reporting(E_ALL);
    $port = 8082;
    $address = "127.0.0.1";

    if(!($socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP))){
        echo "[error]Création du socket échoué: " . socket_strerror(socket_last_error()) . "\n";
    }
    else{
        
        if(!($result = socket_connect($socket, $address, $port))){
            echo "[error]La connection à échoué: " . socket_strerror(socket_last_error()) . "\n";
        }
        else{
            $isFinish = true;
            $dataOut = array();
            $commandList = array();
            while($isFinish){
                $dataIn = socket_read($socket, 2048);
                
                if(startsWith($dataIn, "[info]")){
                    $info = explode("|", explode("[info]",$dataIn)[1]);
                    $dataOut += [
                        'controller' => $info[0],
                        'client' => $info[1],
                        'power' => $info[2]
                    ];

                }
                elseif(startsWith($dataIn, "[comm]")){
                    array_push($commandList, explode("[comm]",$dataIn)[1]);
                    socket_send($socket, "ok", 2, null);
                }
                elseif(startsWith($dataIn, '[end]')){
                    $isFinish = false;
                    $dataOut += ["commandList" => $commandList];
                    echo json_encode($dataOut);
                } else {
                    echo $dataIn;
                }
            }
        }
    }

    function startsWith( $haystack, $needle ) {
        $length = strlen( $needle );
        return substr( $haystack, 0, $length ) === $needle;
   }
    

?>