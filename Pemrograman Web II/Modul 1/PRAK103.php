<?php
    $celcius = 37.841;
    $reamur = round($celcius*0.8,4);
    $fahrenheit = round(($celcius*1.8)+32,4);
    $kelvin = round($celcius+273.15,4);
    echo "Fahrenheit (F) = $fahrenheit<br>";
    echo "Reamur (R) = $reamur<br>";
    echo "Kelvin (K) = $kelvin<br>";
?>