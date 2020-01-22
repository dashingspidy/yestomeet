// Google Place API for user location 
    var userLoc = document.getElementById('location');
    var options = {
        types: ['(cities)']
    };
    autocomplete = new google.maps.places.Autocomplete(userLoc, options);

