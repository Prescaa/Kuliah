<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data</title>
    <style>
        table, th, td{
            border: 1px solid black;
        }
    </style>
</head>
<body>
    <?php
        $samsung = array("Samsung Galaxy S22", "Samsung Galaxy S22+", "Samsung Galaxy A03", "Samsung Galaxy Xcover 5")
    ?>
    <table>
        <tr>
            <th>Daftar Smartphone Samsung</th>
        </tr>
        <?php
            foreach ($samsung as $hp) {
                echo "<tr><td>$hp</td></tr>";
            }
        ?>
    </table>
</body>
</html>