<?php
require 'Model.php';

if (isset($_GET['delete'])) {
    $idBuku = $_GET['delete'];

    $isDipinjam = getData("SELECT COUNT(*) as jumlah FROM peminjaman WHERE id_buku = $idBuku")[0]['jumlah'];

    if ($isDipinjam > 0) {
        echo "<script>alert('Buku tidak bisa dihapus karena sedang dipinjam!'); window.location.href='Buku.php';</script>";
    } else {
        deleteData('buku', 'id_buku', $idBuku);
        header("Location: Buku.php");
        exit;
    }
}

$buku = getData("SELECT * FROM buku");
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Buku</title>
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
            background-color:rgb(137, 152, 167);
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
        <h1><i class="fas fa-book"></i> Layanan Perpustakaan</h1>
        <a href="index.php" class="back-btn"><i class="fas fa-arrow-left"></i> Kembali</a>
    </div>
    <div class="container">
        <h2><i class="fas fa-book"></i> Koleksi Buku</h2>
        <a href="FormBuku.php" class="btn"><i class="fas fa-plus"></i> Tambah Buku</a>
        <?php if (empty($buku)): ?>
            <div class="empty-data">Data buku belum ditambah</div>
        <?php else: ?>
        <table>
            <tr>
                <th>ID Buku</th>
                <th>Judul</th>
                <th>Penulis</th>
                <th>Penerbit</th>
                <th>Tahun Terbit</th>
                <th>Aksi</th>
            </tr>
            <?php foreach ($buku as $b): ?>
            <tr>
                <td><?= $b['id_buku'] ?></td>
                <td><?= $b['judul_buku'] ?></td>
                <td><?= $b['penulis'] ?></td>
                <td><?= $b['penerbit'] ?></td>
                <td><?= $b['tahun_terbit'] ?></td>
                <td class="action-links">
                    <a href="FormBuku.php?id=<?= $b['id_buku'] ?>"><i class="fas fa-edit"></i> Edit</a>
                    <a href="?delete=<?= $b['id_buku'] ?>" onclick="return confirm('Hapus buku ini?')"><i class="fas fa-trash"></i> Hapus</a>
                </td>
            </tr>
            <?php endforeach; ?>
        </table>
        <?php endif; ?>
    </div>
</body>
</html>
