<?= $this->extend('layout/template'); ?>
<?= $this->section('content'); ?>

<div class="card shadow text-center p-4">
    <img src="<?= base_url('images/' . $profil['gambar']) ?>" class="rounded-circle mx-auto d-block" style="width:120px; height:120px; object-fit:cover;">
    <hr class="w-50 mx-auto">

    <h4 class="mb-0"><?= $profil['nama']; ?></h4>
    <p class="mb-1 text-muted"><?= $profil['prodi']; ?></p>
    <p class="mb-3">NIM: <?= $profil['nim']; ?></p>

    <div class="text-start px-3">
        <p><strong>Hobi: </strong> <?= $profil['hobi']; ?></p>
        <p><strong>Skill: </strong> <?= $profil['skill']; ?></p>
        <p><strong>Deskripsi: </strong> Saya adalah mahasiswa aktif di program studi Teknologi Informasi yang tertarik dengan dunia desain. Untuk hobi, saya senang bepergian ke tempat jauh dan wisata alam dan saya juga sering berpartisipasi dalam kegiatan organisasi Himpunan Mahasiswa Teknologi Informasi dan UKM PP FIM ULM.</p>
    </div>

    <div class="mb-4">
        <a href="https://www.facebook.com/rifkyputra.mahardika.7" target="_blank" class="text-decoration-none mx-2"><i class="fab fa-facebook fa-lg"></i></a>
        <a href="https://www.instagram.com/rifkyputram70/" target="_blank" class="text-decoration-none mx-2"><i class="fab fa-instagram fa-lg"></i></a>
        <a href="https://wa.me/6285332123015" target="_blank" class="text-decoration-none mx-2"><i class="fab fa-whatsapp fa-lg"></i></a>
    </div>

    <a href="<?= base_url('beranda'); ?>" class="btn btn-secondary">Kembali ke Beranda</a>
</div>

<?= $this->endSection(); ?>
