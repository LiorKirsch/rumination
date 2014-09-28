ERRORS_MESSAGES = {'dup': "Sorry, you can't participate in this task more than once.", 
				   'math': "Sorry, you can't participate in this task.",
				   'error': "Sorry, an error has accoured. Please notify the requester."};

DEFAULT_ERROR = "Sorry, an error has accoured. Please notify the requester.";

$( document ).ready(function() {
	initGET(document);	
	var errorType = $_GET['type'];
	$('#message')[0].innerHTML = getDictValue(ERRORS_MESSAGES, errorType, DEFAULT_ERROR);
});
