/*--------------------------------------------------------------------
 * inventory.js Handles API calls
 *--------------------------------------------------------------------*/
myAudio = new Audio('/static/sounds/bg_music.mp3');
if (typeof myAudio.loop == 'boolean') {
	myAudio.loop = true;
}
else {
	myAudio.addEventListener('ended', function() {
		this.currentTime = 0;
		this.play();
	}, false);
}
myAudio.play();

window.addEventListener("load", function() {
	var delBTN = document.getElementById("delete");
	delBTN.addEventListener("click", function(event){
		event.preventDefault();
		delData();
	});

	function delData() {
		var ID = document.getElementById("ID");

		var delXHR = new XMLHttpRequest();

		delXHR.addEventListener("error", function(event){
			alert('An error has occured');
		});

		delXHR.addEventListener("load", function(event) {
			alert('Vehicle Deleted');
		});

		delXHR.open("DELETE", "http://softwarebois.com/inventory/" + ID.value, true);

		delXHR.send();
	}

	var postForm = document.getElementById("postForm");
	var elements = postForm.elements;

	function sendData() {
		var postXHR = new XMLHttpRequest();

		var pd = new FormData(postForm),
			PD = {};

		for (var entry of pd.entries()) {
			PD[entry[0]] = entry[1];
		}
		console.log(PD);
		PD = JSON.stringify(PD);
		console.log(PD);

		// Define what happens in case of an error
		postXHR.addEventListener('error', function(event) {
			alert('An error has occured');
		});

		postXHR.addEventListener('load', function(event) {
			alert('Vehicle created.');
		});

		// Set up POST request
		postXHR.open("POST", "http://softwarebois.com/inventory", true);		

		postXHR.setRequestHeader('Content-type', 'application/json');

		// Data sent is what the user provided in the form
		postXHR.send(PD);
	}

	postForm.addEventListener("submit", function(event) {
		event.preventDefault();
		sendData();
	});
});