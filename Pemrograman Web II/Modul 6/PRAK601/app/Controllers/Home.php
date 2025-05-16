<?php

namespace App\Controllers;

use App\Models\MahasiswaModel;

class Home extends BaseController
{
    public function index()
    {
        $model = new MahasiswaModel();
        $data['mahasiswa'] = $model->getDataMhs();
        return view('beranda', $data);
    }

    public function profil()
    {
        $model = new MahasiswaModel();
        $data['profil'] = $model->getDataMhs();
        return view('profil', $data);
    }
}
