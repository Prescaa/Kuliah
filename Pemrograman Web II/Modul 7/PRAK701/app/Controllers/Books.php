<?php namespace App\Controllers;

use App\Models\ModelBuku;

class Books extends BaseController
{
    protected $model;
    
    public function __construct()
    {
        $this->model = new ModelBuku();
    }

    
    public function index()
    {
        $data['books'] = $this->model->findAll();
        return view('books/index', $data);
    }

    public function create()
    {
        return view('books/form');
    }

    public function store()
    {
        if ($this->model->save($this->request->getPost())) {
            return redirect()->to('/books')->with('success', 'Data berhasil disimpan!');
        }
        return redirect()->back()->withInput()->with('errors', $this->model->errors());
    }

    public function edit($id)
    {
        $data['book'] = $this->model->find($id);
        return view('books/form', $data);
    }

    public function update($id)
    {
        if ($this->model->update($id, $this->request->getPost())) {
            return redirect()->to('/books')->with('success', 'Data berhasil diperbarui!');
        }
        return redirect()->back()->withInput()->with('errors', $this->model->errors());
    }

    public function delete($id)
    {
        $this->model->delete($id);
        return redirect()->to('/books')->with('success', 'Data berhasil dihapus!');
    }
}