<?php
require 'Koneksi.php';

function getData($query) {
    $conn = getConnection();
    $result = mysqli_query($conn, $query);
    
    if (!$result) {
        die("Query error: " . mysqli_error($conn));
    }
    
    $rows = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $rows[] = $row;
    }
    return $rows;
}

function insertData($table, $data) {
    $conn = getConnection();
    unset($data['submit']);
    
    $columns = implode(", ", array_keys($data));
    $escaped = array_map(function($val) use ($conn) {
        return mysqli_real_escape_string($conn, $val);
    }, array_values($data));
    
    $values = "'" . implode("', '", $escaped) . "'";
    $query = "INSERT INTO $table ($columns) VALUES ($values)";
    
    if (!mysqli_query($conn, $query)) {
        die("Error inserting data: " . mysqli_error($conn));
    }
    
    return true;
}

function deleteData($table, $column, $value) {
    $conn = getConnection();
    $value = mysqli_real_escape_string($conn, $value);
    $query = "DELETE FROM $table WHERE $column = '$value'";
    
    if (!mysqli_query($conn, $query)) {
        die("Error deleting data: " . mysqli_error($conn));
    }
    
    return true;
}

function editData($table, $columnKey, $keyValue, $data) {
    $conn = getConnection();
    unset($data['submit']);
    
    $updates = [];
    foreach ($data as $column => $value) {
        $escapedValue = mysqli_real_escape_string($conn, $value);
        $updates[] = "$column = '$escapedValue'";
    }
    $updateStr = implode(", ", $updates);
    $keyValue = mysqli_real_escape_string($conn, $keyValue);
    $query = "UPDATE $table SET $updateStr WHERE $columnKey = '$keyValue'";
    
    if (!mysqli_query($conn, $query)) {
        die("Error updating data: " . mysqli_error($conn));
    }
    
    return true;
}
?>
