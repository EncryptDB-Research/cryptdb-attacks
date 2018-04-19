<html lang="en">
	<head>
	<link rel="stylesheet" type="text/css" href="./css/table.css">
	<title>Values</title>
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
			
			$table = $_GET['table'];
			$db = $_GET['db'];
			$query = "use " . $db . ";";
			$result = mysqli_query($link, $query);
			$query = "SELECT * FROM " . $table . ";";
			$result = mysqli_query($link, $query);
			$count = mysqli_num_rows($result);
			
			echo '<a href="tables.php?db='.$db.'"><- previous</a><br><br>';
			
			echo 'Values to insert:
					<form action="insert.php" method="post">
						<input type="hidden" name="db" value="'.$db.'">
						<input type="hidden" name="table" value="'.$table.'">
						<input type="text" name="values" placeholder="1, \'John\', \'Smith\', ..." style="width:16em;">
						<input type="submit" value="insert">
					</form>';
			
			if ($count == 0) {
				echo 'Oops. Looks like the table is empty';
			}
			else {
				echo '<p style="padding-left:2em;"><table><tbody>';
					$first=true;
					while($row=mysqli_fetch_assoc($result)) {
						if ($first) {
							$first = false;
							echo '<tr>';
							foreach($row as $key => $field) {
								echo '<th>'. $key .'</th>';
							}
							echo '</tr>';
						}
						echo '<tr>';
						foreach($row as $key => $field) {
								echo '<td>'. $field .'</td>';
							}
						echo '</tr>';
					}
				echo '</tbody></table></p>';
			}
		?>
		</div>
	</body>
</html>
