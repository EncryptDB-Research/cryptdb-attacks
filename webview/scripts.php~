<html lang="en">
	<head>
	<link rel="stylesheet" type="text/css" href="./css/table.css">
	<title>Scripts</title>
	</head>
	
	<body>
		<div class="main">
		<?php
			include("header.php");
			
			$link = mysqli_connect($_SESSION['host'], $_SESSION['user'], $_SESSION['pass'], NULL, $_SESSION['port']);
			if($link == false) {
				echo 'ERROR: Could not connect. ' . mysqli_connect_error();
				header("location:index.php");
			}
			
			$query = "SHOW DATABASES;";
			$result = mysqli_query($link, $query);
			$count = mysqli_num_rows($result);
		?>
		</div>
	</body>
</html>
