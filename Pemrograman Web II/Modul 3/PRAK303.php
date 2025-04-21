<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soal3</title>
</head>
<body>
    <form method="post" action="">
        Batas Bawah: <input type="text" name="bawah" value="<?php echo isset($_POST['bawah']) ?$_POST['bawah'] : '' ?>"><br>
        Batas Atas: <input type="text" name="atas" value="<?php echo isset($_POST['atas']) ?$_POST['atas'] : '' ?>"><br>
        <input type="submit" value="Cetak">
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $bawah = (int)$_POST["bawah"];
        $atas = (int)$_POST["atas"];
        $star = "images/bintangkuning.png";

        if ($bawah <= $atas) {
            do {
                if (($bawah + 7) % 5 == 0 && $bawah + 7 != 0) {
                    echo "<img src='$star' width='20px' alt='star'> ";
                } else {
                    echo $bawah . " ";
                }

                $bawah++;
            } while ($bawah <= $atas);
        }
    }
    ?>
</body>
</html>
