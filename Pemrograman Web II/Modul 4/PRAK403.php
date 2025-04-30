<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prak403</title>
    <style>
        table,th,td {
            border-collapse: collapse;
            border: 1px solid black;
            padding: 10px;
        }
        th {
            background-color: #808080;
        }
    </style>
</head>
<body>

<?php
$data = [["No" => 1,"Nama" => "Ridho", "Mata Kuliah" => [["nama_matkul" => "Pemrograman I", "SKS" => 2],["nama_matkul" => "Praktikum Pemrograman I", "SKS" => 1],["nama_matkul" => "Pengantar Lingkungan Lahan Basah", "SKS" => 2],["nama_matkul" => "Arsitektur Komputer", "SKS" => 3]]],
        ["No" => 2,"Nama" => "Ratna","Mata Kuliah" => [["nama_matkul" => "Basis Data I", "SKS" => 2],["nama_matkul" => "Praktikum Basis Data I", "SKS" => 1],["nama_matkul" => "Kalkulus", "SKS" => 3]]],
        ["No" => 3,"Nama" => "Tono","Mata Kuliah" => [["nama_matkul" => "Rekayasa Perangkat Lunak", "SKS" => 3],["nama_matkul" => "Analisis dan Perancangan Sistem", "SKS" => 3],["nama_matkul" => "Komputasi Awan", "SKS" => 3],["nama_matkul" => "Kecerdasan Bisnis", "SKS" => 3]]]];

foreach ($data as &$mahasiswa) {
    foreach ($mahasiswa['Mata Kuliah'] as $matkul) {
        $mahasiswa['Total SKS'] = ($mahasiswa['Total SKS'] ?? 0) + $matkul['SKS'];
    }
    $mahasiswa['Keterangan'] = ($mahasiswa['Total SKS'] < 7) ? "Revisi KRS" : "Tidak Revisi";
}
unset($mahasiswa);
        
echo "<table>";
echo "<tr>
        <th>No</th>
        <th>Nama</th>
        <th>Mata Kuliah diambil</th>
        <th>SKS</th>
        <th>Total SKS</th>
        <th>Keterangan</th>
        </tr>";
        
foreach ($data as $mahasiswa) {
    $first = true;
    foreach ($mahasiswa['Mata Kuliah'] as $matkul) {
        echo "<tr>";
        if ($first) {
            echo "<td>{$mahasiswa['No']}</td>";
            echo "<td>{$mahasiswa['Nama']}</td>";
        } else {
            echo "<td></td><td></td>";
        }
    
        echo "<td>{$matkul['nama_matkul']}</td>";
        echo "<td>{$matkul['SKS']}</td>";
        
        if ($first) {
            $warna = ($mahasiswa['Keterangan'] === "Revisi KRS") ? "background-color:red;" : "background-color:green;";
            echo "<td>{$mahasiswa['Total SKS']}</td>";
            echo "<td style='$warna'>{$mahasiswa['Keterangan']}</td>";
            $first = false;
        } else {
            echo "<td></td><td></td>";
        }
        
        echo "</tr>";
    }
}
        
echo "</table>";
?>
        
</body>
</html>