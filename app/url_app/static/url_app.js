/**
 * Function will display the new url above the url creation box for easy copying
 */
function displayShortenedUrl(urlId){
    var displayDiv = document.getElementById('url-display')
    var redirectUrl = `${window.location.origin}/url/${urlId}`;
    displayDiv.removeAttribute('hidden');
    var urlDisplay = document.getElementById('url-copy-box');
    urlDisplay.setAttribute('value', redirectUrl);
    //urlDisplay.innerHTML = `<a href="%{redirectUrl}">${redirectUrl}</a>`;
}

/**
 * Add an event listener for the copy url button which will highlight the
 * url and copy it to the clipboard
 */
document.getElementById('copy-url-btn').addEventListener('click', event => {
    var urlBox = document.getElementById('url-copy-box');
    urlBox.select();
    document.execCommand("copy");
});

/**
 * We dont want the form to actually submit, so we stop propagation with this function
 * then manually submit the form yourself
 */
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
