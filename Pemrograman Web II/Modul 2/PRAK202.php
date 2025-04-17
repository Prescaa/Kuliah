<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PRAK202</title> 
    <style>
        .required {color: #FF0000;}
    </style>
</head>
<body>
    <?php    
        $namaErr = $nimErr = $jeniskelaminErr = "";
        $nama = $nim = $jeniskelamin = "";
        $formSubmitted = false;

        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            if (empty($_POST["nama"])) {
                $namaErr = "nama tidak boleh kosong";
            } else {
                $nama = $_POST["nama"];
            }

            if (empty($_POST["nim"])) {
                $nimErr = "nim tidak boleh kosong";
            } else {
                $nim = $_POST["nim"];
            }

            if (empty($_POST["jeniskelamin"])) {
                $jeniskelaminErr = "jenis kelamin tidak boleh kosong";
            } else {
                $jeniskelamin = $_POST["jeniskelamin"];
            }

            if (!empty($nama) && !empty($nim) && !empty($jeniskelamin)) {
                $formSubmitted = true;
            }
        }
    ?>

    <form method="post" action="">
        Nama: <input type="text" name="nama" value="<?php echo $nama;?>"> <span class="required">*</span>
        <span class="required"><?php echo $namaErr;?></span><br>
        
        NIM: <input type="text" name="nim" value="<?php echo $nim;?>"> <span class="required">*</span>
        <span class="required"><?php echo $nimErr;?></span><br>
 
        Jenis Kelamin: <span class="required">* <?php echo $jeniskelaminErr;?></span><br>
        <input type="radio" name="jeniskelamin" value="Laki-Laki"> Laki-Laki<br>
        <input type="radio" name="jeniskelamin" value="Perempuan"> Perempuan<br>
        <input type="submit" name="submit" value="Submit">
    </form>

    <?php
        if ($formSubmitted) {
            echo "<h1>Output:</h1>";
            echo $nama . "<br>";
            echo $nim . "<br>";
            echo $jeniskelamin;
        }
    ?>
</body>
</html>