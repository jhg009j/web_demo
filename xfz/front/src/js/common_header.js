function Header() {
    this.nav = $('.nav');
}

Header.prototype.HeaderClickEvent = function () {
    var localurl = window.location.href;
    var liTag = $('.nav ul li a');
    for (var i=0; i<liTag.length; i++) {
        if (localurl.toLowerCase() === liTag[i].href.toLowerCase()) {
             liTag[i].parentElement.className='active'
        }
    }
};

$(function () {
    var header = new Header();
    header.HeaderClickEvent();
});