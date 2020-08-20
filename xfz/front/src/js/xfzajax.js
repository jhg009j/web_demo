function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var xfzajax = {
    'post': function (args) {
        args['type'] = 'post';
        this._ajaxsetup();
        this.ajax(args);
    },
    'get': function (args) {
        args['type'] = 'get';
        this.ajax(args)
    },
    '_ajaxsetup': function () {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    },
    'ajax': function (args) {
        $.ajax(args);
    },
    'success': function (error_messages) {
        if (typeof error_messages == 'string' ||
            error_messages.constructor == String) {
            // window.messageBox.ListenShowEvent(error_messages);
            window.messageBox.ShowError(error_messages);
        } else {
            for (var value in error_messages) {
                msg = error_messages[value];
                window.messageBox.ShowError(msg[0]);
            }
        }
    }
};
