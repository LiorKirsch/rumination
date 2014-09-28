var QUESTIONS_NUM = 9;
var current_question = 1;
//var questions = ["I spent some portion of the last 5 minutes thinking what I can do about the future",
//                 "In some portion of the last 5 minutes I thought about my current situation",
//                 "In some portion of the last 5 minutes, I had many thoughts",
//                 "In some portion of the last 5 minutes I thought about a topic that I didn't want to think about ",
//                 "In some portion of the last 5 minutes, my train of thought wandered from topic to topic",
//                 "I spent some portion of the last 5 minutes planning a specific event"];

var questions = ["I was thinking what I can do about the future",
                 "I thought about my current situation",
                 "I had many thoughts",
                 "I thought about a topic that I didn't want to think about",
                 "my train of thought wandered from topic to topic",
                 "I was planning a specific event"];

var options = ["disagree","somewhat disagree","somewhat agree","agree"];

$( document ).ready(function() {
	current_question = 0;
	createQuestions();
	hideQuestions();
	setDefaultAction(showNextQuestion);
	$('#questions_header').hide();
	$('#submit').hide()
	$('#next').hide()
	$('#next').click(showNextQuestion)
	$('#start').click(startQuestionnaire)
	initSliders();
    
	for (var i=1;i<=QUESTIONS_NUM;i++) {
		var radios = document.forms[0].elements["Q" + i + "RB"];
		if (typeof(radios)!='undefined') {
	  	    for (var j=0; j < radios.length; j++) {
	  	      radios[j].onclick=checkRBValues;
	  	    }
		}
	}

	document.getElementById("next").disabled = true;
});

function initSliders() {
    $("#slider8").slider({
        from: 0, 
        to: 10, 
        step: 1, 
        dimension: '',
        skin: 'plastic',
        scale: ['0', '|', '10'],
	    onstatechange: function( value ) { checkSlider(this); }    
      });

    $("#slider9").slider({
        from: 0, 
        to: 10, 
        step: 1, 
        dimension: '',
        skin: 'plastic',
        scale: ['0', '|', '10'],
	    onstatechange: function( value ) { checkSlider(this); }    
      });	
}

function createQuestions() {
	qForm = document.getElementById("rumination_form");
	br = document.getElementById("afterQuestionsBreak");
	
	for (qInd=0; qInd<questions.length; qInd++) {
		var qElm = createMultipleChoicesQuestion(qInd+1, questions[qInd], options);
		qElm.style["margin-top"] = "55px";
		qForm.insertBefore(qElm,br);
	}

	qInd = questions.length;
	var qElm = createMultipleChoicesQuestion(qInd+1, 
		"Please provide an estimate on how many different topics have you thought about in the last 5 minutes", 
		["1-3 topics","4-6 topics","7-9 topics","10 and more topics"]);
	qForm.insertBefore(qElm,br);
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
		$('#questions_header').fadeIn();
	});	
}

function showNextQuestion() {
	if (!document.getElementById("next").disabled) {
		document.getElementById("next").disabled = true;
		if (current_question<questions.length) { $('#questions_header').show(); } 
		else { 	$('#questions_header').fadeOut("slow");	}		
		if (current_question==QUESTIONS_NUM) {
			$('#rumination_div').fadeOut("slow", function () {
				$('#submit').click();	
			});
		} else {
			$('#q' + current_question + '_div').fadeOut("slow", function() {
			    current_question = current_question+1;
				$('#q' + current_question + '_div').fadeIn();
			});
		}
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

function checkSlider(slider) {
//	slider = document.getElementById("slider" + current_question)
	document.getElementById("next").disabled = false;
}

