<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prak401</title>
    <style>
        table, td {
            border-collapse: collapse;
            border: 1px solid black;
            margin-top: 20px;
            padding: 10px;
        }
    </style>
</head>
<body>
    <form method="post" action="">
        Panjang: <input type="text" name="panjang" value="<?php echo isset($_POST['panjang']) ? $_POST['panjang'] : '' ?>"><br>
        Lebar: <input type="text" name="lebar" value="<?php echo isset($_POST['lebar']) ? $_POST['lebar'] : '' ?>"><br>
        Nilai: <input type="text" name="nilai" value="<?php echo isset($_POST['nilai']) ? $_POST['nilai'] : '' ?>"><br>
        <input type="submit" value="Cetak">
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $panjang = (int)$_POST["panjang"];
        $lebar = (int)$_POST["lebar"];
        $nilai = explode(" ", trim($_POST["nilai"]));

        if (count($nilai) != $panjang * $lebar) {
            echo "Panjang nilai tidak sesuai dengan ukuran matriks";
        } else {
            $matrix = array_chunk($nilai, $lebar);

            echo "<table>";
            foreach ($matrix as $row) {
                echo "<tr>";
                foreach ($row as $item) {
                    echo "<td>$item</td>";
                }
                echo "</tr>";
            }
            echo "</table>";
        }
    }
    ?>
</body>
</html>
