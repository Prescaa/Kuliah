<?php
function getConnection() {
    $conn = new mysqli("localhost", "root", "", "perpustakaan");
    
    if ($conn->connect_error) {
        die("Koneksi gagal: " . $conn->connect_error);
    }
    
    return $conn;
}
?>
