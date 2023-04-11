// AJAX functionality for leaderboard refreshing




async function refreshButton() {

    var ol = $("ol")

    $.ajax({
        url: 'leaderboardUpdate',
        type: 'get',
    
    success: function(response) {
        // Fetch the dictionaries from the response
        challengerList = response.challenged
        challengerNames = response.challengedNames

        // Get rid of the child elements in the orderedlist
        ol.empty();

        for (var i = 0; i < challengerList.length; i++) {
            
            // We have to manually inject html to the page
            // The HTML is taken directly from the leaderboard html page
            html = ("<li class='list-group-item d-flex justify-content-between align-items-start'><div class='ms-2'>  " +
            "<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' fill='currentColor' class='bi bi-person-circle' viewBox='0 0 16 16'> " +
            "<path d='M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z'/> <path fill-rule='evenodd' d='M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z'/> " +
            "</svg></div><div class='ms-2 me-auto'>" +
            "<div class='fw-bold'>" + challengerNames[i] + "</div>" +
            "[" + challengerList[i].postcode + "]</div>" +
            "<span class='badge bg-success rounded-pill'>" + challengerList[i].score + "</span></li>");
            

            // Add as a child element to the ordered list element
            ol.append(html)
        }

        // Load the ordered list, current causes a problem in JS Console but does not appear to affect functionality.
        ol.load()
        



    }
    
    
    
    
    
    
    })
}

// Run the script when document is loaded
window.onload = refreshButton;


// Allows for 'real time updates', function called on a timer. I would have loved to just called the function here but it doesnt work
setInterval(function() {

    var ol = $("ol")

    $.ajax({
        url: 'leaderboardUpdate',
        type: 'get',
    
    success: function(response) {
        challengerList = response.challenged
        challengerNames = response.challengedNames
        // challengerList = data.topChallengers

        // 
        ol.empty();

        for (var i = 0; i < challengerList.length; i++) {
            
            html = ("<li class='list-group-item d-flex justify-content-between align-items-start'><div class='ms-2'>  " +
            "<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' fill='currentColor' class='bi bi-person-circle' viewBox='0 0 16 16'> " +
            "<path d='M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z'/> <path fill-rule='evenodd' d='M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z'/> " +
            "</svg></div><div class='ms-2 me-auto'>" +
            "<div class='fw-bold'>" + challengerNames[i] + "</div>" +
            "[" + challengerList[i].postcode + "]</div>" +
            "<span class='badge bg-success rounded-pill'>" + challengerList[i].score + "</span></li>");
            


            ol.append(html)
        }

        ol.load()
        



    }
    

    
    })



// 3 second timer
}, 3000);