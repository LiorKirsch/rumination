FREE_ASS_QUES_NUM = 5;
FREE_ASS_OPT_NUM = 4;

var current_chain=1;
var current_word=1;
var timerId;
var first;

var words = ['dog','cat','mouse','chair','table'];
var WORDS_ZIP_URL = '/get_english_dict/'
var wordsDic;
	
$( document ).ready(function() {
	first = true;
	$('#submit').hide();
	$('#next').click(showFirstChain);
	var formElm = document.getElementById('fat_form');
	getWordsDic();
	createFAT(formElm);
	setDefaultAction();
});

function getWordsDic() {
	JSZipUtils.getBinaryContent(WORDS_ZIP_URL, function(err, data) {
		  if(err) {
		    throw err; // or handle err
		  }
		  zip = new JSZip(data);
		  wordsStr = zip.file("words").asText()
		  wordsDic = wordsStr.split(wordsStr[1]);
		});	
}

function setDefaultAction() {
	// Set showNextWords as the default action in the form (when the user has clicked enter)
	$("body").keypress(function (event) {
	    if (event.which == 13) {
	        event.preventDefault();
	        if (first) {
	        	first = false;
	        	showFirstChain();
	        } else {
	        	if (legalCurrentWord()) {
	        		showNextWords();
	        	}
	        }
	    }
	});			
}

function timerMethod() {
	time_label = getTimer();
	if (time_label.innerHTML=='') {
		time_label.innerHTML = "1";
	} else {
		time = parseInt(time_label.innerHTML,10);
		time = time+1;
		time_label.innerHTML = time.toString();
	}
}


function createFAT(formElm) {
	for (var chain_index=1;chain_index<=FREE_ASS_QUES_NUM;chain_index++) {
		var wdiv = document.createElement('div');
		wdiv.id = 'chain' + chain_index + '_div';
		wdiv.className = 'control-group';
	
		createPrecursorInput('chain' + chain_index + '_w0', wdiv, words[chain_index-1]);
		createArrow(wdiv,'arrow' + chain_index + '_w0')
		for (var word_index=1; word_index<=FREE_ASS_OPT_NUM; word_index++) {
			createInput('chain' + chain_index + '_w' + word_index, wdiv);
			if (word_index<FREE_ASS_OPT_NUM) {
				createArrow(wdiv,'arrow' + chain_index + '_w' + word_index);
			}
		}
		wdiv.appendChild(document.createElement('br'))
		for (var word_index=0 ; word_index<=FREE_ASS_OPT_NUM; word_index++) {
			createTimeLabel(chain_index,word_index, wdiv)
		}
		formElm.appendChild(wdiv);
		$('#chain' + chain_index + '_div').hide();
		document.getElementById('time' + current_chain + '_w1').innerHTML = "1";
	}
}

function showFirstChain() {
	$('#next').click(showNextWords);
	$('#next')[0].value="Next";
	$('#chain1_div').fadeIn('slow', function() { 
		timerId = setInterval(timerMethod, 1000); 
	});	  
	setFocusOnCurrentWord();
}

function emptyWords() {
	for (var word_index=1 ; word_index<=FREE_ASS_OPT_NUM; word_index++) {
		var word = document.getElementById('chain' + current_chain + '_w' + word_index).value;
		if (word=="") { return true; }
	}
	return false;
}

function showNextWords() {
	if (emptyWords()) {
		setWarningLabal("You need to fill all the words");
	} else if (legalCurrentWord()) {
		if (current_chain==FREE_ASS_QUES_NUM) {
			$('#fat_main').fadeOut("slow", function () {
				$('#submit').click();	
			});
		} else {
			$('#chain' + current_chain + '_div').fadeOut("slow", function() {
				current_word = 1;
			    current_chain = current_chain+1;
				$('#chain' + current_chain + '_div').fadeIn(function() { 
					setFocusOnCurrentWord();
				});
			});
		}
	}
}

function createImage(div,id,src,className) {
	var img = document.createElement('img');
	img.src = src;
	img.id = id;
	img.className = className
	div.appendChild(img);	
}

function createArrow(div,id) {
	createImage(div, id, 'pics/arrow.png', 'arrow_img')
}

function createInput(id,div) {
	var inp = document.createElement('input');
	inp.id = id;
	inp.type = 'text';
	inp.className = 'word_input';
	inp.onblur = legalCurrentWord;
	inp.onfocus = wordOnFucus;
	div.appendChild(inp);
}

function legalCurrentWord() {
	if (divNotShown()) { return true; }
	var currentWord = getCurrentWord().value;
	var legalWord = false;
	if (currentWord=="") {
		setWarningLabal("The word cannot be empty")		
		setFocusOnCurrentWord();
	} else if (wordAlreadyAppear(currentWord)){
		setWarningLabal("You cannot use the same word twice")
		setFocusOnCurrentWord();
	} else if (!wordIsValidEnglish(currentWord)) {
		setWarningLabal(currentWord + " isn't a valid English word")
		setFocusOnCurrentWord();
	} else {
		legalWord = true;
		setWarningLabal("");
	}
	return legalWord;
}

function divNotShown() {
	return ($('#chain' + current_chain + '_div')[0].style[1]=="opacity");
}

function wordIsValidEnglish(word) {
	return (word.length>1 && jQuery.inArray(word, wordsDic)>=0);
}

function wordOnFucus(event) {
	var id = document.activeElement.id;
	current_word = parseInt(id[id.length-1],10);
}

function wordAlreadyAppear(word) {
	for (i=current_word-1; i>=0; i--) {
		var prevWord = document.getElementById('chain' + current_chain + '_w' + i).value;
		if (prevWord==word) { return true; }
	}
	return false;
}

function createPrecursorInput(id,div,value) {	
	var inp = document.createElement('input');
	inp.id = id;
	inp.type = 'text';
	inp.className = 'word_input'
	inp.readOnly = true;
	inp.value = value;			
	div.appendChild(inp);
}

function createTimeLabel(chain_index,word_index,div) {
	if (word_index==1) { time="0"; } else {	time="";}
	createLabel('time' + chain_index + '_w' + word_index, div, time,'word_input');
	createImage(div, '', 'pics/empty.png', 'arrow_img')
}

function createLabel(id,div,text,className) {
	var lbl = document.createElement('label');
	if (id!='') {
		lbl.id = id;
	}
	if (className!='') {
		lbl.className = className;
	}
	lbl.innerHTML = text;
	div.appendChild(lbl);
}

function setFocusOnCurrentWord() {
	document.getElementById('chain' + current_chain + '_w' + current_word).focus();
}

function getCurrentWord() {
	return document.getElementById('chain' + current_chain + '_w' + current_word);
}

function setWarningLabal(text) {
	lbl = document.getElementById('warning_lbl');
	lbl.innerHTML = text;
}

function getTimer() {
	return document.getElementById('time' + current_chain + '_w' + current_word);
}
