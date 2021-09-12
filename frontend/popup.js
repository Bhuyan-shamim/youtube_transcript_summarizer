SummaryButton = document.getElementById('Summarize');
const xhr = new XMLHttpRequest();
SummaryButton.onclick = (e) => {
    e.preventDefault();
    console.log("popup.js");
    chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
        let url = tabs[0].url;
        var expression = /https?:\/\/(www\.)?youtube.com\/watch\b([v?=].*)/g
        var regex = new RegExp(expression);

        if (!url.match(regex))
            return;

        chrome.tabs.sendMessage(tabs[0].id, { action: "Load Summary" });



        xhr.onreadystatechange = function ajax_function() {
            chrome.tabs.sendMessage(tabs[0].id, { action: "Load Summary" });
            if (xhr.status == 200) {
                chrome.tabs.sendMessage(tabs[0].id, { "video_url": url, action: "Print_Summary", summary: JSON.parse(xhr.response) });
            } else {
                chrome.tabs.sendMessage(tabs[0].id, { action: "Load Summary" });
            }
        };
        // the api
        xhr.open("GET", 'https://9a8e-117-194-212-75.ngrok.io/api/get_summary?youtube_url=' + url, true);
        xhr.send();
    });
};