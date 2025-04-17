<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PRAK203</title> 
    <style>
        .result { 
            font-weight: bold; 
            font-size: 20px;
            margin-top: 20px;
            display: block;
        }
    </style>
</head>
<body>
    <form method="post" action="">
        Nilai: <input type="text" name="nilai" value="<?php echo isset($_POST['nilai']) ?$_POST['nilai'] : '' ?>"><br>
        Dari:<br>
        <input type="radio" name="dari" value="celcius" <?php echo isset($_POST['dari']) && $_POST['dari'] == 'celcius' ? 'checked' : '' ?>> Celcius<br>
        <input type="radio" name="dari" value="fahrenheit" <?php echo isset($_POST['dari']) && $_POST['dari'] == 'fahrenheit' ? 'checked' : '' ?>> Fahrenheit<br>
        <input type="radio" name="dari" value="rheamur" <?php echo isset($_POST['dari']) && $_POST['dari'] == 'rheamur' ? 'checked' : '' ?>> Rheamur<br>
        <input type="radio" name="dari" value="kelvin" <?php echo isset($_POST['dari']) && $_POST['dari'] == 'kelvin' ? 'checked' : '' ?>> Kelvin<br>
        
        Ke:<br>
        <input type="radio" name="ke" value="celcius" <?php echo isset($_POST['ke']) && $_POST['ke'] == 'celcius' ? 'checked' : '' ?>> Celcius<br>
        <input type="radio" name="ke" value="fahrenheit" <?php echo isset($_POST['ke']) && $_POST['ke'] == 'fahrenheit' ? 'checked' : '' ?>> Fahrenheit<br>
        <input type="radio" name="ke" value="rheamur" <?php echo isset($_POST['ke']) && $_POST['ke'] == 'rheamur' ? 'checked' : '' ?>> Rheamur<br>
        <input type="radio" name="ke" value="kelvin" <?php echo isset($_POST['ke']) && $_POST['ke'] == 'kelvin' ? 'checked' : '' ?>> Kelvin<br>
        
        <input type="submit" name="submit" value="Konversi">
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $nilai = floatval($_POST['nilai'] ?? 0);
        $dari = $_POST['dari'] ?? '';
        $ke = $_POST['ke'] ?? '';

        if ($dari && $ke) {
            if ($dari == 'celcius') {
                $celcius = $nilai;
            } elseif ($dari == 'fahrenheit') {
                $celcius = ($nilai - 32) / 1.8;
            } elseif ($dari == 'rheamur') {
                $celcius = $nilai / 0.8;
            } elseif ($dari == 'kelvin') {
                $celcius = $nilai - 273.15;
            } 

            if ($ke == 'celcius') {
                $result = $celcius;
                $symbol = '°C';
            } elseif ($ke == 'fahrenheit') {
                $result = ($celcius * 1.8) + 32;
                $symbol = '°F';
            } elseif ($ke == 'rheamur') {
                $result = $celcius * 0.8;
                $symbol = '°R';
            } elseif ($ke == 'kelvin') {
                $result = $celcius + 273.15;
                $symbol = 'K';
            }

            echo '<span class="result">Hasil Konversi: ' . round($result, 1) . ' ' . $symbol . '</span>';
        }
    }
    ?>
</body>
</html>