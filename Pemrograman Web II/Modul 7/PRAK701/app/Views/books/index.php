<?= $this->include('templates/header') ?>

<h1>Daftar Buku</h1>
<a href="/books/create" class="btn btn-primary mb-3">Tambah Buku</a>

<?php if (session()->getFlashdata('success')): ?>
<div class="alert alert-success"><?= session()->getFlashdata('success') ?></div>
<?php endif; ?>

<table class="table">
    <thead>
        <tr>
            <th>Judul</th>
            <th>Penulis</th>
            <th>Penerbit</th>
            <th>Tahun</th>
            <th>Aksi</th>
        </tr>
    </thead>
    <tbody>
        <?php foreach ($books as $book): ?>
        <tr>
            <td><?= esc($book['judul']) ?></td>
            <td><?= esc($book['penulis']) ?></td>
            <td><?= esc($book['penerbit']) ?></td>
            <td><?= esc($book['tahun_terbit']) ?></td>
            <td>
                <a href="/books/edit/<?= $book['id'] ?>" class="btn btn-sm btn-warning">Edit</a>
                <form action="/books/delete/<?= $book['id'] ?>" method="post" class="d-inline">
                    <?= csrf_field() ?>
                    <button type="submit" class="btn btn-sm btn-danger" onclick="return confirm('Konfirmasi Hapus?')">Hapus</button>
                </form>
            </td>
        </tr>
        <?php endforeach; ?>
    </tbody>
</table>

<?= $this->include('templates/footer') ?>