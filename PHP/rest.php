<?php   
    $arrContextOptions=array(
        "ssl"=>array(
            "verify_peer"=>false,
            "verify_peer_name"=>false,
        ),
    );  
    
    $response = file_get_contents("https://xkcd.com/info.0.json", false, stream_context_create($arrContextOptions));
    
    $dataJson = json_decode($response, true);
    echo $dataJson['img'].PHP_EOL;
?>;
