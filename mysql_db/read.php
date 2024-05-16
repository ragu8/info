<?php
include 'db_connect.php'; // Include the database connection

// Get books from database
$books = getBooks();

// Display books
foreach ($books as $book) {
    echo "Title: " . $book['title'] . "<br>";
    echo "Author: " . $book['author'] . "<br>";
    echo "Price: $" . $book['price'] . "<br><br>";
}
?>

