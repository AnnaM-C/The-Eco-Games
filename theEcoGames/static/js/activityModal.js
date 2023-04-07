
// var button=document.getElementById("activityButton-16")
// var activity

// Click button to open modal. 
// Input value needs to be added to a line items 'activityDuration' field.
    // Send to the server the activityId and userInput. On server-side. activity=Activity.Objects.get(id=response.get(data:activityId)). lineItem=LineItem.Objects.get(activity=activity). update the field somehow, field=getAttr(lineItem, 'activityDuration'). Field=response.get(data:userInput)
// button16.addEventListener('click', (e) => {
//     e.preventDefault();
//     console.log("button16 clicked")
    // Get user input
// })



// // JavaScript code
// $(document).ready(function() {
//     $('.log-time-button').click(function(event) {
//       var activityId = this.id;
//    // Set the activity ID in the modal's hidden input field
//    $('#aID').val(activityId);
// });

async function setFields(activityid){
  $('#aID').val(activityid);
  document.getElementById('logTime').value = '';
}




// async function setFields(activityid, activityType){
//     $('#aID').val(activityid);
//     $.ajax({
//       url: '/game/setDurationField',
//       method: 'GET',
//       data: {
//         'activityType': activityType,
//       },
//       success: function(data) {
//         // get the class you want to put the data in and call .append(data)
//         if(activityType == 'TR') {
//           $('.modal-body').append(data);
//         } else {

//         }
//       }
//     });
// }

$('#trModalButton').click(function(e) {
  // Get the activity ID and log time from the modal's form fields
  var activityId = $('#aID').val();
  var duration = $('#duration').val();
  var time = $('#logTime').val();
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
      $('#trModal').trigger("reset");
    },
    error: function(xhr, status, error) {
      console.log(error);
      // TODO: Handle the error 
    }
  });
});

$('#ntrModalButton').click(function(e) {
  // Get the activity ID and log time from the modal's form fields
  var activityId = $('#aID').val();
  var time = $('#logTime').val();
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
      // TODO: Add any necessary UI updates or redirections
      $('#tnrModal').modal('hide');
      $('#tnrModal').trigger("reset");
    },
    error: function(xhr, status, error) {
      console.log(error);
      // TODO: Handle the error 
    }
  });
});

// Here data is the lineItemcreated. This is the last thing that triggers. It does soem stuff on the server
// inbetween calling AJAX and entering the success loop.
function updateCart(data) {
  console.log(data)
  // $('.shopping-cart').append('<h5 class="line-item card-title">' + data + '</h5>');
  $('.shopping-cart').append(data);
}


function recordPoints() {
  var elements = $(".line-item");
  var csrf_token = $('[name="csrfmiddlewaretoken"]').val(); // Retrieve CSRF token from the form
  // Extract relevant data from elements
  var elementData = [];
  for (var i = 0; i < elements.length; i++) {
    id = parseInt(elements[i].getAttribute('name'))
    elementData.push(id);
  }
  console.log(elementData);
  $.ajax({
    url: '/game/recordPoints',
    method: 'POST',
    // data: JSON.stringify(elementData),
    data: {
      'list_items': elementData,
    },
    headers: {
      'X-CSRFToken': csrf_token // Include CSRF token in headers
    },
    success: function(response) {
      // Do something with the data you defined on the server and then came here
      console.log(response);
    },
    error: function() {
      console.log("Something went wrong.");
    }
  });
}


