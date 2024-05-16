<?php
// Database connection parameters
$servername = "localhost";
$username = "root";
$password = " ";
$dbname = "bookstore";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Function to sanitize user inputs
function sanitizeInput($input) {
    global $conn;
    return $conn->real_escape_string($input);
}

// CRUD operations (addBook, getBooks, updateBook, deleteBook) will be defined here

// Close connection
//$conn->close(); // Uncomment this line if you want to close the connection in this file
?>

