/**
 * codeShow.js
 *
 * This module implements showing the code for connection with the account on the server.
 * if you double tap the screen, the manner of showing the code switches between numbers and a QR Code
 * 
 * made by Robin Sommer
 */

define(['userData'], function(userData) {
	var page = 1;
	var ctx;
	
	//definitions of screen variables
	var SCREEN_WIDTH = 360;
	var SCREEN_HEIGHT = 360;
	
	//definitions of text variables
	var TITLE_HEIGHT = 70;
	var TITLE_TEXT_HEIGHT = 62;
	var ICON_HEIGHT = 15;
	var DIGIT_SPACE = 76;
	var DIGIT_HEIGHT = 105;
	var POS_FIRST_DIGIT = 40;
	var POS_DIGIT_LEFT = 65;
	var POS_DIGIT_TOP = 80;

	// title font
	var TITLE_FONT = "15px Arial";
	var TITLE_FONT_COLOR = "white";

	// code font
	var CODE_FONT = "80px Arial";
	var CODE_FONT_COLOR = "black";

	var NUMBER_OF_CODE_NUMBERS_ON_PAGE = 8;

	function placePageIcon() {
		ctx = document.getElementById("pageIndicationCanvas").getContext("2d");
		ctx.clearRect(0, 0, SCREEN_WIDTH, ICON_HEIGHT);
	
		if (page === 1) {
			ctx.beginPath();
			ctx.arc(170, 7, 7, 0, 2 * Math.PI);
			ctx.fillStyle = "#FFFFFF";
			ctx.fill();
			ctx.beginPath();
			ctx.arc(190, 7, 7, 0, 2 * Math.PI);
			ctx.fillStyle = "#C3C3C3";
			ctx.fill();
		} else {
			ctx.beginPath();
			ctx.arc(170, 7, 7, 0, 2 * Math.PI);
			ctx.fillStyle = "#C3C3C3";
			ctx.fill();
			ctx.beginPath();
			ctx.arc(190, 7, 7, 0, 2 * Math.PI);
			ctx.fillStyle = "#FFFFFF";
			ctx.fill();
		}
	}
	
	function printCodeNumber(position, number){
		ctx = document.getElementById("codeShowDigitsCanvas").getContext("2d");

		if (position < 4) {
			ctx.clearRect(POS_FIRST_DIGIT + DIGIT_SPACE*position, 0, DIGIT_SPACE ,DIGIT_HEIGHT);
			ctx.font = CODE_FONT;
			ctx.fillStyle = CODE_FONT_COLOR;
			ctx.textAlign = "center";
			ctx.fillText(number, POS_DIGIT_LEFT + DIGIT_SPACE*position, POS_DIGIT_TOP);
		} else {
//			Second four digits beneath first four digits
			ctx.clearRect(POS_FIRST_DIGIT + DIGIT_SPACE*(position-4), DIGIT_HEIGHT, DIGIT_SPACE ,DIGIT_HEIGHT);
			ctx.font = CODE_FONT;
			ctx.fillStyle = CODE_FONT_COLOR;
			ctx.textAlign = "center";
			ctx.fillText(number, POS_DIGIT_LEFT + DIGIT_SPACE*(position-4), POS_DIGIT_TOP+DIGIT_HEIGHT);
		}
	}

	function printTitle(title){
		ctx = document.getElementById("codeShowHeaderCanvas").getContext("2d");
		ctx.clearRect(0, 0, SCREEN_WIDTH, TITLE_HEIGHT);
		
		ctx.font = TITLE_FONT;
		ctx.fillStyle = TITLE_FONT_COLOR;
		ctx.textAlign = "center";
		ctx.fillText(title, SCREEN_WIDTH/2, TITLE_TEXT_HEIGHT);
	}

	function showCode() {
		document.getElementById("mainPage").style.display = "none";
		document.getElementById("codeShowPage").style.display = "block";
		printTitle("Your 8 digit code:");
		placePageIcon();
		
		var accountCode = userData.getCode();
		if (page === 1) {
//			show code in numbers here
			var digitToShow;
			for (var i = 0; i < NUMBER_OF_CODE_NUMBERS_ON_PAGE ; i++) {
				digitToShow = Math.floor(accountCode / Math.pow(10,7-i));
				digitToShow = digitToShow - (Math.floor(digitToShow / 10) * 10);
				printCodeNumber(i,digitToShow);				
			}
		} else {
//			create and show QR Code here
			console.log("QR code should be showed, but is not implemented yet");
			for (var j = 0; j < NUMBER_OF_CODE_NUMBERS_ON_PAGE ; j++) {
				printCodeNumber(j,9);				
			}
		}
	}

	return {
		show: function() {
			document.getElementById("backButtonInCodeShow").addEventListener("click", function(){
				document.getElementById("codeShowPage").style.display = "none";
				document.getElementById("mainPage").style.display = "block";
			});
			showCode();
		},
	
		changePage: function() {
			page = (page === 1? 2 : 1);
			showCode();
		}
	};
});