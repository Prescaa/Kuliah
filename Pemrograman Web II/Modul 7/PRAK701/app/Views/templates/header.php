<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Perpustakaan Universitas Lambung Mangkurat</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        html, body {
            height: 100%;
            margin: 0;
            display: flex;
            flex-direction: column;
            background-color: #f9f9f9;
        }
        main {
            flex: 1;
        }
        header {
            background-color: #FFD700; /* Kuning */
            padding: 1rem;
        }
        footer {
            background-color: #e0e0e0; /* Abu-abu */
            padding: 1rem;
            text-align: center;
        }
        .brand-logo {
            height: 60px;
        }
    </style>
</head>
<body>
    <header>
        <div class="container d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center">
                <img src="<?= base_url('img/ULM_PNG.png') ?>" alt="Logo ULM" width="120">
                <h5 class="m-0">Perpustakaan Universitas Lambung Mangkurat</h5>
            </div>
            <?php if (session()->get('isLoggedIn')): ?>
                <a href="/logout" class="btn btn-danger">Logout</a>
            <?php endif; ?>
        </div>
    </header>
    <main class="container mt-4">
