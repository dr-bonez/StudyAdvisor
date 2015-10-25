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
    $.ajax({
        type: "POST",
        url: "http://23.96.26.252:5000/.json",
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
        }
    });
    console.log("finished");
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
});