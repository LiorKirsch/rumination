FREE_ASS_QUES_NUM = 5;
FREE_ASS_OPT_NUM = 1;

var current_chain=1;
var current_word=1;
var timerId;
var first;
var list_of_words;

var words = ['dog','cat','mouse','chair','table'];
var WORDS_ZIP_URL = '/get_english_dict/'
var wordsDic;
var blockKeyPress=false;
	
$( document ).ready(function() {
	first = true;
	$('#submit').hide();
	$('#next').click(showFirstChain);
	getWords();
	getWordsDic();
});

function getWords() {
	$.getJSON( "/getSelctionWords/1", function( data ) {
  		list_of_words = data;
  		if (data.length==0) {
  			goToErrorPage();
  		}
  		createFAT();
  		setDefaultAction(defaultAction);  		
	});
}

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

function defaultAction() {
    if (!blockKeyPress) {
    	blockKeyPress=true;
        if (first) {
        	first = false;
        	showFirstChain();
        } else {
    		showNextChain();
        }
    }
}

function timerMethod() {
	if (current_word>-1) {
		time_label = getTimer();
		if (time_label.innerHTML=='') {
			time_label.innerHTML = "1";
		} else {
			time = parseInt(time_label.innerHTML,10);
			time = time+1;
			time_label.innerHTML = time.toString();
		}
	}
}


function createFAT() {
	var formElm = document.getElementById('fat_form');
	for (var chain_index=1;chain_index<=FREE_ASS_QUES_NUM;chain_index++) {
		var current_list_of_words = list_of_words[chain_index];
		var wdiv = document.createElement('div');
		wdiv.id = 'chain' + chain_index + '_div';
		wdiv.className = 'words-chain';
var inp = document.createElement('input');
		$('<input>').attr('id','chain' + chain_index + '_w0').attr('type','text').attr('class','word_input').attr('readonly',true).attr('value', words[chain_index-1] ).appendTo($(wdiv));

		createArrow(wdiv,'arrow' + chain_index + '_w0')
		for (var word_index=1; word_index<=FREE_ASS_OPT_NUM; word_index++) {
			createInput('chain' + chain_index + '_w' + word_index, wdiv, 'word_input');
			if (word_index<FREE_ASS_OPT_NUM) {
				createArrow(wdiv,'arrow' + chain_index + '_w' + word_index);
			}
		}
		createArrow(wdiv,'arrow' + chain_index + '_w' + FREE_ASS_OPT_NUM);
		
		var selection = $('<select>').attr('id','sel' + chain_index).attr('class','selectpicker').append($('<option value="" disabled selected>Select your option</option>'));
		var tmp_word;
		for (word_index = 0; word_index < current_list_of_words.length; ++word_index) {
		    selection.append( $('<option>').text( current_list_of_words[word_index] ) )
		}
		$(wdiv).append(selection);

		wdiv.appendChild(document.createElement('br'))
		for (var word_index=0 ; word_index<=FREE_ASS_OPT_NUM+1; word_index++) {
			createTimeLabel(chain_index,word_index, wdiv)
		}
		formElm.appendChild(wdiv);
		$('#chain' + chain_index + '_div').hide();
		document.getElementById('time' + current_chain + '_w1').innerHTML = "1";
	}
}

function showFirstChain() {
	// replace the click action
	first=false;
	$("#next").off("click");
	$('#next').click(showNextChain);
	$('#next')[0].value="Next";
	$('#chain1_div').fadeIn('slow', function() { 
		blockKeyPress=false;
		timerId = setInterval(timerMethod, 1000); 
	});	
//	setFocusOnCurrentWord();
}

function showNextChain() {
	if (legalWords()) {
		setWarningLabel("");
		if (current_chain==FREE_ASS_QUES_NUM) {
			saveToJSON();
			$('#fat_main').fadeOut("slow", function () {
				$('#submit').click();	
			});
		} else {
			$('#chain' + current_chain + '_div').fadeOut("slow", function() {
				current_word = 1;
			    current_chain = current_chain+1;
				$('#chain' + current_chain + '_div').fadeIn(function() { 
					setFocusOnCurrentWord();
					blockKeyPress=false;
				});
			});
		}
	} else { 
		blockKeyPress=false;
	}
}

function emptyWords() {
	for (var word_index=1 ; word_index<=FREE_ASS_OPT_NUM; word_index++) {
		var word = getWord(word_index);
		if (word=="") { return true; }
	}
	return false;
}

function legalWords() {
	isLegal = true;
	for (var word_index=1 ; word_index<=FREE_ASS_OPT_NUM && isLegal; word_index++) {
		current_word = word_index;
		var word = getWord(word_index)
		if (word=="") {
			setWarningLabel("The word cannot be empty");
			setFocusOnWord(word_index);
			isLegal=false;			
		} else if (wordAlreadyAppear(word)) {
			setWarningLabel("You cannot use the same word twice");
			setFocusOnWord(word_index);
			isLegal=false;
		} else if (!wordIsValidEnglish(word)) {
			setWarningLabel(word + " isn't a valid English word");
			setFocusOnWord(word_index);
			isLegal=false;
		}
	}
	return isLegal;
}


function legalWord(word) {
	return (!(word=="" || wordAlreadyAppear(word) || !wordIsValidEnglish(word))) 
}

function createArrow(div,id) {
	createImage(div, id, 'pics/arrow.png', 'arrow_img')
}

function createInput(id,div,className) {
	var inp = document.createElement('input');
	inp.id = id;
	inp.type = 'text';
	inp.className = className;
	inp.onblur = wordLostFocus;
	inp.onfocus = wordOnFucus;
	div.appendChild(inp);
}

function wordLostFocus() {
	if (divNotShown()) { return true; }
	var currentWord = getCurrentWord();
	if (currentWord=="") {
		setWarningLabel("The word cannot be empty")		
		setFocusOnCurrentWord();
	} else {
		if (legalWord(currentWord)) {
			setWarningLabel("");
		}
	}
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
	for (word_index=current_word-1; word_index>=0; word_index--) {
		var prevWord = getWord(word_index);
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

function setFocusOnWord(word_index) {
	current_word = word_index;
	document.getElementById('chain' + current_chain + '_w' + word_index).focus();
}

function getCurrentWord() {
	return $.trim(document.getElementById('chain' + current_chain + '_w' + current_word).value).toLowerCase();
}

function getWord(word_index) {
	return $.trim(document.getElementById('chain' + current_chain + '_w' + word_index).value).toLowerCase();
}

function setWarningLabel(text) {
	lbl = document.getElementById('warning_lbl');
	lbl.innerHTML = text;
}

function getTimer() {
	return document.getElementById('time' + current_chain + '_w' + current_word);
}

function saveToJSON() {
    jsonObj = [];
    $("div[class=words-chain]").each(function() {
    	var chain = {};
    	chain["words"] = [];
    	chain["times"] = [];
    	$(this).find("input[class=word_input]").each(function() { 
	        chain["words"].push($(this).val());
    	});
    	$(this).find("label[class=word_input]").each(function() { 
	        chain["times"].push($(this)[0].innerHTML);
    	});
    	jsonObj.push(chain);
    });
    jsonString = JSON.stringify(jsonObj);
    document.getElementById('data').value = jsonString;
    console.log(jsonString);
}
