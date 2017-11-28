/*--------------------------------------------------------------------
 * main.js Handles API calls
 *--------------------------------------------------------------------*/
window.addEventListener("load", function() {
	function sendData() {
		var XHR = new XMLHttpRequest();

		// Bind the FormData object and the form element
		var FD = new FormData(form);

		// Define what happens on successful data submission
		XHR.addEventListener("load", function(event) {
			alert(event.target.responseText);
		});

		XHR.addEventListener("error", function(event) {
			alert('An error has occured.');
		});

		XHR.open("GET", "http://softwarebois.com/inventory", true);

		// The data sent is what the user provided in the form
		XHR.send(FD);
	}

	var form = document.getElementById("myForm");

	form.addEventListener("submit", function(event) {
		event.preventDefault();

		sendData();
	});
});