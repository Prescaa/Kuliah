<?= $this->extend('layout/template'); ?>
<?= $this->section('content'); ?>

<div class="card shadow text-center p-4">
    <h3>Hai! Selamat Datang</h3>
    <p>Selamat datang, anda sedang mengakses website yang dibuat oleh:</p>
    <hr class="w-50 mx-auto">

    <img src="<?= base_url('images/' . $mahasiswa['gambar']) ?>" class="rounded-circle mx-auto d-block" style="width:120px; height:120px; object-fit:cover;">
    <h4 class="mt-3"><?= $mahasiswa['nama']; ?></h4>
    <p>NIM: <?= $mahasiswa['nim']; ?></p>

    <a href="<?= base_url('profil'); ?>" class="btn btn-secondary">Lihat Profil</a>
</div>

<?= $this->endSection(); ?>
