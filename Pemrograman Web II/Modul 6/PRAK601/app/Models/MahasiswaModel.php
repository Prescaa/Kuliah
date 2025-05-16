<?php

namespace App\Models;

use CodeIgniter\Model;

class MahasiswaModel extends Model
{
    public function getDataMhs()
    {
        return [
            'nama' => 'Rifky Putra Mahardika',
            'nim' => '2310817210023',
            'prodi' => 'Teknologi Informasi',
            'hobi' => 'Road trip ke luar kota, bermain GeoGuessr',
            'skill' => 'Edit poster, bisa pp Banjarmasin-Tanjung 1 kali seminggu',
            'gambar' => 'fotodika.jpg'
        ];
    }
}
