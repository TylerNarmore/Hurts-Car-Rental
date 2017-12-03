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
	getXHR = new XMLHttpRequest();

	getXHR.addEventListener("error", function(event) {
		alert('An error has occured.');
	});

	getXHR.addEventListener("readystatechange", processRequest, false);

	function processRequest() {
		if (getXHR.readyState == 4 && getXHR.status == 200) {
			var revenue = document.getElementById('revenue');
			var response = JSON.parse(getXHR.responseText);
			console.log(response.revenue);
			revenue.innerHTML = "Total Revenue: $" + response.revenue;
		}
	}

	getXHR.open("GET", "http://softwarebois.com/money", true);

	getXHR.send(null);


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

		var vehicleID = document.getElementById('vehicleID').value,
			make = document.getElementById('make').value,
			model = document.getElementById('model').value,
			year = document.getElementById('year').value,
			location = document.getElementById('location').value,
			cost = document.getElementById('cost').value,
			passengers = document.getElementById('passengers').value,
			autoTransmission = document.getElementById('autoTransmission').value,
			type = document.getElementById('type').value,
			mpg = document.getElementById('mpg').value,
			gps = document.getElementById('gps').value,
			maxChildSeat = document.getElementById('maxChildSeat').value,
			skiRack = document.getElementById('skiRack').value,
			snowChains = document.getElementById('snowChains').value,
			leftControl = document.getElementById('leftControl').value;

		var string = '{ "vehicles": [ { "vehicleID":' + vehicleID + ', "make": ' + '"' + make + '"' + ', "model": ' + '"' + model + '"' + ', "year": ' + year + ', "location": ' + '"' + location + '"' + ', "cost": ' + cost + ', "passengers": ' + passengers + ', "autoTransmission": ' + autoTransmission + ', "type": ' + '"' + type + '"' + ', "mpg": ' + mpg + ', "specialEquipment": { "gps": ' + gps + ', "maxChildSeat": ' + maxChildSeat + ', "skiRack": ' + skiRack + ', "snowChains": ' + snowChains + ', "leftControl": ' + leftControl + '} } ] }';

		// Define what happens in case of an error
		postXHR.addEventListener('error', function(event) {
			alert('An error has occured');
		});

		postXHR.addEventListener('load', function(event) {
			alert('Vehicle created.');
		});

		var proxy = 'https://cors-anywhere.herokuapp.com';

		// Set up POST request
		postXHR.open("POST", "http://softwarebois.com/inventory", true);		

		postXHR.setRequestHeader('Content-type', 'application/json');

		// Data sent is what the user provided in the form
		postXHR.send(string);
	}

	postForm.addEventListener("submit", function(event) {
		event.preventDefault();
		sendData();
	});
});