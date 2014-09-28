var click_num = 0;
var mdist = 0; // mouse acc distance
var prev_mx = 0 ;
var prev_my = 0 ; 
var first = true;
var elapsed_seconds = 60 * 5;
var click_time;
var times_diff = [];

$( document ).ready(function() {
	$('#submit').hide();
	$('#start_game_button').click(start);
	$('#click_times')[0].innerHTML = '0';
	$('#timer')[0].innerHTML = '05:00';	
});

function start() {
	$('#start_div').fadeOut("slow", function() {
		$('#game_div').fadeIn(function() {
			setInterval(timerFunction, 1000);
			click_time = new Date();
		});
	});	
}

function gameClick(mx,my) {
	click_num = parseInt($('#click_times')[0].innerHTML,10);
	click_num = click_num+1;
	$('#click_times')[0].innerHTML = click_num.toString();
	if (first) { 
		first = false;
	} else { 
		mdist = mdist + Math.sqrt((prev_mx-mx)*(prev_mx-mx)+(prev_my-my)*(prev_my-my)); 
		times_diff.push((new Date()-click_time)/1000)
	}
	prev_mx = mx;
	prev_my = my;
	click_time = new Date();
}

function timerFunction() {
	elapsed_seconds = elapsed_seconds - 1;
	if (elapsed_seconds>0) {
		$('#timer')[0].innerHTML = get_elapsed_time_string(elapsed_seconds);
	} else {
		saveToJSON();
		$('#submit').click();	
	}
}

function saveToJSON() {
	// Add last time diff
	times_diff.push((new Date()-click_time)/1000)
	max_time_diff = Math.max.apply(null, times_diff);
    jsonObj = [];
    var data = {};
    data['clicks'] = click_num;
    data['distance'] = mdist;
    data['times_diff'] = times_diff;
    data['max_time_diff'] = max_time_diff;
	jsonObj.push(data);
    jsonString = JSON.stringify(jsonObj);
    document.getElementById('data').value = jsonString;
    console.log(jsonString);    
}
