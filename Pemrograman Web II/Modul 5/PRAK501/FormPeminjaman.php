<?php
require 'Model.php';

$id = $_GET['id'] ?? '';
$data = ['id_member'=>'','id_buku'=>'','tgl_pinjam'=>'','tgl_kembali'=>''];

if ($id) {
    $result = getData("SELECT * FROM peminjaman WHERE id_peminjaman=$id");
    if (!empty($result)) {
        $data = $result[0];
    }
}

$members = getData("SELECT id_member, nama_member FROM member");
$buku = getData("SELECT id_buku, judul_buku FROM buku");

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = [
        'id_member' => $_POST['member_id'],
        'id_buku' => $_POST['buku_id'],
        'tgl_pinjam' => $_POST['tanggal_pinjam'],
        'tgl_kembali' => $_POST['tanggal_kembali']
    ];
    
    if ($id) {
        editData('peminjaman', 'id_peminjaman', $id, $input);
    } else {
        insertData('peminjaman', $input);
    }
    header("Location: Peminjaman.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $id ? 'Edit' : 'Tambah' ?> Peminjaman</title>
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
        select,
        input[type="date"] {
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
    <h1><i class="fas fa-exchange-alt"></i> Layanan Perpustakaan</h1>
    <a href="Peminjaman.php" class="back-btn"><i class="fas fa-arrow-left"></i> Kembali</a>
</div>
<div class="container">
    <h2><i class="fas fa-exchange-alt"></i> <?= $id ? 'Edit' : 'Tambah' ?> Peminjaman</h2>
    <form method="post">
        <div class="form-group">
            <label for="member_id">Member:</label>
            <select id="member_id" name="member_id" required>
                <?php foreach ($members as $m): ?>
                    <option value="<?= $m['id_member'] ?>" <?= $m['id_member'] == $data['id_member'] ? 'selected' : '' ?>>
                        <?= htmlspecialchars($m['nama_member']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
        <div class="form-group">
            <label for="buku_id">Buku:</label>
            <select id="buku_id" name="buku_id" required>
                <?php foreach ($buku as $b): ?>
                    <option value="<?= $b['id_buku'] ?>" <?= $b['id_buku'] == $data['id_buku'] ? 'selected' : '' ?>>
                        <?= htmlspecialchars($b['judul_buku']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
        <div class="form-group">
            <label for="tanggal_pinjam">Tgl Pinjam:</label>
            <input type="date" id="tanggal_pinjam" name="tanggal_pinjam" value="<?= htmlspecialchars($data['tgl_pinjam']) ?>" required>
        </div>
        <div class="form-group">
            <label for="tanggal_kembali">Tgl Kembali:</label>
            <input type="date" id="tanggal_kembali" name="tanggal_kembali" value="<?= htmlspecialchars($data['tgl_kembali']) ?>">
        </div>
        <button type="submit" class="btn"><i class="fas fa-save"></i> Simpan</button>
        <a href="Peminjaman.php" class="btn btn-back"><i class="fas fa-arrow-left"></i> Kembali</a>
    </form>
</div>
</body>
</html>