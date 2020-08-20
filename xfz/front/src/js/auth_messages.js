function Messages() {
    this.wrapperHeight = 48;
    this.wrapperWidth = 300;
    this.isAppended = false;
    this.InitElement();
    this.ListenCloseEvent();
}

Messages.prototype.InitElement = function () {
    var self = this;
    self.wrapper = $('<div></div>');
    self.closebtn = $('<span>×</span>');
    self.messagespan = $('<span class="xfz-auth-message"></span>');

    self.wrapper.css({
        'padding': '10px',
        'font-size': '14px',
        'width': '300px',
        'position': 'fixed',
        'z-index': '1100',
        'left': '50%',
        'top': '-48px',
        'margin-left':'-150px',
        'height': '48px',
        'box-sizing': 'border-box',
        'border': '1px solid #ddd',
        'border-radius': '4px',
        'line-height': '24px',
        'font-weight': 700,
        'background': '#fff'
    });
    self.closebtn.css({
        'font-family': 'core_sans_n45_regular,"Avenir Next","Helvetica Neue",Helvetica,Arial,"PingFang SC","Source Han Sans SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi MicroHei",sans-serif;',
        'font-weight': '700',
        'float': 'right',
        'cursor': 'pointer',
        'font-size': '22px'
    });

    self.wrapper.append(self.messagespan);
    self.wrapper.append(self.closebtn);
};

Messages.prototype.ListenCloseEvent = function () {
    var self = this;
    self.closebtn.click(function () {
        self.CloseEvent();
    })
};

Messages.prototype.CloseEvent = function () {
    var self = this;
    self.wrapper.animate({'top': -self.wrapperHeight});
};

Messages.prototype.ShowEvent = function () {
    var self = this;
    self.wrapper.animate({'top': 0});
};

Messages.prototype.ListenShowEvent = function () {
    var self = this;
    if (!self.isAppended) {
        $(document.body).append(self.wrapper);
        self.isAppended = true;
    }
    self.ShowEvent();
    setTimeout(function () {
        self.CloseEvent();
    },2000)
};

Messages.prototype.ShowError = function (message) {
    var self = this;
    self.messagespan.text(message);
    self.ListenShowEvent();

};

Messages.prototype.Success = function (message) {
    var self = this;
    self.messagespan.text(message);
    self.ListenShowEvent();

};

window.messageBox = new Messages();