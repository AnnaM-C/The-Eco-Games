async function setFields(activityid){
  $('#aID').val(activityid);
}


$('#trModalButton').click(function(e) {
  e.preventDefault() 
  // Get the activity ID and log time from the modal's form fields
  var activityId = $('#aID').val();
  var duration = $('#duration').val();
  var time = document.getElementById('ltime3').value;
  var csrf_token = $('[name="csrfmiddlewaretoken"]').val(); // Retrieve CSRF token from the form
  // Send the data to the server using AJAX
  $.ajax({
    url: '/game/addTime',
    method: 'POST',
    data: {
      activityId: activityId,
      duration: duration,
      time: time,
    },
    headers: {
        'X-CSRFToken': csrf_token // Include CSRF token in headers
    },
    success: function(data) {
      // Data is in the form of whatever the server sends back from return HTTPResponse("reformatted line item")
      if (data.not_cart_success == false) { 
        alert("You have logged this activity today. Try again tomorrow!");
      } else if (data.cart_success == false) { 
        alert("Activity is already in your cart.");
      } else {
        console.log("Data successfully sent to the server.");
        updateCart(data);
      }
      // TODO: Add any necessary UI updates or redirections
      $('#trModal').modal('hide');
    },
    error: function(xhr, status, error) {
      console.log(error);
      // TODO: Handle the error 
    }
  });
});


$('#ntrModalButton').click(function(e) {
  e.preventDefault() 
  // Get the activity ID and log time from the modal's form fields
  var activityId = $('#aID').val();
  console.log("test")
  var time = document.getElementById('ltime4').value;
  var duration=0;
  var csrf_token = $('[name="csrfmiddlewaretoken"]').val(); // Retrieve CSRF token from the form
  // Send the data to the server using AJAX
  $.ajax({
    url: '/game/addTime',
    method: 'POST',
    data: {
      activityId: activityId,
      duration: duration,
      time: time,
    },
    headers: {
        'X-CSRFToken': csrf_token // Include CSRF token in headers
    },
    success: function(data) {
      // Data is in the form of whatever the server sends back from return HTTPResponse("reformatted line item")
      if (data.not_cart_success == false) { 
        alert("You have logged this activity today. Try again tomorrow!");
      } else if (data.cart_success == false) { 
        alert("Activity is already in your cart.");
      } else {
        console.log("Data successfully sent to the server.");
        updateCart(data);
      }
      // UI updates
      $('#tnrModal').modal('hide');
    },
    error: function(xhr, status, error) {
      console.log(error);
    }
  });
});

// Here data is the lineItemcreated. This is the last thing that triggers. It accumulates the activity title on the server
// into a tag line item inbetween calling AJAX and entering the success loop.
function updateCart(data) {
  console.log(data)
  $('.shopping-cart').append(data);
}


// function recordPoints() {
//   e.preventDefault(); 
//   var elements = $(".line-item");
//   var csrf_token = $('[name="csrfmiddlewaretoken"]').val(); // Retrieve CSRF token from the form
//   // Extract relevant data from elements
//   var elementData = [];
//   for (var i = 0; i < elements.length; i++) {
//     id = parseInt(elements[i].getAttribute('name'))
//     elementData.push(id);
//   }
//   console.log(elementData);
//   $.ajax({
//     url: '/game/recordPoints',
//     method: 'POST',
//     // data: JSON.stringify(elementData),
//     data: {
//       'list_items': elementData,
//     },
//     headers: {
//       'X-CSRFToken': csrf_token // Include CSRF token in headers
//     },
//     success: function(response) {
//       // Do something with the data you defined on the server and then came here
//       console.log(response);
//       console.log("test");
//       window.location.reload();
//     },
//     error: function() {
//       console.log("Something went wrong.");
//     }
//   });
//   console.log("end")
// }
