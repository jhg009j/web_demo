function CoursePub() {

}

CoursePub.prototype.CoursePublication = function () {
    var self = this;
    var pubBtn = $('#pub-btn');
    pubBtn.click(function (event) {
        event.preventDefault();
        var title = $("input[name='title']").val();
        var teacher = $("input[name='teacher_name_id']").val();
        var category = $("select[name='category']").val();
        var abstract = $("textarea[name='abstract']").val();
        var course_pic = $("input[name='course-pic']").val();
        var course_id = $('.form-group').attr('courseId');
        var url = null;
        if (course_id) {
            url = '/cms/course_edit/'
        } else {
            url = '/cms/course_pub/'
        }
        xfzajax.post({
            'url': url,
            'data': {
                'name': title,
                'category': category,
                'abstract': abstract,
                'course_id': course_id,
                'teacher': teacher,
                'picture': course_pic
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    if (course_id) {
                        xfzalert.SuccessBox('修改成功！', '课程修改成功！', function () {
                            window.location.reload();
                        })
                    } else {
                        xfzalert.SuccessBox('添加成功！', '课程添加成功！', function () {
                            window.location.reload();
                        })
                    }
                } else {
                    xfzajax.success(result['message'])
                }
            }
        })
    })
};

CoursePub.prototype.UploadAvatar = function () {
    var picture_btn = $('#picture-btn');
    picture_btn.change(function () {
        var file = picture_btn[0].files[0];
        var formdata = new FormData();
        var course_picture = 1;
        formdata.append('file', file);
        formdata.append('course_picture', course_picture);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formdata,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    var url = (result['data']['url']);
                    var pic_form = $('#pic-form');
                    pic_form.val(url);
                } else {
                    xfzajax.success(result['message'])
                }
            }
        })
    })
};

$(function () {
    var coursepub = new CoursePub();
    coursepub.CoursePublication();
    coursepub.UploadAvatar();
});