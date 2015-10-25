document.addEventListener('DOMContentLoaded', function() {
    var btn1 = document.getElementById('btn1');
 // onClick's logic below:
    btn1.addEventListener('click', function() {
      chrome.tabs.executeScript({
			code: 'document.body.style.backgroundColor="red"'
		});
    });
});
