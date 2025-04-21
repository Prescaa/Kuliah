<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soal1</title>
</head>
<body>
        <form method="post" action="">
            Jumlah Peserta: <input type="text" name="jumlah" value="<?php echo isset($_POST['jumlah']) ?$_POST['jumlah'] : '' ?>"><br>
            <input type="submit" value="Cetak">
        </form>
        
        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $jumlah = $_POST["jumlah"];
    
            $i = 1;
            while ($i <= $jumlah) {
                if ($i % 2 == 1) {
                    echo "<h2 style='color:red; font-weight:bold;'>Peserta ke-$i</h2>";
                } else {
                    echo "<h2 style='color:green; font-weight:bold;'>Peserta ke-$i</h2>";
                }
                $i++;
            }
        }
        ?>

</body>
</html>