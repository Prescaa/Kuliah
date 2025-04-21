<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soal4</title>
</head>
<body>
<?php
$jumlahBintang = 0;
$tampilkanBintang = false;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $jumlahBintang = isset($_POST['jumlah_bintang']) ? (int)$_POST['jumlah_bintang'] : 0;

    if (isset($_POST['klik'])) {
        if ($_POST['klik'] === 'submit') {
            $jumlahBintang = isset($_POST['input_bintang']) ? (int)$_POST['input_bintang'] : 0;
        } elseif ($_POST['klik'] === 'tambah') {
            $jumlahBintang++;
        } elseif ($_POST['klik'] === 'kurang') {
            $jumlahBintang = max(0, $jumlahBintang - 1);
        }
        $tampilkanBintang = true;
    }
}
?>

<form method="post" action="">
    <?php if (!$tampilkanBintang): ?>
        <label for="input_bintang">Jumlah bintang: </label>
        <input type="text" name="input_bintang" id="input_bintang"><br>
        <button type="submit" name="klik" value="submit">Submit</button>
    <?php else: ?>
        <p>Jumlah bintang <?php echo $jumlahBintang; ?></p>

        <?php
        for ($i = 0; $i < $jumlahBintang; $i++) {
            echo '<img src="images/bintangkuning.png" width="50" alt="Bintang">';
        }
        ?>

        <br><br>

        <input type="hidden" name="jumlah_bintang" value="<?php echo $jumlahBintang; ?>">

        <button type="submit" name="klik" value="tambah">Tambah</button>
        <button type="submit" name="klik" value="kurang">Kurang</button>
    <?php endif; ?>
</form>
</body>
</html>
