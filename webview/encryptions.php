<html lang="en">
	<head>
	<link rel="stylesheet" type="text/css" href="./css/table.css">
	<title>Encryption</title>
	</head>
	
	<body>
		<div class="main">
		<?php
			include("header.php");
			
			$host=$_SESSION['host'];
			$port=$_SESSION['port'];
			$user=$_SESSION['user'];
			$pass=$_SESSION['pass'];
		
			$link = mysqli_connect($host, $user, $pass, NULL, $port);
			if($link == false) {
				echo 'ERROR: Could not connect. ' . mysqli_connect_error();
			}
			
			$query = "SET @cryptdb='show';";
			$result = mysqli_query($link, $query);
			$count = mysqli_num_rows($result);
			
			if ($count == 0) {
				echo 'No onions to show. Make sure there is an encrypted database with tables available';
			}
			else {
				$oEq = array("RND", "DET", "JOIN");
				$oOrd = array("RND", "OPE", "OPE-JOIN");
				$oSearch = array("SEARCH");
				$oAdd = array("HOM");
				
				echo '<p style="padding-left:2em;"><table><tbody>';
					$first=true;
					while($row=mysqli_fetch_assoc($result)) {
						if ($first) {
							$first = false;
							echo '<tr>';
							foreach($row as $key => $field) {
								echo '<th>'. $key .'</th>';
							}
							echo '<th>_layers</th>';
							echo '</tr>';
						}
						//save the values of the row to adjust the onion in the future
						echo '<tr>';
						$count=0;
						foreach($row as $key => $field) {
							switch ($count) {
								case 0:
									$_db=$field;
									break;
								case 1:
									$_table=$field;
									break;
								case 2:
									$_field=$field;
									break;
								case 3:
									$_onion=$field;
									break;
								case 4:
									$_level=$field;
									break;
							}
							echo '<td>'. $field .'</td>';
							$count=$count+1;
						}
						//know what options should be in the dropdown menu
						switch ($_onion) {
							case "oEq":
								$layers=$oEq;
								break;
							case "oOrder":
								$layers=$oOrd;
								break;
							case "oADD":
								$layers=$oAdd;
								break;
							case "oSearch":
								$layers=$oSearch;
								break;
							default:
								echo 'nothing ' . $_onion;
								break;
						}
						echo '<td style="text-align:center;">
								<form action="adjust.php?">
									<input type="hidden" name="db" value="'.$_db.'">
									<input type="hidden" name="table" value="'.$_table.'">
									<input type="hidden" name="field" value="'.$_field.'">
									<input type="hidden" name="onion" value="'.$_onion.'">
									<input type="hidden" name="level" value="'.$_level.'">
									<select name="choice" style="width:5em">';
										$cur_lvl=false;
										foreach ($layers as $key) {
											if ($key == $_level) {
												$cur_lvl=true;
											}
											if ($cur_lvl) {
												echo '<option value="'.$key.'">'.$key.'</option>';
											}
										}
								//future implementation to adjust onion
								//echo '</select><input type="submit" value="Submit">';
							echo '</form></td>';
						echo '</tr>';
					}
				echo '</tbody></table></p>';
			}
		?>
		</div>
	</body>
</html>
