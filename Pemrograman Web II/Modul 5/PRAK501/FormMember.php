<?php
require 'Model.php';

$id_member = isset($_GET['id']) ? $_GET['id'] : null;
$memberData = null;

if ($id_member) {
    $memberData = getData("SELECT * FROM member WHERE id_member = '$id_member'");
    $memberData = $memberData ? $memberData[0] : null;
}

if (isset($_POST['submit'])) {
    $data = [
        'nama_member' => $_POST['nama_member'],
        'nomor_member' => $_POST['nomor_member'],
        'alamat' => $_POST['alamat'],
        'tgl_mendaftar' => $_POST['tgl_mendaftar'],
        'tgl_terakhir_bayar' => $_POST['tgl_terakhir_bayar']
    ];

    if ($id_member) {
        editData('member', 'id_member', $id_member, $data);
        header('Location: Member.php');
    } else {
        insertData('member', $data);
        header('Location: Member.php');
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $id_member ? 'Edit' : 'Tambah' ?> Member</title>
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
        input[type="datetime-local"],
        input[type="date"],
        textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        textarea {
            height: 80px;
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
        <h1><i class="fas fa-users"></i> Layanan Perpustakaan</h1>
        <a href="Member.php" class="back-btn"><i class="fas fa-arrow-left"></i> Kembali</a>
    </div>
    <div class="container">
        <h2><i class="fas fa-user-plus"></i> <?= $id_member ? 'Edit' : 'Tambah' ?> Member</h2>
        <form action="FormMember.php<?= $id_member ? '?id=' . $id_member : '' ?>" method="POST">
            <label for="nama_member">Nama Member</label>
            <input type="text" id="nama_member" name="nama_member" value="<?= $memberData['nama_member'] ?? '' ?>" required>
            <br><br>
            <label for="nomor_member">Nomor Member</label>
            <input type="text" id="nomor_member" name="nomor_member" value="<?= $memberData['nomor_member'] ?? '' ?>" required>
            <br><br>
            <label for="alamat">Alamat</label>
            <textarea id="alamat" name="alamat" required><?= $memberData['alamat'] ?? '' ?></textarea>
            <br><br>
            <label for="tgl_mendaftar">Tanggal Mendaftar</label>
            <input type="datetime-local" id="tgl_mendaftar" name="tgl_mendaftar" value="<?= $memberData['tgl_mendaftar'] ? date('Y-m-d\TH:i', strtotime($memberData['tgl_mendaftar'])) : '' ?>" required>
            <br><br>
            <label for="tgl_terakhir_bayar">Tanggal Terakhir Bayar</label>
            <input type="date" id="tgl_terakhir_bayar" name="tgl_terakhir_bayar" value="<?= $memberData['tgl_terakhir_bayar'] ? date('Y-m-d', strtotime($memberData['tgl_terakhir_bayar'])) : '' ?>" required>
            <br><br>
            <button type="submit" name="submit"><?= $id_member ? 'Update' : 'Simpan' ?></button>
        </form>
    </div>
</body>
</html>
