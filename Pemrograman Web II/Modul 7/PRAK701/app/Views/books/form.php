<?= $this->include('templates/header') ?>

<h1><?= isset($book) ? 'Edit Buku' : 'Tambah Buku' ?></h1>

<?php if (session()->getFlashdata('errors')): ?>
<div class="alert alert-danger">
    <?php foreach (session()->getFlashdata('errors') as $error): ?>
        <p><?= $error ?></p>
    <?php endforeach; ?>
</div>
<?php endif; ?>

<form method="post" action="<?= isset($book) ? '/books/update/'.$book['id'] : '/books' ?>">
    <div class="mb-3">
        <label for="judul" class="form-label">Judul</label>
        <input type="text" class="form-control" name="judul" 
               value="<?= isset($book) ? esc($book['judul']) : '' ?>" required>
    </div>
    <div class="mb-3">
        <label for="penulis" class="form-label">Penulis</label>
        <input type="text" class="form-control" name="penulis" 
               value="<?= isset($book) ? esc($book['penulis']) : '' ?>" required>
    </div>
    <div class="mb-3">
        <label for="penerbit" class="form-label">Penerbit</label>
        <input type="text" class="form-control" name="penerbit" 
               value="<?= isset($book) ? esc($book['penerbit']) : '' ?>" required>
    </div>
    <div class="mb-3">
        <label for="tahun_terbit" class="form-label">Tahun Terbit</label>
        <input type="number" class="form-control" name="tahun_terbit" 
               value="<?= isset($book) ? esc($book['tahun_terbit']) : '' ?>" required>
    </div>
    <button type="submit" class="btn btn-primary">Simpan</button>
    <a href="/books" class="btn btn-secondary">Kembali</a>
</form>

<?= $this->include('templates/footer') ?>