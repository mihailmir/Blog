
var ArticlePage = (function() {
    let initial_data = {}
    let init = function (article_id, page, urls) {
        initial_data.article_id = article_id;
        initial_data.page = page;
        initial_data.urls = urls;
        update_comments.call(initial_data);
    }
    function update_comments() {
        $.ajax(this.urls["view_comment"], {
            type: 'get',
            data: { 'article_id': this.article_id, 'page': this.page},
            dataType: 'html',
            success : function(html) {
                $(".comment-block").html(html);
            },
            error: function() {
                alert("Error");
            }
        });
    }
    function add_comment(form) {
        $.ajax(form.attr('action'), {
            type: form.attr('method'),
            data: form.serialize(),
            success : function() {

                update_comments.call(initial_data);
                form.trigger('reset');
            },
            error: function() {
                alert("Error");
            }
        });
    }
    function reply_comment(comment_id) {
        let article_id = this.article_id;
        $.ajax(this.urls["add_comment"], {
            type: 'get',
            data: { 'article_id': article_id, 'comment_id': comment_id},
            dataType: 'html',
            success : function(html) {
                $(".reply-form-" + comment_id).html(html);
            },
            error: function() {
                alert("Error");
            }
        });
    }
    $(document).on('submit', '.add-comment' , function(e) {
        e.preventDefault();
        add_comment.call(initial_data, $(this));
    });

    $(document).on('click', '.view-next, .view-prev' , function(e) {
        e.preventDefault();
        initial_data.page = $(this).attr('page');
        update_comments.call(initial_data);
    });

    $(document).on('click', '.reply-button' , function(e) {
        e.preventDefault();
        let comment_id = $(this).attr('comment');
        let comment_container = $(".reply-form-" + comment_id);

        if ($(comment_container).is(':empty')){
            reply_comment.call(initial_data, comment_id)
        }
        else if ($(comment_container).is(':hidden')){
            comment_container.show();
        }
        else {
            comment_container.hide();
        }
    });
    return {'init': init}
}());

