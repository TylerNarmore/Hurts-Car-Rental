/*--------------------------------------------------------------------
 * main.js Handles API calls
 *--------------------------------------------------------------------*/
window.addEventListener("load", function() {
	var form = document.getElementById("getForm");
	var elements = form.elements;

	function sendData() {
		// If an input was left blank disable it from form
		for (var i = 0; element = elements[i++];) {
			if (element.value === "")
				element.disabled = true;
		}
 
		var xhr = new XMLHttpRequest();

		// Bind the FormData object and the form element
		var fd = new FormData(form);

		// Define what happens in case of error
		xhr.addEventListener("error", function(event) {
			alert('An error has occured. Abandon ship! Abandon ship! Mayday!');
		});

		// Define what happens when data is returned from GET request
		xhr.addEventListener("readystatechange", processRequest, false);

		function processRequest(event) {
			if (xhr.readyState == 4 && xhr.status == 200) {
				// Parse and store returned object
				var response = JSON.parse(xhr.responseText);
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
					postForm.id = "postForm";
					tempContainer.append(postForm);

					var field = document.createElement("fieldset");
					postForm.append(field);

					var legend = document.createElement("legend");
					legend.innerHTML = "Input Start/End Date For Rental";
					field.append(legend);

					// Create inputs for form
					var startDate = document.createElement("input");
					startDate.setAttribute('type', 'datetime-local');
					startDate.setAttribute('step', '1');
					field.append(startDate);

					var endDate = document.createElement("input");
					endDate.setAttribute('type', 'datetime-local');
					endDate.setAttribute('step', '1');
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
						// Send the POST request with the vehicleID and dates
					});
				}

				console.log(response.vehicles);

			}
		}

		// Set up GET request
		xhr.open("GET", "http://softwarebois.com/inventory", true);

		// The data sent is what the user provided in the form
		xhr.send(fd);
	}
	
	form.addEventListener("submit", function(event) {
		event.preventDefault();
		sendData();

		// Reenable all elements on the form
		for (var i = 0; element = elements[i++];) {
			element.disabled = false;
		}
	});
});