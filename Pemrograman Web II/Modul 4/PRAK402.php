<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prak402</title>
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
$data = [
    ["nama" => "Andi", "nim" => "2101001", "uts" => 87, "uas" => 65],
    ["nama" => "Budi", "nim" => "2101002", "uts" => 76, "uas" => 79],
    ["nama" => "Tono", "nim" => "2101003", "uts" => 50, "uas" => 41],
    ["nama" => "Jessica", "nim" => "2101004", "uts" => 60, "uas" => 75]
];

function Konversi($uts, $uas) {
    $nilai = ($uts * 0.4) + ($uas * 0.6);
    $nilai = round($nilai, 1);

    if ($nilai >= 80) {
        $huruf = 'A';
    } elseif ($nilai >= 70) {
        $huruf = 'B';
    } elseif ($nilai >= 60) {
        $huruf = 'C';
    } elseif ($nilai >= 50) {
        $huruf = 'D';
    } elseif ($nilai < 50) {
        $huruf = 'E';
    }

    return [$nilai, $huruf];
}

echo "<table>";
echo "<tr>
        <th>Nama</th>
        <th>NIM</th>
        <th>Nilai UTS</th>
        <th>Nilai UAS</th>
        <th>Nilai Akhir</th>
        <th>Huruf</th>
      </tr>";

foreach ($data as $mhs) {
    list($nilai, $huruf) = Konversi($mhs["uts"], $mhs["uas"]);

    echo "<tr>
            <td>{$mhs['nama']}</td>
            <td>{$mhs['nim']}</td>
            <td>{$mhs['uts']}</td>
            <td>{$mhs['uas']}</td>
            <td>{$nilai}</td>
            <td>{$huruf}</td>
          </tr>";
}

echo "</table>";
?>

</body>
</html>
