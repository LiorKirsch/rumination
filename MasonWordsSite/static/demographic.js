$( document ).ready(function() {	
	var workerID=''
	$.getJSON( "/get_uuid/", function( data ) {
		workerID = data['workerID']
		if (workerID=="") {
			document.getElementById("workerID").type= "text";	
		} else {
			document.getElementById("worker_id_label").style.display= "none";
			document.getElementById("workerID").value = workerID;
		}	
	});	
});

