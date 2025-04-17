<!DOCTYPE html>
<html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">   
    <title>PRAK201</title> 
    </head>
<body>
    <form method="post"action="">
     Nama: 1 <input type="text" name="name1"><br>
     Nama: 2 <input type="text" name="name2"><br>
     Nama: 3 <input type="text" name="name3"><br>
    <input type="submit" name="submit" value="Urutkan" />
    </form>

    <?php
        if(isset($_POST['submit'])){
            $names = [$_POST['name1'], $_POST['name2'], $_POST['name3']];
           
            sort($names);
            foreach ($names as $name) {
                echo "$name <br>";
            }
        }
    ?>
</body>
</html>