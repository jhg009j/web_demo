function Auth() {
    this.AuthBoxPosition = $('.auth-group-box');
    this.MaskWrapper = $('.mask-wrapper');
}

// Auth.prototype.MaskWrapperControl = function () {
//     var self = this;
//
//     $('#btn').click(function () {
//        $('.mask-wrapper').show();
//     });
//
//     $('.close-btn').click(function () {
//         $('.mask-wrapper').hide();
//         self.AuthBoxPosition.css({'left':0});
//     });
// };

Auth.prototype.AuthBoxLeft = function () {
    var self = this;

    $('.auth-right').click(function () {
        var leftpx = self.AuthBoxPosition.css('left');
        var Intleftpx = parseInt(leftpx);

        if (Intleftpx < 0) {
            self.AuthBoxPosition.animate({'left': 0})
        } else {
            self.AuthBoxPosition.animate({'left': -400});
        }
    })

};

Auth.prototype.ShowEvent = function () {
    var self = this;
    self.MaskWrapper.show();
};

Auth.prototype.HideEvent = function () {
    var self = this;
    self.MaskWrapper.hide();
};

Auth.prototype.ListenShowHideEvent = function () {
    var self = this;
    var authbox = $('.auth-box');
    var close = $('.close-btn');
    var login_btn = authbox.find("a[class='login']");
    var signup_btn = authbox.find("a[class='signup']");
    close.click(function () {
        self.HideEvent();
        self.AuthBoxPosition.css({'left': 0});
    });

    login_btn.click(function () {
        self.ShowEvent();
    });

    signup_btn.click(function () {
        self.ShowEvent();
        self.AuthBoxPosition.css({'left': -400});
    });
};

Auth.prototype.ListenloginEvent = function () {
    var self = this;
    var LoginSelector = $('#login-btn');
    var TelephoneInput = LoginSelector.find("input[name='telephone']");
    var PasswordInput = LoginSelector.find("input[name='password']");
    var Remember = LoginSelector.find("input[name='remember']");
    var SubmitBtn = LoginSelector.find("input[id='login-submit']");
    SubmitBtn.click(function () {
        var telephone = TelephoneInput.val();
        var password = PasswordInput.val();
        var remember = Remember.prop('checked');
        console.log('ok');
        xfzajax.post({
            'url': '/account/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember ? 1 : 0
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    self.HideEvent();
                    window.location.reload();
                } else {
                    var error_messages = result['message'];
                    // if (typeof error_messages == 'string' ||
                    //     error_messages.constructor == String) {
                    //     // window.messageBox.ListenShowEvent(error_messages);
                    //     window.messageBox.ShowError(error_messages);
                    // } else {
                    //     for (var value in error_messages) {
                    //         msg = error_messages[value];
                    //         window.messageBox.ShowError(msg[0]);
                    //         console.log('ok')
                    //     }
                    // }
                    xfzajax.success(error_messages)
                }
            },
            'error': function (error) {
                window.messageBox.ShowError('服务器内部错误')
            }
        })
    })

};

Auth.prototype.ListenImgCap = function () {
    var self = this;
    var img_cap = $('.img-captcha');
    img_cap.click(function () {
        img_cap.attr('src', '/account/captcha/' + '?id=' + Math.random())
    })
};

Auth.prototype.ListenRegisterEvent = function () {
    var self = this;
    var SignupSelector = $('#signup-btn');
    var TelephoneInput = SignupSelector.find("input[name='telephone']");
    var UsernameInput = SignupSelector.find("input[name='username']");
    var Password1Input = SignupSelector.find("input[name='password1']");
    var Password2Input = SignupSelector.find("input[name='password2']");
    var ImgCaptchaInput = SignupSelector.find("input[name='inner-captcha']");
    var submitbtn = SignupSelector.find("input[id='signup-submit']");

    submitbtn.click(function () {
        var telephone = TelephoneInput.val();
        var username = UsernameInput.val();
        var password1 = Password1Input.val();
        var password2 = Password2Input.val();
        var img_captcha = ImgCaptchaInput.val();
        xfzajax.post({
            'url': '/account/register/',
            'data': {
                'telephone': telephone,
                'username': username,
                'password1': password1,
                'password2': password2,
                'img_captcha': img_captcha
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    self.HideEvent();
                    window.messageBox.Success('登录成功!');
                    window.location.reload();
                } else {
                    var error_messages = result['message'];
                    // if (typeof error_messages == 'string' ||
                    //     error_messages.constructor == String) {
                    //     // window.messageBox.ListenShowEvent(error_messages);
                    //     window.messageBox.ShowError(error_messages);
                    // } else {
                    //     for (var value in error_messages) {
                    //         msg = error_messages[value];
                    //         window.messageBox.ShowError(msg[0]);
                    //     }
                    // }
                    xfzajax.success(error_messages)
                }
            },
            'error': function (error) {
                window.messageBox.ShowError('服务器内部错误')
            }

        })
    })
};


$(function () {
    var auth = new Auth();
    auth.ListenShowHideEvent();
    auth.AuthBoxLeft();
    auth.ListenloginEvent();
    auth.ListenImgCap();
    auth.ListenRegisterEvent();
});


