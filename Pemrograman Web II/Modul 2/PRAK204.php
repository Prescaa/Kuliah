<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PRAK204</title> 
    <style>
        .hasil { 
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
        <input type="submit" name="submit" value="Konversi">
        </form>

        <?php
          if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $nilai = $_POST["nilai"];

            if (is_numeric($nilai)){
                if ($nilai == 0) {
                    echo '<span class="hasil">Hasil: Nol </span>';
                } 
                else if ($nilai >= 1 && $nilai <= 9) {
                    echo '<span class="hasil">Hasil: Satuan </span>';
                } 
                else if ($nilai >= 10 && $nilai <= 99) {
                    echo '<span class="hasil">Hasil: Belasan </span>';
                } 
                else if ($nilai >= 100 && $nilai <= 999) {
                    echo '<span class="hasil">Hasil: Ratusan</span>';
                } 
                else {
                    echo '<span class="hasil">Anda Menginput Melebihi Limit Bilangan</span>';
                }
                }
            }

        ?>

</body>
</html>