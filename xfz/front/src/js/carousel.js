function CarouselManager() {
    this.carouselBox = $('.carousel-box');
}

CarouselManager.prototype.AddNewCarousel = function () {
    var self = this;
    var addBtn = $('.add-carousel-btn');
    addBtn.click(function () {
        var tpl = template('carousel-card');
        var carouselBoxlength = self.carouselBox.children().length;
        if (carouselBoxlength >= 4) {
            window.messageBox.ShowError('最多添加4张轮播图！');
        } else {
            self.carouselBox.prepend(tpl);
        }
    });
};

CarouselManager.prototype.ImgLoad = function () {
    var self = this;
    self.carouselBox.on('click', '.carousel-img-add', function () {
        var that = $(this);
        var imgload = that.siblings();
        imgload.off('click').click();
        imgload.change(function () {
            var file = this.files[0];
            var formdata = new FormData();
            var carousel_tag = 1;
            formdata.append('file', file);
            formdata.append('carousel_tag', carousel_tag);
            xfzajax.post({
                'url': '/cms/upload_file/',
                'data': formdata,
                'processData': false,
                'contentType': false,
                'success': function (result) {
                    if (result['code'] === 200) {
                        var url = result['data']['url'];
                        that.attr('src', url);
                    }
                }
            })
        });
    });
};

CarouselManager.prototype.RemoveButton = function () {
    var self = this;
    self.carouselBox.on('click', '.carousel-close-btn', function () {
        var that = $(this);
        var this_Box = that.parent().parent().parent();
        var carousel_id = this_Box.attr('carousel_id');
        if (carousel_id) {
            xfzalert.WarningMessage('删除轮播图', '请注意，删除后将无法恢复！', function () {
                xfzajax.post({
                    'url': '/cms/del_carousel/',
                    'data': {
                        'carousel_id': carousel_id
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            xfzalert.SuccessBox('删除成功！', '轮播图已删除！', function () {
                                this_Box.remove();
                            })
                        }
                    }
                })
            })
        } else {
            this_Box.remove();
        }
    })
};

CarouselManager.prototype.SaveCarousel = function () {
    var self = this;
    self.carouselBox.on('click', '.save-carousel-btn', function () {
        var that = $(this);
        var priorityInputBox = that.parent().siblings('.card-body').find("input[name='priority']");
        var link_toInputBox = that.parent().siblings('.card-body').find("input[name='link_to']");
        var ImgUrlBox = that.parent().siblings('.card-body').find('.carousel-img-add');
        var CardBox = that.parent().parent();

        var priorityInput = priorityInputBox.val();
        var link_toInput = link_toInputBox.val();
        var ImgUrl = ImgUrlBox.attr('src');
        var CarouselId = CardBox.attr('carousel_id');
        var Url = null;
        var priority = null;
        if (CarouselId) {
            Url = '/cms/edit_carousel/';
        } else {
            Url = '/cms/add_carousel/';
        }
        xfzajax.post({
            'url': Url,
            'data': {
                'carousel_url': ImgUrl,
                'link_to': link_toInput,
                'priority': priorityInput,
                'carousel_id': CarouselId
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    if (CarouselId) {
                        priority = result['data']['priority'];
                        CardBox.find('.priority-text').text('优先级:'+priority);
                        window.messageBox.Success('轮播图修改成功！');
                    } else {
                        var carousel_id = result['data']['carousel_id'];
                        priority = result['data']['priority'];
                        CardBox.attr('carousel_id', carousel_id);
                        CardBox.find('.priority-text').text('优先级:'+priority);
                        window.messageBox.Success('轮播图添加成功！');
                    }
                } else {
                    xfzajax.success(result['message'])
                }
            }
        })

    })
};

$(function () {
    var carousel = new CarouselManager();
    carousel.AddNewCarousel();
    carousel.ImgLoad();
    carousel.RemoveButton();
    carousel.SaveCarousel();
});
