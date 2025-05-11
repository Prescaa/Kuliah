<?php
require 'Model.php';

if (isset($_GET['delete'])) {
    deleteData('peminjaman', 'id_peminjaman', $_GET['delete']);
    header("Location: Peminjaman.php");
}

$peminjaman = getData("
    SELECT p.id_peminjaman, m.nama_member, b.judul_buku, p.tgl_pinjam, p.tgl_kembali
    FROM peminjaman p
    JOIN member m ON p.id_member = m.id_member
    JOIN buku b ON p.id_buku = b.id_buku
");
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Peminjaman</title>
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
            max-width: 1200px;
            margin: 30px auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h2 {
            color: #2c3e50;
        }
        .btn {
            display: inline-block;
            padding: 8px 16px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .btn:hover {
            background-color: #2980b9;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #2c3e50;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .action-links a {
            color: #3498db;
            text-decoration: none;
            margin-right: 10px;
        }
        .action-links a:hover {
            text-decoration: underline;
        }
        .empty-data {
            text-align: center;
            padding: 20px;
            color: #777;
            font-style: italic;
        }
        </style>
</head>
<body>
<div class="header">
    <h1><i class="fas fa-exchange-alt"></i> Layanan Perpustakaan</h1>
    <a href="index.php" class="back-btn"><i class="fas fa-arrow-left"></i> Kembali</a>
</div>
<div class="container">
    <h2><i class="fas fa-exchange-alt"></i> Data Peminjaman</h2>
    <a href="FormPeminjaman.php" class="btn"><i class="fas fa-plus"></i> Tambah Peminjaman</a>
    <?php if (empty($peminjaman)): ?>
        <div class="empty-data">Data belum ditambah</div>
    <?php else: ?>
    <table>
        <tr>
            <th>ID Peminjaman</th>
            <th>Member</th>
            <th>Buku</th>
            <th>Tgl Pinjam</th>
            <th>Tgl Kembali</th>
            <th>Aksi</th>
        </tr>
        <?php foreach ($peminjaman as $p): ?>
        <tr>
            <td><?= htmlspecialchars($p['id_peminjaman']) ?></td>
            <td><?= htmlspecialchars($p['nama_member']) ?></td>
            <td><?= htmlspecialchars($p['judul_buku']) ?></td>
            <td><?= htmlspecialchars($p['tgl_pinjam']) ?></td>
            <td><?= htmlspecialchars($p['tgl_kembali']) ?></td>
            <td class="action-links">
                <a href="FormPeminjaman.php?id=<?= $p['id_peminjaman'] ?>"><i class="fas fa-edit"></i> Edit</a>
                <a href="?delete=<?= $p['id_peminjaman'] ?>" onclick="return confirm('Hapus?')"><i class="fas fa-trash"></i> Hapus</a>
            </td>
        </tr>
        <?php endforeach; ?>
    </table>
    <?php endif; ?>
</div>
</body>
</html>