function TeacherManager() {
    this.ClearBtn = $('.clear-search');
}

TeacherManager.prototype.ClearSearchInfo = function () {
    var self = this;
    self.ClearBtn.click(function () {
        var keyword = $('#InputKeyword');
        var teacherid = $('#InputTeacherId');
        keyword.val('');
        teacherid.val('');
    })
};

TeacherManager.prototype.DeleteTeacher = function () {
    var self = this;
    var DelBtn = $('.del-btn');
    DelBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var teacherid = tr.attr('teacher-id');
        xfzalert.WarningMessage('删除讲师信息', '请注意，删除后将无法恢复！', function () {
            xfzajax.post({
                'url': '/cms/del_teacher/',
                'data': {
                    'pk': teacherid
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        xfzalert.SuccessBox('删除讲师信息', '信息删除成功！', function () {
                            window.location.reload();
                        })
                    } else {
                        xfzajax.success(result['message'])
                    }
                }
            })
        })
    })
};

$(function () {
    var teachermanager = new TeacherManager();
    teachermanager.ClearSearchInfo();
    teachermanager.DeleteTeacher();
});