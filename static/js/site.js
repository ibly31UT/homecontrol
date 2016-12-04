function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function postWithJson(url, data, onSuccess, onFail){
    var settings = {
        url: url,
        method: "POST",
        data: JSON.stringify(data),
        dataType: "json",
        contentType: "application/json",
        success: function(response){
            if(response["status"] == "success"){
                onSuccess(response["payload"]);
            }else{
                console.log("Error, POST on URL: \"" + url + "\", message: " + response["message"]);
            }
        },
        error: function(error){
            console.log("Error POST with JSON on URL: \"" + url + "\"");
            console.log(error);
            if(onFail !== undefined){
                onFail(error);
            }
        }
    };
    $.ajax(settings);
}