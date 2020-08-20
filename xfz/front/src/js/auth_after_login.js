function AuthAfterLogin() {
}


AuthAfterLogin.prototype.show = function () {
    var authbox = $('.auth-box');
    var usermorebox = $('.user-more-box');
    authbox.hover(function () {
        usermorebox.show();
    }, function () {
        usermorebox.hide();
    })
};

$(function () {
    var auth_after_login = new AuthAfterLogin();
    auth_after_login.show();
    if (window.template) {
        template.defaults.imports.TimeSince = function (value) {
        var time = new Date(value);
        var timesince = time.getTime();
        var now = (new Date()).getTime();
        var timestamp = (now - timesince) / 1000;
        if (timestamp < 60) {
            return '刚刚';
        } else if (timestamp >= 60 && 60 * 60 > timestamp) {
            minutes = parseInt(timestamp / 60);

            return minutes + '分钟前';
        } else if (timestamp >= 60 * 60 && 60 * 60 * 24 > timestamp) {

            hours = parseInt(timestamp / 60 / 60);
            return hours + '小时前';
        } else if (timestamp >= 60 * 60 * 24 && timestamp < 60 * 60 * 24 * 30) {

            days = parseInt(timestamp / 60 / 60 / 24);
            return days + '天前';
        } else {
            var year = time.getFullYear();
            var month = time.getMonth();
            var day = time.getDay();
            var hours = time.getHours();
            var min = time.getMinutes();
            return year + '/' + month + '/' + day + ' ' + hours + ':' + min;
        }
    };
    }
});