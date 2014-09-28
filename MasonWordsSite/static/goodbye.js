var uuid;

$( document ).ready(function() {
	var workerID=''
	var text='';
	$.getJSON( "/get_uuid/", function( data ) {
		uuid = data['uuid'];
		var elmUUID = document.getElementById("uuid");
		elmUUID.value = data['uuid'];
		workerID = data['workerID']
		fromAmazon = data['fromAmazon']
		
		if (fromAmazon=='0') {
			text = sprintf('Thanks %s, have a nice day!',workerID);
			document.getElementById("uuid").style.display= "none";
		} else {
			text = sprintf('Thanks %s, please return now to Amazon <br>and enter the following key:',workerID);
		}
		document.getElementById("message").innerHTML = text;
		document.getElementById("message").onclick = showLog
	});				
});

function showLog() {
	$.getJSON(sprintf("/get_summary/%s",uuid), function( data ) {
		document.getElementById("worker_summary").innerHTML = data['summary'];
	});	
//	window.open(sprintf('/logs/%s',uuid));
}