// request permission on page load
document.addEventListener('DOMContentLoaded', function () {
  if (Notification.permission !== "granted")
    Notification.requestPermission();
});

var port = chrome.extension.connect({name: "Sample Communication"});
port.postMessage("Hi BackGround");
port.onMessage.addListener(function(url) {
  console.log("message recieved"+ url);
  $("#recommendation_url").text(url);
  $("#recommendation_url").href(url);
});

function notifyMe() {
  if (!Notification) {
    alert('Desktop notifications not available in your browser. Try Chromium.'); 
    return;
  }

  if (Notification.permission !== "granted")
    Notification.requestPermission();
  else {
    var notification = new Notification('Notification title', {
      icon: 'http://cdn.sstatic.net/stackexchange/img/logos/so/so-icon.png',
      body: "Hey there! You've been notified!",
    });

    notification.onclick = function () {
      window.open("http://stackoverflow.com/a/13328397/1269037");      
    };

  }

}
