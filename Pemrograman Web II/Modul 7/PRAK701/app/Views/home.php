<?= $this->include('templates/header') ?>
<link href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" rel="stylesheet">

<div class="text-center py-5 animate__animated animate__fadeInDown">
    <img src="<?= base_url('img/ULM_PNG.png') ?>" alt="Logo ULM" width="120">
    <h1 class="mt-3">Perpustakaan Universitas Lambung Mangkurat</h1>
    <p class="lead">Selamat datang di sistem informasi perpustakaan ULM.</p>
</div>

<div class="container mb-5 animate__animated animate__fadeInDown">
    <div class="row justify-content-center g-4">
        <div class="col-md-3">
            <div class="card shadow h-100">
                <div class="card-body text-center d-flex flex-column justify-content-between">
                    <div>
                        <h5 class="card-title">Akses Data Buku</h5>
                        <p class="card-text">Login untuk mengelola data buku.</p>
                    </div>
                    <a href="/login" class="btn btn-primary mt-3">Login Sekarang</a>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="text-center mb-5 animate__animated animate__fadeInDown">
    <p>Reach us at:</p>
    <a href="https://www.instagram.com/lambungmangkurat/?hl=id" target="_blank" class="me-3">
        <img src="https://cdn-icons-png.flaticon.com/512/1384/1384031.png" width="32" style="filter: grayscale(100%);" alt="Instagram">
    </a>
    <a href="https://www.facebook.com/lambungmangkurat/?locale=id_ID" target="_blank" class="me-3">
        <img src="https://cdn-icons-png.flaticon.com/512/1384/1384005.png" width="32" style="filter: grayscale(100%);" alt="Facebook">
    </a>
    <a href="https://www.youtube.com/@universitaslambungmangkura1814" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" width="32" style="filter: grayscale(100%);" alt="YouTube">
    </a>
</div>

<?= $this->include('templates/footer') ?>
