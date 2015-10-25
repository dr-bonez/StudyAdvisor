chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
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
});