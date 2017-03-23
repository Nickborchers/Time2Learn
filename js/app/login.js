/**
 * login.js
 *
 * This module takes care of the gui for the login, the code & connection checking happens
 * in session.js, which returns the status to login with the callback function 'checkLogin'
 * implemented in main.js module.
 *
 * If there is already a account code saved in the storage, then there will be no login interface
 * drawn. An account code will only be saved if it was correct code. So the user only has to login in
 * once.
 *
 * made by Rick Nienhuis & Niels Haan
 * 
 * NEW FEATURES:
 * 
 * Anonymous account checking and session fetching for anonymous account using Zeeguu API.
 * A nice gui is added where the user can press a flag to select the desired language.
 * 
 * made by Yaroslav Tykhonchuk, Nick Borchers and Robin Sommer
 */

define(['userData', 'popup'], function(userData, popup) {
    var ctx;
    var loginCode = 0;

    //Definition of login endpoints:
	const RELOGIN_ENDPOINT = "https://zeeguu.unibe.ch/api/get_anon_session/";
	const GET_ANONYMOUS_ACCOUNT_ENDPOINT = "https://zeeguu.unibe.ch/api/add_anon_user";
	
	// Definition of country code constants
	const NETHERLANDS = "nl";
	const GERMANY = "de";
	const SPAIN = "es";
	const FRANCE = "fr";
	
	// Definition of connection messages:
	const WRONG_SESSION_NUMBER = "WRONG_SESSION_NUMBER";
	const NO_CONNECTION = "NO_CONNECTION";
	
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
    
    var NUMBER_OF_CODE_NUMBERS_ON_PAGE = 4;

    /*
     * goToMainPage() sets the right html "<div>" to display. The drawing of other elements is done by other functions.
     */
    
    function goToMainPage() {
        document.getElementById("languageFlags").style.display="none";
        document.getElementById("mainPage").style.display = "block";
    }
    
    /* 
     * selectLanguages() handles flag presses from the selectLanguage menu. The corresponding country is passed on to
     * the requestAnonAccount() function. 
     */
    
    function selectLanguages(){
    	document.getElementById("frenchFlag").addEventListener("click", function() {
    		requestAnonAccount(FRANCE);
    		if( localStorage.getItem("accountCode") !== null ){
    			goToMainPage();
    		}else{
    			selectLanguages();
    		}
 	    });
    	 document.getElementById("germanFlag").addEventListener("click", function() {
     		requestAnonAccount(GERMANY);
    		if( localStorage.getItem("accountCode") !== null ){
    			goToMainPage();
    		}else{
    			selectLanguages();
    		}
  	    });
    	 document.getElementById("spanishFlag").addEventListener("click", function() {
      		requestAnonAccount(SPAIN);
    		if( localStorage.getItem("accountCode") !== null ){
    			goToMainPage();
    		}else{
    			selectLanguages();
    		}
  	    });
    	 document.getElementById("dutchFlag").addEventListener("click", function() {
      		requestAnonAccount(NETHERLANDS);
    		if( localStorage.getItem("accountCode") !== null ){
    			goToMainPage();
    		}else{
    			selectLanguages();
    		}
  	    });
    }

    /*
     * guid() generates a (nearly) random UUID. It is not hardware based, we need system calls for this which turned out to be quite tricky.
     * Therefore it just generates a very large random string. In the rare occasion that two (globally, known to the server)
     * identical strings are generated, we simply try again.
     */
    function guid() {
    	  function s4() {
    	    return Math.floor((1 + Math.random()) * 0x10000)
    	      .toString(16)
    	      .substring(1);
    	  }
    	  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    	    s4() + '-' + s4() + s4() + s4();
    	}
    /*
     * randPass() generates a number between 1 and 1 million. Which is used as a password for the random account.
     */
    
	function randPass() {
		return (Math.floor((1 + Math.random() * 1000000))).toString();
	}
    	
	/*
	 * requestAnonAccount() gets a string containing the desired language to be learned. This function generates a random UUID ans password combination 
	 * which is then being stored inside localStorage for subsequent logins. The server returns a session which can be used for further requests for the server.
	 * 
	 */
	function requestAnonAccount(learning_language) {
		var uuid = guid();
		var password = randPass();
	    var form = new FormData();
		form.append('uuid', uuid);
		form.append('password', password);
	    try { 
			var xhr = new XMLHttpRequest();
			xhr.open('POST', GET_ANONYMOUS_ACCOUNT_ENDPOINT, true);
			xhr.onload = function () {
				try {
					localStorage.setItem("accountCode", JSON.parse(this.responseText));
					localStorage.setItem("uuid", uuid);
					localStorage.setItem("password", password);
				} catch(err) {
				// UUID and Password combination are invalid.
				console.log(WRONG_SESSION_NUMBER);
				}
			};
			xhr.send(form);
		} catch(err) {
			// there is no internet connection
			console.log(NO_CONNECTION);
		}	
	}
    
	/*
	 * relogin is being called when uuid and password are present in localstorage. We are 100% sure that 
	 * this combination should then ring a bell with the server; they are only stored when the server has accepted them before.
	 * In the unusual event that this is not the case, the selectLanguage page is loaded and a new anonynous account can then be 
	 * created for the user.
	 */
	function relogin(uuid, password) {
		var form = new FormData();
		form.append('password', password);
	    try { 
			var xhr = new XMLHttpRequest();
			xhr.open('POST', RELOGIN_ENDPOINT + uuid, true);
			xhr.onload = function () {
				try {
					localStorage.setItem("accountCode", JSON.parse(this.responseText));
				} catch(err) {
				// UUID and Password combination are invalid.
				console.log(WRONG_SESSION_NUMBER);
				}
			};
			xhr.send(form);
		} catch(err) {
			// there is no internet connection
			console.log(NO_CONNECTION);
		}	
	}
    	
    /*
     * login handles everything that corresponds with the login functionality: the core logic is implemented here.
     * As you can see, there are two lines which can be uncommented to demonstrate both cases: when an account is present
     * and when this is not the case.
     */
    return function login(checkLogin) {
    	localStorage.removeItem("password");
    	localStorage.removeItem("uuid");
    	//Uncomment the following two lines to skip the language selection: 
//        	localStorage.setItem("uuid", "d615d7ff-9895-aab8-cb45-a14da23f7ca3");
//        	localStorage.setItem("password", "17196");
    	if( (localStorage.getItem("uuid") !== null) && (localStorage.getItem("password") !== null) ){
    		relogin(localStorage.getItem("uuid"), localStorage.getItem("password"))
    		if( localStorage.getItem("accountCode") !== null ){
    			goToMainPage();
    		}else{
    			selectLanguages();
    		}
    	}else{
    		selectLanguages();
    	}
    }
});
