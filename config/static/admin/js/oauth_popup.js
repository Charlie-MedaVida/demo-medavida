// static/admin/js/oauth_popup.js
function openOAuthPopup(url) {
    var width = 600;
    var height = 600;
    var left = (screen.width / 2) - (width / 2);
    var top = (screen.height / 2) - (height / 2);
    window.open(
        url,
        "OAuthPopup",
        "width=" + width + ",height=" + height + ",top=" + top + ",left=" + left
    );
}

