function CousesCategory() {
}

CousesCategory.prototype.AddCategory = function () {
    var self = this;
    var addbtn = $('#add-btn');
    addbtn.click(function () {

        xfzalert.InputMessage('添加课程分类', '请输入分类名称', function (value) {
            xfzajax.post({
                'url': '/cms/add_course_category/',
                'data': {
                    'course_category': value
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        console.log(result);
                        window.location.reload();
                    } else {
                        xfzajax.success(result['message']);
                        xfzalert.Close();
                    }
                }
            })
        })
    })
};

CousesCategory.prototype.EditCategory = function () {
    var self = this;
    var editbtn = $('.edit-btn');
    editbtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('cate-pk');
        var cate_name = tr.attr('cate-name');
        xfzalert.InputMessage('修改课程分类名称', '请输入新的课程分类名称', function (value) {
            xfzajax.post({
                'url': '/cms/edit_course_category/',
                'data': {
                    'course_category': cate_name,
                    'pk': pk,
                    'new_category_name': value
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        console.log(result);
                        // xfzalert.SuccessMessage();
                        window.location.reload();
                    } else {
                        xfzajax.success(result['message']);
                        xfzalert.Close();
                    }
                }
            })
        })
    })
};

CousesCategory.prototype.DeleteCategory = function () {
    var self = this;
    var delbtn = $('.del-btn');
    delbtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('cate-pk');
        xfzalert.WarningMessage('删除课程分类', '请注意，删除后将无法恢复！', function () {
            xfzajax.post({
                'url': '/cms/del_course_category/',
                'data': {
                    'pk': pk
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        xfzalert.SuccessBox('删除课程分类', '分类删除成功！', function () {
                            window.location.reload();
                        })
                    }
                }
            })
        });
    })
};

$(function () {
    var cate = new CousesCategory();
    cate.AddCategory();
    cate.EditCategory();
    cate.DeleteCategory();
});