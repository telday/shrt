
document.getElementById('copy-url-btn').addEventListener('click', event => {
    var urlBox = document.getElementById('url-copy-box');
    urlBox.select();
    document.execCommand("copy");
});

function displayShortenedUrl(urlId){
    var displayDiv = document.getElementById('url-display')
    var redirectUrl = `${window.location.origin}/url/${urlId}`;
    displayDiv.removeAttribute('hidden');
    var urlDisplay = document.getElementById('url-copy-box');
    urlDisplay.setAttribute('value', redirectUrl);
    //urlDisplay.innerHTML = `<a href="%{redirectUrl}">${redirectUrl}</a>`;
}

document.getElementById('shorten-url-btn').addEventListener('click', event => {
    event.preventDefault();
    var data = new FormData(event.target.parentNode);
    
    $.ajax({
        type: "POST",
        enctype: 'multipart/form-data',
        url: '/api/',
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 80000,
        success: data => {
            displayShortenedUrl(data);
        },
        error: e => {
            console.log(data);
        }
    });
});
