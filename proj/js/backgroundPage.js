var studyModeEnabled = true;
var current_url;
var referer;

var com_port;
var url_rec;

function get_url() {
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs) {
        console.log(tabs[0].url);
        current_url = tabs[0];
        return tabs[0];
    });
}

chrome.extension.onConnect.addListener(function(port) {
    console.log("Connected .....");
    port.onMessage.addListener(function(msg) {
        com_port = port;
        console.log("message recieved"+ msg);
        port.postMessage(url_rec);
    });
});

function get_device() {
    return "mycomp";
}

function display_link(data){

}

chrome.extension.onRequest.addListener(function(request, sender, sendResponse) {
    referer = request.ref;
});

chrome.webNavigation.onCompleted.addListener(function(details) {
    console.log("foo bar baz");
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/.json",
        dataType: "application/json",
        data: {
            url: get_url(),
            referer: referer,
            device: get_device()
        },
        success: function(data) {
            alert("Data: " + data);
            console.log("success");
            display_link(data);
            arr = eval(data);
            url_rec = arr[0];
            com_port(url_rec);
        },

        error: function(data) {
            console.log('failed');
        },
        done: function() {
            console.log("finished");
        }
    });
});