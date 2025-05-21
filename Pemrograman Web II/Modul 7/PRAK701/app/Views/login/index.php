<?= $this->include('templates/header') ?>

<div class="container mt-5">
    <h2>Login</h2>

    <?php if (session()->getFlashdata('warning')): ?>
        <div class="alert alert-warning">
            <?= session()->getFlashdata('warning') ?>
        </div>
    <?php endif; ?>

    <?php if (session()->getFlashdata('error')): ?>
        <div class="alert alert-danger">
            <?= session()->getFlashdata('error') ?>
        </div>
    <?php endif; ?>
    
    <form action="/login" method="post">
        <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" class="form-control" name="email" required>
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" name="password" required>
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
    </form>
</div>

<?= $this->include('templates/footer') ?>