<html>
	<head>
		<title>inserting</title>
	</head>
	
	<body>
		<?php
			session_start();
			$db=$_REQUEST['db'];
			$table=$_REQUEST['table'];
			$vals=$_REQUEST['values'];
			$prev="location:values.php?table=". $table ."&db=". $db;
			
			if ($vals == "") {
				echo 'vals empty';
				header($prev);
			}
			else {			
				$link = mysqli_connect($_SESSION['host'], $_SESSION['user'], $_SESSION['pass'], NULL, $_SESSION['port']);
				if($link == false) {
					echo 'ERROR: Could not connect. ' . mysqli_connect_error();
					header("location:index.php");
				}
				
				$query="USE ". $db;
				$result = mysqli_query($link, $query);
				$query="INSERT INTO ". $table ." VALUES(". $vals .", 0)";
				$result = mysqli_query($link, $query);
				
				header($prev);
			}
		?>
	</body>
</html>
