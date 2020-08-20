function NewsPub() {

}

NewsPub.prototype.FileUpload = function () {
    var self = this;
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formdata = new FormData();
        //此处通过ajax->FormData决定发送给后端的文件的name名称
        //若使用表单，name应该在input标签中设置
        formdata.append('file', file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formdata,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    var url = (result['data']['url']);
                    var thumbnail_form = $('#thumbnail-form');
                    thumbnail_form.val(url);
                } else {
                    xfzajax.success(result['message'])
                }
            }
        })
    })
};

NewsPub.prototype.NewsPublication = function () {
    var self = this;
    var pubBtn = $('#pub-btn');
    pubBtn.click(function (event) {
        event.preventDefault();
        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = $("textarea[name='content']").val();
        var news_id = $('.form-group').attr('newsId');
        var url = null;
        if (news_id) {
            url = '/cms/news_edit/'
        } else {
            url = '/cms/news_pub/'
        }
        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content,
                'news_id': news_id
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    if (news_id) {
                        xfzalert.SuccessBox('操作成功！', '文章修改成功！', function () {
                            window.location.reload()
                        })
                    } else {
                        xfzalert.SuccessBox('操作成功！', '文章发布成功！', function () {
                            window.location.reload()
                        })
                    }
                } else {
                    xfzajax.success(result['message'])
                }
            }
        })
    })
};

$(function () {
    var newspub = new NewsPub();
    newspub.FileUpload();
    newspub.NewsPublication();
});