<?php
include 'db_connect.php'; // Include the database connection

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $id = $_POST['id'];
    $title = $_POST['title'];
    $author = $_POST['author'];
    $price = $_POST['price'];

    // Update book in database
    if (updateBook($id, $title, $author, $price)) {
        echo "Book updated successfully";
    } else {
        echo "Error updating book";
    }
}
?>

