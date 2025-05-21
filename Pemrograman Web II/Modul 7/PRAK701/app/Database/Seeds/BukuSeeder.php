<?php namespace App\Database\Seeds;

use CodeIgniter\Database\Seeder;

class BukuSeeder extends Seeder
{
    public function run()
    {
        $data = [
            [
                'judul' => 'Percy Jackson #1: The Lightning Thief',
                'penulis' => 'Rick Riordan',
                'penerbit' => 'Hyperion Books',
                'tahun_terbit' => 2005
            ],
            [
                'judul' => 'Light Novel: Stand By Me Doraemon',
                'penulis' => 'Fujiko F. Fujio',
                'penerbit' => 'Elex Media Komputindo',
                'tahun_terbit' => 2023
            ],
            [
                'judul' => 'Hunger Games #3: Mockingjay',
                'penulis' => 'Suzanne Collins',
                'penerbit' => 'Scholastic',
                'tahun_terbit' => 2010
            ]
        ];
        $this->db->table('buku')->insertBatch($data);
    }
}