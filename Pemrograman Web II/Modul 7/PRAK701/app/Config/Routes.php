<?php

use CodeIgniter\Router\RouteCollection;

/**
 * @var RouteCollection $routes
 */

$routes->get('/', function () {
    return view('home');
});

// ROUTE LOGIN/LOGOUT
$routes->get('/login', 'Login::index');
$routes->post('/login', 'Login::processLogin');
$routes->get('/logout', 'Login::logout');
// ROUTE BOOKS (PROTECTED)
$routes->group('', ['filter' => 'auth'], function($routes) {
    $routes->get('/books', 'Books::index');
    $routes->get('/books/create', 'Books::create');
    $routes->post('/books', 'Books::store');
    $routes->get('/books/edit/(:num)', 'Books::edit/$1');
    $routes->post('/books/update/(:num)', 'Books::update/$1');
    $routes->post('/books/delete/(:num)', 'Books::delete/$1');
});