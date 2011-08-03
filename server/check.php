<?php

/*
check.php - ShowYourDesktop

Copyright (c) 2011 by William Edwards


 This component handles the creation of sessions and returns open ports on the 
 server for new SSH tunnels. It also stores connection information in the database.
*/

ini_set('display_errors',1);
error_reporting(E_ALL);

include("includes/config.inc.php");
include("includes/functions.php");

$password = $_GET['key'];
$request = $_GET['request'];

$link = mysql_connect($dbhost, $dbuser, $dbpass) or die("Error:  Unable to connect to database");
mysql_select_db($dbname, $link) or die("Error:  Unable to select database");

// If the request is from a sharing client, check for an existing entry in the database
if ($request == "share") {
	// Query the database for all currently used ports
	$query  = "SELECT port FROM clients";
	$result = mysql_query($query);
	$exceptions = array();

	// Add each port in the database to the array of ports not to use
	while($row = mysql_fetch_array($result, MYSQL_ASSOC))
	{
	      array_push($exceptions, $row['port']);
	}

	// Generate a random unused port between 30000 and 60000
	$port = rand_except(30000, 60000, $exceptions);

	// Insert a new entry into the database
	$sql = "INSERT INTO `clients`
			(`share_ip`,`port`,`password`) VALUES
			('${_SERVER['REMOTE_ADDR']}', '$port', '$password')";
	$result = mysql_query($sql);
	if (!$result) {
	    die('Invalid query: ' . mysql_error());
	}

	echo $port;
}

// If the request is from the viewer, lookup the session password and update the database
elseif ($request == "view") {
	// Update the database with the viewer's IP address
	$sql = "UPDATE `clients` SET view_ip='${_SERVER['REMOTE_ADDR']}' WHERE password='$password'";
	$result = mysql_query($sql);
	if (!$result) {
	    die('Invalid query: ' . mysql_error());
	}

	// Echo the port associated with the share session
        $sql  = "SELECT port FROM clients WHERE password='$password'";
	$result = mysql_query($sql);
	if (!$result) {
	    die('Invalid query: ' . mysql_error());
	}
	$port = mysql_fetch_array($result, MYSQL_ASSOC);

	echo $port['port'];

}

elseif ($request == "close") {

	// Remove the entry from the database
	$sql = "DELETE FROM `clients` WHERE password='$password'";
	$result = mysql_query($sql);

	if (!$result) {
	    die('Invalid query: ' . mysql_error());
	}

	echo "Closed";

}

else {

	echo "Invalid request";

}
?>
