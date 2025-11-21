<?php

$connection = mysqli_connect("localhost:13306", "root", "rootpassword", "Wytrychy-21-11");

$zapytanie = mysqli_query($connection, "SELECT * FROM aktorzy");

mysqli_query($connection, $zapytanie);

mysqli_close($connection);