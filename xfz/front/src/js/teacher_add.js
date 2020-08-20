function TeacherAdd() {

}

TeacherAdd.prototype.UploadAvatar = function () {
    var avatar_btn = $('#avatar-btn');
    avatar_btn.change(function () {
        var file = avatar_btn[0].files[0];
        var formdata = new FormData();
        var teacher_avatar = 1;
        formdata.append('file', file);
        formdata.append('teacher_avatar', teacher_avatar);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formdata,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    var url = (result['data']['url']);
                    var avatar_form = $('#avatar-form');
                    avatar_form.val(url);
                } else {
                    xfzajax.success(result['message'])
                }
            }
        })
    })
};

TeacherAdd.prototype.TeacherPublication = function () {
    var self = this;
    var pubBtn = $('#pub-btn');
    pubBtn.click(function (event) {
        event.preventDefault();
        var teacher_name = $("input[name='teacher-name']").val();
        var teacher_title = $("input[name='teacher-title']").val();
        var teacher_intro = $("textarea[name='teacher-intro']").val();
        var teacher_avatar = $("input[name='teacher-avatar']").val();
        var teacherId = $('.form-group').attr('teacherId');
        var url = null;
        if (teacherId) {
            url = '/cms/teacher_edit/'
        } else {
            url = '/cms/teacher_add/'
        }
        xfzajax.post({
            'url': url,
            'data': {
                'name': teacher_name,
                'title': teacher_title,
                'intro': teacher_intro,
                'pk': teacherId,
                'avatar': teacher_avatar
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    if (teacherId) {
                        xfzalert.SuccessBox('操作成功！', '讲师信息修改成功！',function () {
                            window.location.reload()
                        });

                    } else {
                        xfzalert.SuccessBox('操作成功！', '讲师添加成功！',function () {
                            window.location.reload()
                        });

                    }
                } else {
                    xfzajax.success(result['message'])
                }
            }
        })
    })
};

$(function () {
    var teacheradd = new TeacherAdd();
    teacheradd.TeacherPublication();
    teacheradd.UploadAvatar();
});