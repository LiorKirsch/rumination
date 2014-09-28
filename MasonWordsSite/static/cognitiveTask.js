var tries = 3;

$( document ).ready(function() {
	initGET(document);
	setDefaultAction(checkMathAnswer);
	if (isChrome()) { $('#onlyChrome').hide(); } 
	else { $('#ct_main').hide(); }
	initHiddenFields();	
	$('#submit').hide();
	$('#next').click(checkMathAnswer);
	document.getElementById('solution').focus();
});

function initHiddenFields() {
	var category_id = $_GET['category_id'];
	var worker_id = $_GET['worker_id'];
	var condition = $_GET['condition'];
	var experiment = $_GET['experiment'];
	
	document.getElementById("categoryID").value = category_id;
	document.getElementById("experiment").value = experiment;
	
	if (typeof condition!="undefined") {
		document.getElementById("condition").value = condition;
	}
	
	if (typeof worker_id=="undefined") {
		document.getElementById("workerID").value = '';	
		document.getElementById("fromAmazon").value = 0;
	} else {
		document.getElementById("workerID").value = worker_id;
		document.getElementById("fromAmazon").value = 1;
	}	
}

function checkMathAnswer() {
	var ans = document.getElementById('solution').value;
	if (ans=='3') {
		$('#solved')[0].value='true';
		$('#submit').click();	
	} else {
		setWarningLabel("Sorry, your answer is incorrect");
		document.getElementById('solution').value = '';
		tries=tries-1;
		if (tries==0) {
			$('#submit').click();
		}
	}
}

function setWarningLabel(text) {
	lbl = document.getElementById('warning_lbl');
	lbl.innerHTML = text;
}

