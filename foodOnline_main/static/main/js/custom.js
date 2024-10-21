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
    price = $(this).attr("data-price")

    data = {
      food_id: food_id,
    }
    $.ajax({
      type: "GET",
      url: url,
      data: data,
      success: function (response) {
        console.log(response);

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
          applyCartAmount(response.get_cart_amounts['subtotal'], response.get_cart_amounts['tax'], response.get_cart_amounts['grand_total'])
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


  // decrease cart
  $(".decrease_cart").on("click", function (e) {
    e.preventDefault();
    decrease_btn = $(this);
    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");
    cart_id = $(this).attr("id");
    // alert(cart_id)

    // console.log(food_id);
    // console.log(url);

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        console.log(response)

        if (response.status == 'login_required') {
          swal(response.message, '', 'info').then(function () {
            window.location = '/login'
          })
        }
        else if (response.status == 'Removed') {
          $("#cart_counter").html(response.cart_counter['cart_count'])
          swal(response.message, '', 'success')
          $("#qty-" + food_id).html(response.qty)
          if (window.location.pathname == '/marketplace/cart') {
            document.getElementById("cart-item-" + cart_id).remove();
            checkEmptyCart();
          }
          applyCartAmount(response.get_cart_amounts['subtotal'], response.get_cart_amounts['tax'], response.get_cart_amounts['grand_total'])

        }
        else if (response.status == 'Failed') {
          swal(response.message, '', 'error')
        } else {
          $("#cart_counter").html(response.cart_counter['cart_count'])
          $("#qty-" + food_id).html(response.qty)
          applyCartAmount(response.get_cart_amounts['subtotal'], response.get_cart_amounts['tax'], response.get_cart_amounts['grand_total'])
        }
      }
    });
  });






  // delete cart
  $(".delete_cart").on("click", function (e) {
    e.preventDefault();
    delete_cart_btn = $(this);
    // food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");

    console.log(url);

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        console.log(response)
        if (response.status == 'login_required') {
          swal(response.message, '', 'info').then(function () {
            window.location = '/login'
          })
        }
        else if (response.status == 'Deleted') {
          $("#cart_counter").html(response.cart_counter['cart_count'])
          delete_cart_btn.closest('li').fadeOut(function () {
            $(this).remove();
          });
          applyCartAmount(response.get_cart_amounts['subtotal'], response.get_cart_amounts['tax'], response.get_cart_amounts['grand_total'])
          swal(response.message, '', 'success')
          checkEmptyCart();
        }
        else if (response.status == 'Invalid Request') {
          swal(response.message, '', 'info')
        }
        else if (response.status == 'Not Found') {
          swal(response.message, '', 'info')
        }
        else if (response.status == 'Failed') {
          swal(response.message, '', 'error')
        }
      }
    });

  });

});

function removeCartItem(cartItemQty, cart_id) {

  if (window.location.pathname == '/marketplace/cart') {
    if (cartItemQty <= 0) {
      document.getElementById("cart-item" + cart_id).remove()
    }
  }

}

// check if the cart is empty
function checkEmptyCart() {
  cart_counter = document.getElementById("cart_counter");
  if (cart_counter.innerHTML == 0) {
    document.getElementById("empty_cart").style.display = "block";
  }
}


function applyCartAmount(subtotal, tax, grand_total) {

  if (window.location.pathname == '/marketplace/cart') {
    $("#subtotal").html(subtotal.toFixed(2))
    $("#tax").html(tax.toFixed(2))
    $("#total").html(grand_total.toFixed(2))
  }
}