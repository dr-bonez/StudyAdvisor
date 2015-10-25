/*chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
    if (changeInfo.status == 'complete' && tab.active) {
        $.post("23.96.26.252:5000/.json",
            {
                url: "https://google.com",
                referef: "http://google.com",
                device: "mycomp"
            },
            function(data, status){
                alert("Data: " + data + "\nStatus: " + status);
            });
        alert("Post request executed.")
    }
});*/

var studyModeEnabled = false;

chrome.webNavigation.onCompleted.addListener(function(details) {
    console.log("foo bar baz");
  /*  var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            // JSON.parse does not evaluate the attacker's scripts.
            var resp = JSON.parse(xhr.responseText);
        }
    }
    xhr.open("POST", "http://23.96.26.252:5000/.json", true);
    xhr.send(encodeURIComponent("url=http://www.jewfaq.org/") + "&referer=" +
        encodeURIComponent("http://www.britannica.com/topic/judaism") + "&device=" + encodeURIComponent("mycomp"));
});




    $.ajax({
        url: 'css/style.css',
        type: 'GET',
        data: {
            searchtext: $("#request").val(),
            app_id: 'qB42RwI8Kum9fXo2xpsJ',
            app_code: 'XcdhsTMx5naHN3Zi-e6_iQ',
            gen: '8'
        },
        success: function (data) {
            alert("ajax happened");
            /!*latLong = data.Response.View[0].Result[0].Location.DisplayPosition;
            if (requestMarker != null && requestMarker != undefined)
                map.removeObject(requestMarker);
            requestMarker = new H.map.Marker({lat:latLong.Latitude, lng:latLong.Longitude},{icon : dicon});
            map.addObject(requestMarker);
            map.setCenter({lat:latLong.Latitude, lng:latLong.Longitude});
            polling = true;*!/
        }
    });*/

    $.ajax({
        type: "POST",
        url: "http://localhost:5000/.json",
        dataType: "application/json",
        data: {
            url: "http://www.jewfaq.org/",
            referef: "http://www.religionfacts.com/judaism/",
            device: "mycomp"
        },
        success: function(data) {
            alert("Data: " + data);
            console.log("success");
        },

        error: function(data) {
            console.log('failed');
        },
        done: function() {
            console.log("finished");
        }
    });});
    /*$.ajax({
        url: "http://23.96.26.252:5000/.json",
        type: "POST",
        dataType: "json",
        data: {
            url: "https://google.com",
            referef: "http://google.com",
            device: "mycomp"
        },
        success: function(data) {
            alert("Data: " + data);
        }
    });*/
    /*alert("Post request executed.")*/