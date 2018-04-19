<html lang="en">
	<head>
	<link rel="stylesheet" type="text/css" href="./css/table.css">
	<title>Tables</title>
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
			
			$db = $_GET['db'];
			$query = "use " . $db . ";";
			$result = mysqli_query($link, $query);
			$query = "show tables;";
			$result = mysqli_query($link, $query);
			$count = mysqli_num_rows($result);
			
			echo '<a href="databases.php"><- previous</a><br><br>';
			
			echo 'Create table:
					<form action="create.php" method="post">
						<input type="hidden" name="db" value="'.$db.'">
						<input type="hidden" name="type" value="table">
						<input type="text" name="name" placeholder="name(val1 type1, val2 type2, ...)" style="width:16em;">
						<input type="submit" value="create">
					</form>';
			
			if ($count == 0) {
				echo 'No tables available to view';
			}
			else {
				echo '<p style="padding-left:2em;"><table><tbody>';
					$type="table";
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
							echo '<td><a href="values.php?table='.$field.'&amp;db='.$db.'">'.$field.'</a></td>';
							echo '<td style="text-align:center;">
									<b><a href="drop.php?type='.$type.'&amp;db='.$db.'&amp;table='.$field.'" style="color:red;">drop</a></b></td>';
						}
						echo '</tr>';
					}
				echo '</tbody></table></p>';
			}
		?>
		</div>
	</body>
</html>
