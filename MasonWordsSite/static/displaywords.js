var worker_id ;
var list_of_words;
var list_id = 0;
var click_times = [];


$( document ).ready(function() {
	$('#big_text').hide();
	$('#submit').hide();
	$('#start_show_button').hide();
	$('#start_show_button').click(start_slideshow);
	setDefaultAction(start_slideshow);
	
	$.getJSON( "/get_words/", function( data ) {
  		list_of_words = data;
  		$('#start_show_button').show();
  		if (data.length==0) {
  			goToErrorPage();
  		}
	});
});

function start_slideshow() {
	var current_datetime = new Date() ;
	click_times.push( current_datetime.toJSON() ) ;

	$('#loading_div').hide();
	$('#big_text').show();
	document.getElementById("start_show_button").innerHTML = "click to continue";
	$('#start_show_button').hide();
	
	var runCount = 1;    
	var currenList = list_of_words[list_id]
	var maxRepeats = currenList.length;
	$('#changing_word').text(currenList[0]);
	$('#big_text').bigtext();	

	function timerMethod() {
		$('#changing_word').text( currenList[runCount] );
		$('#big_text').bigtext();
		runCount++;
		if(runCount > maxRepeats) { 
			clearInterval(timerId);
			$('#big_text').hide();

			if(list_id == list_of_words.length) {
				document.getElementById("click_times").value = click_times;
				$('#start_show_button').fadeOut("slow", function () {
					$('#submit').click();
				});
			}
			else {
				$('#start_show_button')[0].style["margin-top"] = "230px";
				$('#start_show_button').show();
			}
		}
	}

	var timerId = setInterval(timerMethod, 1200);    //1,200 milliseconds

	list_id = list_id +1;
}
