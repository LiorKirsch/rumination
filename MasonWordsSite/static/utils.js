var $_GET = {};

function initGET(document) {
	document.location.search.replace(/\??(?:([^=]+)=([^&]*)&?)/g, function () {
		function decode(s) {
		    return decodeURIComponent(s.split("+").join(" "));
		}

		$_GET[decode(arguments[1])] = decode(arguments[2]);
	});	
}

function isChrome() {
	var chrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
	return chrome;
}

function isFF() {
	var FF = !(window.mozInnerScreenX == null);
	return FF;
}

function isIE() {
	var IE = /*@cc_on!@*/false;
	return IE;
}

function isSafari() {
	var isSafari = /Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor);
	return isSafari;
}

function get_elapsed_time_string(total_seconds) {
	var hours = Math.floor(total_seconds / 3600);
	total_seconds = total_seconds % 3600;
	
	var minutes = Math.floor(total_seconds / 60);
	total_seconds = total_seconds % 60;
	
	var seconds = Math.floor(total_seconds);
	
	// Pad the minutes and seconds with leading zeros, if required
	hours = pretty_time_string(hours);
	minutes = pretty_time_string(minutes);
	seconds = pretty_time_string(seconds);
	
	// Compose the string for display
	// var currentTimeString = hours + ":" + minutes + ":" + seconds;
	var currentTimeString = minutes + ":" + seconds;
	
	return currentTimeString;
}

function pretty_time_string(num) {
	return ( num < 10 ? "0" : "" ) + num;
}

function get_time() {
	var t = new Date() ;
	return d.toUTCString() + "/" + d.getUTCMilliseconds();
}

function sendDataToServer(dataToSend, urlToSend) {
	// example: 
	// dataToSend: {'click_times': JSON.stringify(click_times)};
	// urlToSend: '/click_times/'
    $.ajax({
        url: urlToSend,
        type: 'post',
        dataType: 'json',
        success: function (dataRecieved) {
            console.log( dataRecieved );
        },
        data: dataToSend
    });
}

function getDictValue(dict, key, defaultVal) {
	if (key in dict) {
		return dict[key];
	} else {
		return defaultVal;
	}
}

function setDefaultAction(defaultFunction) {
	// Set showNextChain as the default action in the form (when the user has clicked enter)
	$("body").keypress(function (event) {
	    if (event.which == 13) {
	        event.preventDefault();
	        defaultFunction();
        }
	});			
}

function goToErrorPage() {
	window.location.href = '/error/';
}

function createMultipleChoicesQuestion(questionNum, question, options) {
	parser = new DOMParser()
	ql = new Array();
	for (q=0; q<4; q++) { ql.push(sprintf('Q%dRB%d',questionNum,q+1)); }
	if (options.length == 0) { options = ["Almost never","Sometimes","Often","Almost always"]; }
	var mainDiv = document.createElement('div');
	mainDiv.className = 'control-group';
	mainDiv.id = sprintf('q%d_div',questionNum);
	mainDiv.appendChild(createQuestionTitle(question));
	var div = document.createElement('div');
	for (ans=0; ans<4; ans++) {
		createQuestionInput(div,sprintf('Q%dRB%d',questionNum,ans+1),sprintf('Q%dRB',questionNum),options[ans]);
	}
	mainDiv.appendChild(div);
	return mainDiv; 
}

function createH2(div, id, question) {
	var h2 = document.createElement('h2');
	h2.id = id;
	h2.innerHTML = question;
	div.appendChild(h2);	
	return h2;
}


function createQuestionInput(div,qID,qName,option) {
	var lbl = document.createElement('label');
	lbl.htmlFor = qID;
	lbl.className = "radio";
	var inp = document.createElement('input');
	inp.id = qID;
	inp.type = "radio";
	inp.name = qName;
	inp.value = option;
	lbl.appendChild(inp);
	lbl.innerHTML += option;
	div.appendChild(lbl)
}

function createDiv(id,className) {
	var div = document.createElement('div');
	div.className = className;
	div.id = id;
	return div
}

function createSliderQuestion(div, questionNum, fromNum, toNumm, sliderClass, defaultValue, textBefore, textAfter) {
	var h3 = document.createElement('h3');
	var sliderDiv = document.createElement('div');
	sliderDiv.className = 'layout-slider';
	sliderDiv.style["width"] = "100%";
	if (textBefore.length!=0) {
		createTextElm(sliderDiv,textBefore)
		createImage(sliderDiv, '', 'pics/empty.png', '')	
	}
	
	sliderName = sprintf('slider%d',questionNum)
	var span =  document.createElement('span');
	span.style["display"] = "inline-block";
	span.style["width"] = "400px";
	span.style["padding"] = "0 5px";

	var inp = document.createElement('input');
	inp.id = sliderName;
	inp.type = "slider";
	inp.name = sprintf('q%d',questionNum);
	inp.setAttribute('value',defaultValue)
	
	span.appendChild(inp);
	sliderDiv.appendChild(span)
	if (textAfter.length!=0) {
		createImage(sliderDiv, '', 'pics/empty.png', '')	
		createTextElm(sliderDiv,textAfter)
	}
	h3.appendChild(sliderDiv)
	div.appendChild(h3);
}

function createImage(div,id,src,className) {
	var img = document.createElement('img');
	img.src = src;
	img.id = id;
	img.className = className
	div.appendChild(img);	
}

function createTextElm(div,text) {
	var content = document.createTextNode(text);
	div.appendChild(content);		
	return content;
}

function createSpan(div,id,text) {
	var span = document.createElement('span');
	span.innerHTML = text;
	span.id = id;
	div.appendChild(span);
	return span;
}

function createBR(div) {
	var br = document.createElement('br');
	div.appendChild(br);
}

function createDropDown(div,id, values, defaultValue) {
	defaultValue = typeof defaultValue !== 'undefined' ? defaultValue : 'Please select';
	var select = document.createElement('select');
	select.id = id;
	select.className = "form-control";
	createOption(select,defaultValue)
	for (i=0; i<values.length; i++) { 
		createOption(select,values[i])
	}
	div.appendChild(select);
}

function createOption(select,value) {
	var option = document.createElement('option');
	option.setAttribute('value',value);
	option.innerHTML = value;
	select.appendChild(option);	
}

var bindEvent = function(el, event, handler) {
	  if (el.addEventListener){
	    el.addEventListener(event, handler, false); 
	  } else if (el.attachEvent){
	    el.attachEvent('on'+event, handler);
	  }
}

//bindEvent(removeButton, "click", function(){
//    removeEmployee(phone, pin, employees[i]['id']);
//});

String.prototype.capitalize = function(lower) {
    return (lower ? this.toLowerCase() : this).replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); });
};