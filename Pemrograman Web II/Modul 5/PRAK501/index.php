<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menu</title>
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
            justify-content: center;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0;
            font-size: 1.5rem;
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
            text-align: center;
        }
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 30px;
        }
        .menu-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
            text-decoration: none;
            color: #2c3e50;
        }
        .menu-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            background-color: #f0f8ff;
        }
        .menu-card i {
            font-size: 40px;
            color: #3498db;
            margin-bottom: 15px;
        }
        .menu-card h3 {
            margin: 0;
            font-size: 1.2rem;
            font-weight: bold;
            text-decoration: none;
        }
    </style>
</head>
<body>

<div class="header">
    <h1><i class="fas fa-book"></i> Layanan Perpustakaan</h1>
</div>

<div class="container">
    <h2>Layanan Kami</h2>
    <div class="menu-grid">
        <a href="Member.php" class="menu-card">
            <i class="fas fa-users"></i>
            <h3>Data Member</h3>
        </a>
        <a href="Buku.php" class="menu-card">
            <i class="fas fa-book"></i>
            <h3>Koleksi Buku</h3>
        </a>
        <a href="Peminjaman.php" class="menu-card">
            <i class="fas fa-exchange-alt"></i>
            <h3>Peminjaman Buku</h3>
        </a>
    </div>
</div>

</body>
</html>
