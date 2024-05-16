<?php
include 'db_connect.php'; // Include the database connection

// Check if ID parameter is provided
if(isset($_GET['id'])) {
    $id = $_GET['id'];

    // Delete book from database
    if (deleteBook($id)) {
        echo "Book deleted successfully";
    } else {
        echo "Error deleting book";
    }
} else {
    echo "No ID provided";
}
?>

