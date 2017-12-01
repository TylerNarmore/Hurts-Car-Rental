/*--------------------------------------------------------------------
 * main.js Handles API calls
 *--------------------------------------------------------------------*/
myAudio = new Audio('assets/sounds/bg_music.mp3');
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
	var getForm = document.getElementById("getForm");
	var elements = getForm.elements;

	function initMap() {
		var map = new google.maps.Map(document.getElementById('map'), {
			zoom: 4,
			center: data
		});
		var marker = new google.maps.Marker ({
			position: data,
			map: map
		});
	}

	function sendData() {
		// If an input was left blank disable it from form
		for (var i = 0; element = elements[i++];) {
			if (element.value === "")
				element.disabled = true;

			else if (element.id == "location") {
				if (element.value = "Home") {
					window.location.href = "http://softwarebois.com";
				}
			}

			// Correctly format date values for search -- FIX THIS sober Josh
			else if (element.id == 'start' || element.id == 'end') {
				element.value = element.value + "T12:00:00";
				console.log(element.value);
			}
		}

		var getXHR = new XMLHttpRequest();

		// Define what happens in case of error
		getXHR.addEventListener("error", function(event) {
			alert('An error has occured.');
		});

		// Define what happens when data is returned from GET request
		getXHR.addEventListener("readystatechange", processRequest, false);

		function processRequest(event) {
			if (getXHR.readyState == 4 && getXHR.status == 200) {
				// Parse and store returned object
				var response = JSON.parse(getXHR.responseText);
				var data = response.vehicles;	// For readability

				// Grab wrapper for displaying data and clone
				var wrapper = $('#wrapper'),
					container = $('.container', wrapper).clone();
				wrapper.empty();

				// Loop for displaying data in separate divs
				for (var each in data) {
					var tempContainer = container.clone();
					$('.make', tempContainer).text("Make: " + data[each].make);
					$('.model', tempContainer).text("Model: " + data[each].model);
					$('.year', tempContainer).text("Year: " + data[each].year);
					$('.type', tempContainer).text("Type: " + data[each].type);
					$('.location', tempContainer).text("Location: " + data[each].location);
					$('.cost', tempContainer).text("Cost: " + data[each].cost);
					$('.mpg', tempContainer).text("MPG: " + data[each].mpg);
					$('.passengers', tempContainer).text("Passengers: " + data[each].passengers);

					// Create form data for selecting start/end dates for rental
					var postForm = document.createElement("form");
					postForm.id = "postForm" + each;
					tempContainer.append(postForm);

					var field = document.createElement("fieldset");
					field.className = "outputField";
					postForm.append(field);

					var legend = document.createElement("legend");
					legend.innerHTML = "Input Start/End Date For Rental";
					field.append(legend);

					// Create inputs for form
					var startDate = document.createElement("input");
					startDate.setAttribute('type', 'datetime-local');
					startDate.setAttribute('step', '1');
					startDate.setAttribute('name', 'startDate')
					field.append(startDate);

					var endDate = document.createElement("input");
					endDate.setAttribute('type', 'datetime-local');
					endDate.setAttribute('step', '1');
					endDate.setAttribute('name', 'endDate');
					field.append(endDate);

					// Attach rent buttons to each div
					var button = document.createElement("button");
					button.id = each;
					button.className = "rentMe";
					var text = document.createTextNode("RENT ME");
					button.append(text);

					tempContainer.append(button);
					wrapper.append(tempContainer);
				}

				// Attach event to each buttons to send POST request for selected vehicle
				var buttons = document.getElementsByClassName("rentMe");
				for (var i = 0; i < buttons.length; i++) {
					buttons[i].addEventListener("click", function(event) {
						var sendForm = document.getElementById("postForm" + event.target.id);
						var vehicle = response.vehicles[event.target.id];
						var vehicleID = vehicle.vehicleID;

						var sendXHR = new XMLHttpRequest();

						// Bind the form data object to the form
						var sd = new FormData(sendForm),
							SD = {};
						sd.append("vehicleID", vehicleID);	// Add the vehicle ID to the form

						for (var entry of sd.entries()) {
							SD[entry[0]] = entry[1];
						}
						SD = JSON.stringify(SD)
						console.log(SD);

						// Define what happens when data is returned from GET request
						sendXHR.addEventListener("readystatechange", processResponse, false);

						function processResponse(event) {
							if (sendXHR.readyState == 4 && sendXHR.status == 200) {
								// Parse and store returned object
								var response = JSON.parse(sendXHR.responseText);
								var data = response.vehicles;	// For readability
								console.log(response);
							}
						}

						// Define what happens in case of an error
						sendXHR.addEventListener('error', function(event) {
							alert('An error has occured');
						});

						// Set up POST request
						sendXHR.open("POST", "http://softwarebois.com/purchase/12345", true);

						sendXHR.setRequestHeader('Content-type', 'application/json');

						// Data sent is what the user provided in the form
						sendXHR.send(SD);
					});
				}

				console.log(response.vehicles);

			}
		}

		// Set up GET request
		var protoURL = "http://softwarebois.com/inventory";
		var str = $("#getForm").serialize();
		var url = protoURL + '?' + str;
		console.log(url);
		getXHR.open("GET", url, true);
		getXHR.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		getXHR.send(null);
	}
	
	getForm.addEventListener("submit", function(event) {
		event.preventDefault();
		var wrapper = $("#wrapper");
		//wrapper.empty();
		sendData();
		// Reenable all elements on the form
		for (var i = 0; element = elements[i++];) {
			element.disabled = false;
		}
	});
});