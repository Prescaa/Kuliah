<?php
require 'Model.php';

$id_buku = isset($_GET['id']) ? $_GET['id'] : null;
$bukuData = null;

if ($id_buku) {
    $bukuData = getData("SELECT * FROM buku WHERE id_buku = '$id_buku'");
    $bukuData = $bukuData ? $bukuData[0] : null;
}

if (isset($_POST['submit'])) {
    $data = [
        'judul_buku' => $_POST['judul_buku'],
        'penulis' => $_POST['penulis'],
        'penerbit' => $_POST['penerbit'],
        'tahun_terbit' => $_POST['tahun_terbit']
    ];

    if ($id_buku) {
        editData('buku', 'id_buku', $id_buku, $data);
        header('Location: Buku.php');
    } else {
        insertData('buku', $data);
        header('Location: Buku.php');
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $id_buku ? 'Edit' : 'Tambah' ?> Buku</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
        }
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0;
            font-size: 1.5rem;
        }
        .back-btn {
            color: white;
            text-decoration: none;
            font-size: 0.9rem;
        }
        .container {
            max-width: 600px;
            margin: 30px auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h2 {
            color: #2c3e50;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"],
        input[type="number"],
        textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .btn {
            display: inline-block;
            padding: 8px 16px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .btn:hover {
            background-color: #2980b9;
        }
        .btn-back {
            background-color: #95a5a6;
        }
        .btn-back:hover {
            background-color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1><i class="fas fa-book"></i> Layanan Perpustakaan</h1>
        <a href="Buku.php" class="back-btn"><i class="fas fa-arrow-left"></i> Kembali</a>
    </div>
    <div class="container">
        <h2><i class="fas fa-book"></i> <?= $id_buku ? 'Edit' : 'Tambah' ?> Buku</h2>
        <form action="FormBuku.php<?= $id_buku ? '?id=' . $id_buku : '' ?>" method="POST">
            <label for="judul_buku">Judul Buku</label>
            <input type="text" id="judul_buku" name="judul_buku" value="<?= $bukuData['judul_buku'] ?? '' ?>" required>
            <br><br>
            <label for="penulis">Penulis</label>
            <input type="text" id="penulis" name="penulis" value="<?= $bukuData['penulis'] ?? '' ?>" required>
            <br><br>
            <label for="penerbit">Penerbit</label>
            <input type="text" id="penerbit" name="penerbit" value="<?= $bukuData['penerbit'] ?? '' ?>" required>
            <br><br>
            <label for="tahun_terbit">Tahun Terbit</label>
            <input type="number" id="tahun_terbit" name="tahun_terbit" value="<?= $bukuData['tahun_terbit'] ?? '' ?>" required>
            <br><br>
            <button type="submit" name="submit"><?= $id_buku ? 'Update' : 'Simpan' ?></button>
        </form>
    </div>
</body>
</html>
