<?php
	$result = exec("F:/7th sem/Attendace_management_system-master/demoWeb.py");
	echo $result;	
	print("hdsb");
	$result_array = json_decode($result);
	foreach ($result_array as $row){
		echo $row."<BR>";
		
	}
?>
