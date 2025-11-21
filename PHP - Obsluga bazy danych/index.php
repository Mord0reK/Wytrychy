<?php

$connection = mysqli_connect("100.109.170.34:13306", "root", "rootpassword", "wytrychy_db") or die("Problem z połączeniem.");

$zapytanie = mysqli_query($connection, "SELECT * FROM aktorzy");

mysqli_query($connection, $zapytanie);

mysqli_close($connection);