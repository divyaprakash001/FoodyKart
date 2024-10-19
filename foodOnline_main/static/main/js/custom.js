let autocomplete;



function initAutoComplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
      types: ['geocode', 'establishment'],
      //default in this app is "IN" - add your country code
      componentRestrictions: { 'country': 'in' },
    })
  // function to specify what should happen when the prediction is clicked
  autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
  var place = autocomplete.getPlace();

  // User did not select the prediction. Reset the input field or alert()
  if (!place.geometry) {
    document.getElementById('id_address').placeholder = "Start typing...";
  }
  else {
    // console.log('place name=>', place.name)
  }
  // get the address components and assign them to the fields
  let geoCoder = new google.maps.Geocoder()
  var address = document.getElementById('id_address').value

  geoCoder.geocode({ 'address': address }, function (results, status) {
    // console.log(results);
    // console.log(status);
    if (status == google.maps.GeocoderStatus.OK) {
      var latitude = results[0].geometry.location.lat()
      var longitude = results[0].geometry.location.lng()
      // console.log('lat==>', latitude);
      // console.log('longitude==>', longitude);
      $("#id_latitude").val(latitude);
      $("#id_longtitude").val(longitude);

      $("#id_address").val(address);

      // loop through the address components and assign other address data
      for (var i = 0; i < place.address_components.length; i++) {
        for (var j = 0; j < place.address_components[i].types.length; j++) {
          // get country
          if (place.address_components[i].types[j] == 'country') {
            $("#id_country").val(place.address_components[i].long_name);
          }

          if (place.address_components[i].types[j] == 'administrative_area_level_1') {
            $("#id_state").val(place.address_components[i].long_name);
          }

          if (place.address_components[i].types[j] == 'locality') {
            $("#id_city").val(place.address_components[i].long_name);
          }

          if (place.address_components[i].types[j] == 'postal_code') {
            $("#id_pin_code").val(place.address_components[i].long_name);
          } else {
            $("#id_pin_code").val("");
          }
        }
      }

    }
  })

}


// add to cart functionality
$(document).ready(function () {
  $(".add_to_cart").on("click", function (e) {
    e.preventDefault();
    food_id = $(this).attr("data-id")
    url = $(this).attr("data-url")

    data = {
      food_id: food_id,
    }
    $.ajax({
      type: "GET",
      url: url,
      data: data,
      success: function (response) {
        if (response.status == 'login_required') {
          swal(response.message, '', 'info').then(function () {
            window.location = "/login";
          })
        }
        else if (response.status == 'Failed') {
          swal(response.message, '', 'error')
        } else {
          $("#cart_counter").html(response.cart_counter['cart_count'])
          $("#qty-" + food_id).html(response.qty)
        }


      }
    });

  })

  // place the cart item quantity on load
  $(".item_qty").each(function () {
    var the_id = $(this).attr("id")
    var qty = $(this).attr("data-qty")
    $("#" + the_id).html(qty)
  });

  // decrease

  // decrease cart
  $(".decrease_cart").on("click", function (e) {
    e.preventDefault();
    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");

    console.log(food_id);
    console.log(url);

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status == 'login_required') {
          swal(response.message, '', 'info').then(function () {
            window.location = '/login'
          })
        }
        else if (response.status == 'Removed') {
          swal(response.message, '', 'success')
        }
        else if (response.status == 'Failed') {
          swal(response.message, '', 'error')
        } else {
          $("#cart_counter").html(response.cart_counter['cart_count'])
          $("#qty-" + food_id).html(response.qty)
        }
      }
    });

  });


});
