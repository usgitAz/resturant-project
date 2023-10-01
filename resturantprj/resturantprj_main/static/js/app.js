// The API Key provided is restricted to JSFiddle website
// Get your own API Key on https://myprojects.geoapify.com
const myAPIKey = "3e282e3ccac9457f840beaad8053da7c";

const streetInput = new autocomplete.GeocoderAutocomplete(
  document.getElementById("address"),
  myAPIKey, {
    allowNonVerifiedHouseNumber: true,
    allowNonVerifiedStreet: true,
    skipDetails: true,
    skipIcons: true,
    placeholder: "Enter Your Address here"
  });

// const stateInput = new autocomplete.GeocoderAutocomplete(
//   document.getElementById("state"),
//   myAPIKey, {
//     type: "state",
//     skipDetails: true,
//     placeholder: " ",
//     skipIcons: true,
//     lang : 'fa'
//   });

// const cityInput = new autocomplete.GeocoderAutocomplete(
//   document.getElementById("city"),
//   myAPIKey, {
//     type: "city",
//     skipDetails: true,
//     skipIcons: true,
//     placeholder: " "
//   });


// const countryInput = new autocomplete.GeocoderAutocomplete(
//   document.getElementById("country"),
//   myAPIKey, {
//     type: "country",
//     skipDetails: true,
//     placeholder: " ",
//     skipIcons: true
//   });

// const postcodeElement = document.getElementById("postcode");
// const housenumberElement = document.getElementById("housenumber");

streetInput.on('select', (street) => {
  if (street) {
    // streetInput.setValue(street.properties.street || '');
    document.getElementById("id_address").value = (street.properties.address_line1)

  }
  if (street && street.properties.city) {
    // cityInput.setValue(street.properties.city);
    document.getElementById("id_city").value = (street.properties.city)
  }

  if (street && street.properties.state) {
    // stateInput.setValue(street.properties.state);
    document.getElementById("id_state").value = (street.properties.state)

  }

  if (street && street.properties.country) {
    // countryInput.setValue(street.properties.country);
    document.getElementById("id_country").value = (street.properties.country)

  }
  if (street) {
    // streetInput.setValue(street.properties.street || '');
    document.getElementById("id_latitude").value = (street.properties.lat)

  }
  if (street) {
    // streetInput.setValue(street.properties.street || '');
    document.getElementById("id_longitude").value = (street.properties.lon)

  }
});

// cityInput.on('select', (city) => {

//   if (city) {
//     cityInput.setValue(city.properties.city || '');
//   }
//   if (city && city.properties.state) {
//     stateInput.setValue(city.properties.state);
//   }

//   if (city && city.properties.country) {
//     countryInput.setValue(city.properties.country);
//   }
// });

// stateInput.on('select', (state) => {

//   if (state) {
//     stateInput.setValue(state.properties.state || '');
//   }

//   if (state && state.properties.country) {
//     countryInput.setValue(state.properties.country);
//   }
// });

function checkAddress() {
  const postcode = document.getElementById("postcode").value;;
  const city = cityInput.getValue();
  const street = streetInput.getValue();
  const state = stateInput.getValue();
  const country = countryInput.getValue();
  const housenumber = document.getElementById("housenumber").value;

  const message = document.getElementById("message");
  message.textContent = "";

  if (!city || !street || !housenumber || !state || !country) {
    highlightEmpty();
    message.textContent = "Please fill in the required fields and check your address again.";
    return;
  }

  // Check the address with Geoapify Geocoding API
  // You may use it for internal information only. Please note that house numbers might be missing for new buildings and non-mapped buildings. So consider that most addresses with verified streets and cities are correct.
  fetch(`https://api.geoapify.com/v1/geocode/search?housenumber=${encodeURIComponent(housenumber)}&street=${encodeURIComponent(street)}&postcode=${encodeURIComponent(postcode)}&city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}&country=${encodeURIComponent(country)}&apiKey=${myAPIKey}`).then(result => result.json()).then((result) => {
    let features = result.features || [];

    // To find a confidence level that works for you, try experimenting with different levels
    const confidenceLevelToAccept = 0.25;
    features = features.filter(feature => feature.properties.rank.confidence >= confidenceLevelToAccept);

    if (features.length) {
      const foundAddress = features[0];
      if (foundAddress.properties.rank.confidence === 1) {
        message.textContent = `We verified the address you entered. The formatted address is: ${foundAddress.properties.formatted}`;
      } else if (foundAddress.properties.rank.confidence > 0.5 && foundAddress.properties.rank.confidence_street_level === 1) {
        message.textContent = `We have some doubts about the accuracy of the address: ${foundAddress.properties.formatted}`
      } else if (foundAddress.properties.rank.confidence_street_level === 1) {
        message.textContent = `We can confirm the address up to street level: ${foundAddress.properties.formatted}`
      } else {
        message.textContent = `We can only verify your address partially. The address we found is ${foundAddress.properties.formatted}`
      }
    } else {
      message.textContent = "We cannot find your address. Please check if you provided the correct address."
    }
  });
}


function highlightEmpty() {
  const toHightlight = [];
  if (!cityInput.getValue()) {
    toHightlight.push(cityInput.inputElement);
  }

  if (!streetInput.getValue()) {
    toHightlight.push(streetInput.inputElement);
  }
  if (!stateInput.getValue()) {
    toHightlight.push(stateInput.inputElement);
  }

  if (!countryInput.getValue()) {
    toHightlight.push(countryInput.inputElement);
  }

  toHightlight.forEach(element => element.classList.add("warning-input"));

  setTimeout(() => {
    toHightlight.forEach(element => element.classList.remove("warning-input"));
  }, 3000);
}
