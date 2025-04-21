<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soal2</title>
    <style>
        .output {
            display: inline-block;
            line-height: 1.2;
        }
        .spasi {
            display: inline-block;
            width: 20px;
        }
        .gambar {
            width: 20px;
            height: 20px;
        }
    </style>
</head>
<body>
    <form method="post" action="">
        Tinggi: <input type="text" name="jumlah" value="<?php echo isset($_POST['jumlah']) ?$_POST['jumlah'] : '' ?>"><br>
        Alamat Gambar: <input type="text" name="gambar" value="<?php echo isset($_POST['gambar']) ?$_POST['gambar'] : '' ?>"><br>
        <input type="submit" value="Cetak">
    </form>
    
    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $jumlah = (int)$_POST["jumlah"];
        $gambar = $_POST["gambar"];

        if (!empty($jumlah) && !empty($gambar)) {
            echo "<span class='output'>";
            $i = $jumlah;
            while ($i >= 1) {
                $spasi = $jumlah - $i;
                for ($s = 0; $s < $spasi; $s++) {
                    echo "<span class='spasi'></span>";
                }

                for ($j = 1; $j <= $i; $j++) {
                    echo "<img src='$gambar' class='gambar'>";
                }

                echo "<br>";
                $i--;
            }
            echo "</span>";
        }
    }
    ?>
</body>
</html>
