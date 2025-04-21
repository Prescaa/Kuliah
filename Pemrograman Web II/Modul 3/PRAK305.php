<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soal5</title>
</head>
<body>
    <form method="post" action="">
        <input type="text" name="input">
        <input type="submit" value="submit">
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $input = $_POST['input'];
        $length = strlen($input);

        echo "<br><b>Input:</b><br>";
        echo $input;

        echo "<br><br><b>Output:</b><br>";
        for ($i = 0; $i < $length; $i++) {
            $char = $input[$i];
            $output = strtoupper($char);
            $output .= str_repeat(strtolower($char), $length - 1);
            echo $output;
        }
    }
    ?>
</body>
</html>