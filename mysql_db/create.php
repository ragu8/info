<?php
include 'db_connect.php'; // Include the database connection

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $title = $_POST['title'];
    $author = $_POST['author'];
    $price = $_POST['price'];

    // Add book to database
    if (addBook($title, $author, $price)) {
        echo "Book added successfully";
    } else {
        echo "Error adding book";
    }
}
?>

