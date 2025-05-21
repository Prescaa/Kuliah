<?php namespace App\Controllers;

use App\Models\ModelUser;

class Login extends BaseController
{
    public function index()
    {
        if ($this->request->getMethod() == 'post') {
            return $this->processLogin();
        }
        
        return view('login/index');
    }
    
    public function processLogin()
    {
        $model = new ModelUser();
        $email = $this->request->getPost('email');
        $password = $this->request->getPost('password');
        
        $user = $model->where('email', $email)->first();
        
        if ($user && password_verify($password, $user['password'])) {
            session()->set('isLoggedIn', true);
            return redirect()->to('/books');
        }
        
        return redirect()->back()->with('error', 'Email/Password salah!');
    }
    
    public function logout()
    {
        session()->remove('isLoggedIn');
        return redirect()->to('/login');
    }
}