<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data</title>
    <style>
        table,th,td{
            border: 1px solid black;
        }
        th{
            font-size: 25px;
            height: 60px;
            background-color: red;
            text-align: center;
        }
    </style>
</head>
<body>
    <?php
        $samsung = array("samsung 1" => "Samsung Galaxy S22", "samsung 2" => "Samsung Galaxy S22+", "samsung 3" => "Samsung Galaxy A03", "samsung 4" => "Samsung Galaxy Xcover 5")
    ?>
    <table>
        <tr>
            <th>Daftar Smartphone Samsung</th>
        </tr>
        <tr>
            <td><?= $samsung['samsung 1']; ?></td>
        </tr>
        <tr>
            <td><?= $samsung['samsung 2']; ?></td>
        </tr>
        <tr>
            <td><?= $samsung['samsung 3']; ?></td>
        </tr>
        <tr>
            <td><?= $samsung['samsung 4']; ?></td>
        </tr>
    </table>
</body>
</html>