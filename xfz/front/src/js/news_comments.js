function NewsComments() {

}

NewsComments.prototype.SendComment = function () {
    var submitBtn = $('.submit-comment');
    var comment_textarea = $('.comment-textarea');
    submitBtn.click(function () {
        var news_id = $('.article-title').find("h1[class='title']").attr('news_id');
        var content = comment_textarea.val();
        var comment_ul = $('.comment-list-ul');
        xfzajax.post({
            'url':'/news/add_comment/',
            'data':{
                'news_id':news_id,
                'content':content
            },
            'success':function (result) {
                if (result['code'] === 200) {
                    var tpl = template('comment-list',{
                        'comment':result['data']
                    });
                    comment_textarea.val('');
                    comment_ul.prepend(tpl);
                } else {
                    xfzajax.success(result['message'])
                }
            }
        })

    })
};

$(function () {
    var newscomment = new NewsComments();
    newscomment.SendComment();
});