var QUESTIONS_NUM = 10;
var current_question = 1;

var questions = ["Upset","Hostile","Alert","Ashamed","Inspired","Nervous","Determined","Attentive","Afraid","Active"];
var sliderText = ['Not at all','Highly']

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
    
	document.getElementById("next").disabled = true;
});

function createQuestions() {
	qForm = document.getElementById("rumination_form");
	br = document.getElementById("afterQuestionsBreak");

	for (qInd=0; qInd<questions.length; qInd++) {
		var div = createDiv(sprintf('q%d_div',qInd+1),'control-group');	
		qTitle = createH2(div,'question_number',sprintf('%d) %s',qInd+1,questions[qInd]))
		qTitle.style["margin-left"] = "230px";
		createBR(div);
		createSliderQuestion(div, qInd+1, 1, 5, "layout-slider", 3, sliderText[0], sliderText[1]);
		div.style["margin-top"] = "120px";
		qForm.insertBefore(div,br);
	}
	$('#rumination_form').waitUntilExists(initSliders);
}

function initSliders() {
	for (qInd=0; qInd<questions.length; qInd++) {
		$(sprintf("#slider%d",qInd+1)).slider({
	        from: 1, 
	        to: 5, 
	        step: 1,
	        smooth: false,
	        skin: 'plastic',
	        scale: ['1',  '2',  '3',  '4', '5'],
		    onstatechange: function( value ) { checkSlider(this); }    
	      });
	}
}

function checkSlider(slider) {
//	slider = document.getElementById("slider" + current_question)
	document.getElementById("next").disabled = false;
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
			$('#question_number').fadeOut('slow');
			$('#q' + current_question + '_div').fadeOut("slow", function() {
			    current_question = current_question+1;
			    $('#question_number').fadeIn();
				$('#q' + current_question + '_div').fadeIn();
			});
		}
	}
}


