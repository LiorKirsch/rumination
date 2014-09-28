var QUESTIONS_NUM = 10;
var current_question = 1;
var questions = ["Think &ldquo;What am I doing to deserve this?&rdquo;",
                 "Analyse recent events to try to understand why you are depressed",
                 "Think &ldquo;Why do I always react this way?&rdquo;",
                 "Go away by yourself and think about why you feel this way",
                 "Write down what you are thinking and analyse it",
                 "Think about a recent situation, wishing it had gone better",
                 "Think &ldquo;Why do I have problems other people don&rsquo;t have?&rdquo;",
                 "Think &ldquo;Why can&rsquo;t I handle things better&rdquo;",
                 "Analyse your personality to try to understand why you are depressed",
                 "Go someplace alone to think about your feelings"];

$( document ).ready(function() {
	current_question = 0;
	createQuestions();
	hideQuestions();
	setDefaultAction(showNextQuestion);
	$('#submit').hide()
	$('#next').hide()
	$('#next').click(showNextQuestion)
	$('#start').click(startQuestionnaire)
	document.getElementById("next").disabled = true;

	for (var i=1;i<=QUESTIONS_NUM;i++) {
		var radios = document.forms[0].elements["Q" + i + "RB"];
  	    for (var j=0; j < radios.length; j++) {
  	      radios[j].onclick=checkRBValues;
  	    }
	}

});

function createQuestions() {
	qForm = document.getElementById("rumination_form");
	br = document.getElementById("afterQuestionsBreak");
	for (qInd=0; qInd<QUESTIONS_NUM; qInd++) {
		var qElm = createMultipleChoicesQuestion(qInd+1, questions[qInd], []);
		qForm.insertBefore(qElm,br);
	}
}

function hideQuestions() {
	for (var i=1;i<=QUESTIONS_NUM;i++) {
		$('#q' + i + '_div').hide();
	}
	$('#q' + current_question + '_div').fadeIn();
}

function startQuestionnaire(){
	$('#start').fadeOut('slow')
	$('#rumination_title').fadeOut("slow", function() {
		$('#next').fadeIn('slow')
	    current_question = current_question+1;
		$('#q1_div').fadeIn();
	});	
}

function showNextQuestion() {
	document.getElementById("next").disabled = true;
	if (current_question==QUESTIONS_NUM) {
		$('#rumination_form').fadeOut("slow", function () {
			$('#submit').click();	
		});
	} else {
		$('#q' + current_question + '_div').fadeOut("slow", function() {
		    current_question = current_question+1;
			$('#q' + current_question + '_div').fadeIn();
		});
	}
}

function checkRBValues() {
	var radios = document.forms[0].elements["Q" + current_question + "RB"];
	var oneChecked = false;
    for (var i=0; i < radios.length; i++) {
    	oneChecked = oneChecked || radios[i].checked; 
    }
    if (oneChecked) {
    	document.getElementById("next").disabled = false; 
    }
}
