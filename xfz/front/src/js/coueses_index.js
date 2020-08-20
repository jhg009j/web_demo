function CouesesIndex() {

}


CouesesIndex.prototype.Category = function () {
    var self = this;
    self.courseul = $('.course-list-ul');
    self.categoryul = $('.courses-ul');
    self.categoryli = self.categoryul.children();
    var firstcate = self.categoryli.first();
    firstcate.addClass('active');

    this.categoryli.click(function () {
        var li_list = $(this);
        li_list.addClass('active').siblings().removeClass('active');
        var cateid = li_list.attr('cateid');
        xfzajax.get({
            'url': '/courses/course_deffer_cate/',
            'data': {
                'cateid': cateid
            },
            'success': function (result) {
                if (result['code'] === 200){
                    var courses = result['data'];
                    var tpl = template('course-index', {'courses': courses});
                    self.courseul.empty();
                    self.courseul.append(tpl)
                }
            }
        })
    })
};


$(function () {
    category = new CouesesIndex();
    category.Category();
});