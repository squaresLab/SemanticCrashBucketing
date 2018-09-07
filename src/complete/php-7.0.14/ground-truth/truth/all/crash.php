<?php 
$xml = <<<EOF
<?xml version="1.0" ?>
<wddxPacket version="1.0">
	<struct>
		<var name="php_class_name">
			<string>Throwable</string>
                </var>
        </struct>
</wddxPacket>
EOF;
	$wddx = wddx_deserialize($xml);
	var_dump($wddx);
?>
