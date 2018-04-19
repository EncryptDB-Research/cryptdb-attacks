<html>
	<head>
		<title>dropping</title>
	</head>
	
	<body>
		<?php
			session_start();
			$type=$_GET['type'];
			$db=$_GET['db'];
			
			$link = mysqli_connect($_SESSION['host'], $_SESSION['user'], $_SESSION['pass'], NULL, $_SESSION['port']);
			if($link == false) {
				echo 'ERROR: Could not connect. ' . mysqli_connect_error();
				header("location:index.php");
			}
			
			if ($type == "database") {
				echo 'prev = db';
				$name=$db;
				$prev='location:databases.php';
			}
			elseif ($type == "table") {
				echo 'prev = table';
				$name=$_GET['table'];
				$prev='location:tables.php?db=' . $db;
				$query = "use " . $db . ";";
				$result = mysqli_query($link, $query);
			}
			
			//semi-colons at end of queries can break for some reason
			$query="DROP " . $type . " " . $name;
			$result = mysqli_query($link, $query);
			
			header($prev);
		?>
	</body>
</html>
