function Banner() {
    this.index = 1;
    this.bannerGroup = $('#navsroll');
    this.toggleArrow = $('.arrow');
    this.leftArrow = $('.left-arrow');
    this.rightArrow = $('.right-arrow');
    this.bannerUl = $('#navsrollul');
    this.lilist = this.bannerUl.children('li');
    this.liCount = this.lilist.length;
    this.pageControl = $('.page-control');

}

Banner.prototype.InitBannerUl = function () {
    var self = this;
    var FirstBanner = self.bannerUl.children('li').eq(0).clone();
    var LastBanner = self.bannerUl.children('li').eq(self.liCount - 1).clone();
    self.bannerUl.append(FirstBanner);
    self.bannerUl.prepend(LastBanner);
    self.bannerUl.css({'width': 796 * (self.liCount + 2)});
    self.bannerUl.css({'left': -796});
};

Banner.prototype.run = function () {
    var self = this;
    this.timecon = setInterval(function () {
        if (self.index < (self.liCount + 1)) {
            self.index += 1;
        } else if (self.index === self.liCount + 1) {
            self.bannerUl.css({'left': -796});
            self.index = 2;
        }
        self.animate();
        self.FollowRunPageControl();

    }, 2000);
};

Banner.prototype.animate = function () {
    var self = this;
    self.bannerUl.stop().animate({'left': -796 * self.index}, 500)
};

Banner.prototype.InitPageControl = function () {
    var self = this;
    var i = 0;
    for (i === 0; i < self.liCount; i++) {
        var liTag = $('<li></li>');
        self.pageControl.append(liTag);
        if (i === 0) {
            liTag.addClass('active');
        }
    }
    self.pageControl.css({'width': 12 * self.liCount + 8 * 2 + 16 * (self.liCount - 1)})
};

Banner.prototype.ClickPageControl = function () {
    var self = this;
    self.pageControl.children('li').each(function (index, obj) {
        $(obj).click(function () {
            if (index === 0) {
                self.index = 1;
            } else if (index === 3) {
                self.index = 4;
            } else {
                self.index = index + 1;
            }
            $(obj).addClass('active').siblings().removeClass('active');
            self.animate()
        })
    })
};

Banner.prototype.FollowRunPageControl = function () {
    var self = this;
    var index = self.index;
    if (index === self.liCount + 1) {
        index = 0;
    } else if (index === 0) {
        index = self.liCount - 1;
    } else {
        index = index - 1;
    }
    self.pageControl.children('li').eq(index).addClass('active').siblings().removeClass('active');
};

Banner.prototype.MouseHoverListen = function () {
    var self = this;
    self.bannerGroup.hover(function () {
        clearInterval(self.timecon);
        self.toggleArrow.show();
    }, function () {
        self.toggleArrow.hide();
        self.run();
    })
};

Banner.prototype.ArrowClick = function () {
    var self = this;
    self.leftArrow.click(function () {
        if (self.index === 0) {
            self.bannerUl.css({'left': -796 * self.liCount});
            self.index = self.liCount - 1;
        } else {
            self.index -= 1
        }
        self.FollowRunPageControl();
        self.animate()
    });

    self.rightArrow.click(function () {
        if (self.index === self.liCount + 1) {
            self.bannerUl.css({'left': -796});
            self.index = 2;
        } else {
            self.index += 1
        }
        self.animate();
        self.FollowRunPageControl();
    });
};

function NewsList() {
    this.next_page = 2;

    this.category_id = 0;
    this.loadBtn = $('#load-more-btn');

}


NewsList.prototype.LoadMore = function () {
    var self = this;
    self.loadBtn.click(function () {
        xfzajax.get({
            'url': '/news/more/',
            'data': {
                'p': self.next_page,
                'category_id':self.category_id
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var newslist = result['data'];
                    if (newslist.length > 0) {
                        var tpl = template('news-load', {'newslist': newslist});
                        var ul = $(".news-list-ul");
                        ul.append(tpl);
                        self.next_page += 1;
                    } else {
                        self.loadBtn.hide();
                    }
                }
            }
        })
    })
};

NewsList.prototype.DifferCategory = function () {
    var self = this;
    var ul = $('.news-guide-list');
    var atag = ul.children().children();
    atag.click(function () {
        var a = $(this);
        //找到a的父元素li，找到li的子元素a移除class
        a.addClass('active').parent().siblings().children().removeClass('active');
        self.category_id = a.attr('category-id');
        xfzajax.get({
            'url': '/news/differ_cate/',
            'data': {
                'category_id': self.category_id
            },
            'success': function (result) {
                var newslist = result['data'];
                var news_list_group = $('.news-list-ul');
                news_list_group.empty();
                var tpl = template('news-load', {'newslist': newslist});
                news_list_group.append(tpl);
                self.loadBtn.show();
                self.next_page = 2;
            }
        });

    })
};

$(function () {
    var banner = new Banner();
    banner.run();
    banner.MouseHoverListen();
    banner.ArrowClick();
    banner.InitPageControl();
    banner.ClickPageControl();
    banner.InitBannerUl();

    var newslist = new NewsList();
    newslist.LoadMore();
    newslist.DifferCategory();
});