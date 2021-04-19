<?php include_once('website/home.html'); 
echo '<link href="website/style.css" rel="stylesheet">';
echo '<script type="text/javascript" src="website/app.js"></script>';
shell_exec('python3 ./perspectiveserver.py')
?>