//var studyModeEnabled = true;
var current_url = undefined;
var referer;

//var com_port;
var url_rec;

function get_url() {  // ?!?! Actually returns the referer
    chrome.tabs.query({'active': true, 'windowId': chrome.windows.WINDOW_ID_CURRENT},
        function(tabs){
            current_url = tabs[0].url;
        }
    );
    return current_url;
}

function get_device() {
    return "mycomp";
}

function display_link(link){
    if(typeof link == "undefined"){
        alert("We do not have a recommendation for you at this time.");
    }
    else{
        alert("You may be interested in "+link);
    }
}

chrome.runtime.onMessage.addListener(function(request, sender, callback) {
    if (request.type == 'rec') {
        chrome.tabs.executeScript( null, {code:"var x = 10; x"},
            function(results){ display_link(url_rec) } );
    }
});

chrome.webNavigation.onCompleted.addListener(function(details) {
    console.log("foo bar baz");
    if(get_url() == undefined){
        console.log('null');
    }else {
        console.log(get_url());
        $.ajax({
            type: "POST",
            url: "http://localhost:5000/.json",
            data: {
                url: get_url(),
                referer: referer,
                device: get_device()
            }}).success(function (data) {
                //alert("Data: " + data);
                console.log("success");
                arr = JSON.parse(data);
                url_rec = arr[0];
                //com_port(url_rec);
            }).error(function (data) {
                console.log('failed');
                arr = JSON.parse(data);
            }).done(function () {
                console.log("finished");
            });
    }
});