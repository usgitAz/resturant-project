const myAPIKey = "3e282e3ccac9457f840beaad8053da7c";

const streetInput = new autocomplete.GeocoderAutocomplete(
  document.getElementById("id_address"),
  myAPIKey, {
    allowNonVerifiedHouseNumber: true,
    allowNonVerifiedStreet: true,
    skipDetails: true,
    skipIcons: true,
    placeholder: "Enter Your Address here"
  });


streetInput.on('select', (street) => {
    if (street) {
      // streetInput.setValue(street.properties.street || '');
      document.getElementById("address").value = (street.properties.address_line1)
  
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