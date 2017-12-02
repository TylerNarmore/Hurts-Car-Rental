/*--------------------------------------------------------------------
 * main.js Handles API calls
 *--------------------------------------------------------------------*/
 // HEY ASSHOLE ALERT THEM WHEN THEY RENT A CAR
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

function googleMapAPI(cityState) {
	var mapXHR = new XMLHttpRequest();

	// Define what happens in case of error
	mapXHR.addEventListener("error", function(event) {
		alert('An error has occured.');
	});

	var mapXHR = new XMLHttpRequest();

	var data;

	mapXHR.open("GET", "https://maps.googleapis.com/maps/api/geocode/json?address="+ cityState + "&key=AIzaSyBjSWNyYv2Zm5r6BUjQgDZIxq7bEnoit1A", true);
	mapXHR.send();
	// Define what happens when data is returned from GET request
	mapXHR.addEventListener("readystatechange", processMapRequest, false);


function processMapRequest(event) {
	if (mapXHR.readyState == 4 && mapXHR.status == 200) {
		// Parse and store returned object
		var response = JSON.parse(mapXHR.responseText);
		data = response.results[0].geometry.location;	// For readability

		console.log(data);
		initMap(data)

		}
	} 
}

function initMap(data) {
	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 8,
		center: data,
		styles: [
            {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
            {
              featureType: 'administrative.locality',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'poi',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'geometry',
              stylers: [{color: '#263c3f'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'labels.text.fill',
              stylers: [{color: '#6b9a76'}]
            },
            {
              featureType: 'road',
              elementType: 'geometry',
              stylers: [{color: '#38414e'}]
            },
            {
              featureType: 'road',
              elementType: 'geometry.stroke',
              stylers: [{color: '#212a37'}]
            },
            {
              featureType: 'road',
              elementType: 'labels.text.fill',
              stylers: [{color: '#9ca5b3'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry',
              stylers: [{color: '#746855'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry.stroke',
              stylers: [{color: '#1f2835'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'labels.text.fill',
              stylers: [{color: '#f3d19c'}]
            },
            {
              featureType: 'transit',
              elementType: 'geometry',
              stylers: [{color: '#2f3948'}]
            },
            {
              featureType: 'transit.station',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'water',
              elementType: 'geometry',
              stylers: [{color: '#17263c'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.fill',
              stylers: [{color: '#515c6d'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.stroke',
              stylers: [{color: '#17263c'}]
            }
          ]
	});
	var marker = new google.maps.Marker ({
		position: data,
		map: map
	});
}

window.addEventListener("load", function() {
	var getForm = document.getElementById("getForm");
	var elements = getForm.elements;

	function sendData() {
		// If an input was left blank disable it from form
		for (var i = 0; element = elements[i++];) {
			if (element.value === "")
				element.disabled = true;

			else if (element.id == "location" && element.value != null) {
				if (element.value === "Home") {
					window.location.href = "http://softwarebois.com";
				}
				else if (element.value === "Moron Mountain") {
					window.location.href = "http://spacejam.com";
				}
				else if (element.value === "Game Over") {
					gameOver = new Audio('/static/sounds/gameOver.mp3');
					gameOver.play();
				}
				else if (element.value === "Ice Cold") {
					iceCold = new Audio('/static/sounds/ice.mp3');
					iceCold.play();
				}
				else if (element.value === "Lisa") {
					lisa = new Audio('/static/sounds/lisa.mp3');
					lisa.play();
				}
				else {
					var mapDiv = document.getElementById('map');
					mapDiv.style.display = "block";
					var cityState = element.value;
					googleMapAPI(cityState);
				}
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
					//tempContainer.children().atrr('disabled', 'disabled');
					$('.make', tempContainer).text("Make: " + data[each].make);
					$('.model', tempContainer).text("Model: " + data[each].model);
					$('.year', tempContainer).text("Year: " + data[each].year);
					$('.type', tempContainer).text("Type: " + data[each].type);
					$('.passengers', tempContainer).text("Passengers: " + data[each].passengers);
					$('.cost', tempContainer).text("Cost: " + data[each].cost);
					$('.mpg', tempContainer).text("MPG: " + data[each].mpg);
					$('.location', tempContainer).text("Location: " + data[each].location);

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

						sendXHR.addEventListener('load', function(event) {
							alert('Vehicle rented!')
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