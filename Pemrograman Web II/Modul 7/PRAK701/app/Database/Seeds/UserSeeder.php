<?php namespace App\Database\Seeds;

use CodeIgniter\Database\Seeder;
use App\Models\ModelUser;

class UserSeeder extends Seeder
{
    public function run()
    {
        $model = new ModelUser();
        $model->insert([
            'username' => 'kominfo',
            'email' => 'kontak@kominfo.go.id',
            'password' => 'admin#1234'
        ]);
    }
}