<html lang="en">
	<head>
	<link rel="stylesheet" type="text/css" href="./css/table.css">
	<title>Databases</title>
	</head>
	
	<body>
		<div class="main">
		<?php
			include("header.php");
			if(!isset($_SESSION['user'])) {
				$_SESSION['host']=$_REQUEST['host'];
				$_SESSION['port']=$_REQUEST['port'];
				$_SESSION['user']=$_REQUEST['user'];
				$_SESSION['pass']=$_REQUEST['pass'];
			}
			$link = mysqli_connect($_SESSION['host'], $_SESSION['user'], $_SESSION['pass'], NULL, $_SESSION['port']);
			if($link == false) {
				echo 'ERROR: Could not connect. ' . mysqli_connect_error();
				header("location:index.php");
			}
			
			$query = "SHOW DATABASES;";
			$result = mysqli_query($link, $query);
			$count = mysqli_num_rows($result);
			
			echo 'Create database:
					<form action="create.php" method="post">
						<input type="hidden" name="type" value="database">
						<input type="text" name="name" placeholder="database name" style="width:16em;">
						<input type="submit" value="create">
					</form>';
					
			if ($count == 0) {
				echo 'No databases available';
			}
			else {
				echo '<p style="padding-left:2em;"><table><tbody>';
					$type="database";
					$first=true;
					while($row=mysqli_fetch_assoc($result)) {
						if ($first) {
							$first = false;
							echo '<tr>';
							foreach($row as $key => $field) {
								echo '<th>'. $key .'</th>';
							}
							echo '<th>Action</th>';
							echo '</tr>';
						}
						echo '<tr>';
						foreach($row as $key => $field) {
							if ($field != "mysql" and
							$field != "performance_schema" and
							$field != "information_schema" and
							$field != "remote_db" and
							$field != "cryptdb_udf" and
							$field != "phpmyadmin") {
								echo '<td><a href="tables.php?db='. $field .'">'. $field .'</a></td>';
								echo '<td style="text-align:center;">';
								echo '<b><a href="drop.php?type='.$type.'&amp;db='.$field.'" style="color:red;">drop</a></b></td>';
							}
							else {
								echo '<td>'. $field .'</td>';
								echo '<td style="text-align:center;">';
								echo 'N/A';
							}
							echo '</td>';
						}
						echo '</tr>';
					}
				echo '</tbody></table></p>';
			}
		?>
		</div>
	</body>
</html>
