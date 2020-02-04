
var ArticlePage = (function() {
    self = this;
    init = function (article_id, page, urls) {
        self.article_id = article_id;
        self.page = page;
        self.urls = urls;
        self.update();
    }
    update = function() {
        $.ajax(self.urls["view_comment"], {
            type: 'get',
            data: { 'article_id': self.article_id, 'page': self.page},
            dataType: 'html',
            success : function(html) {
                $(".comment-block").html(html);
            },
            error: function() {
                alert("Error");
            }
        });
    }
    add_comment = function() {
        $.ajax(form.attr('action'), {
            type: self.form.attr('method'),
            data: self.form.serialize(),
            success : function() {
                self.update();
                form.trigger('reset');
            },
            error: function() {
                alert("Error");
            }
        });
    }
    $(document).on('submit', '.add-comment' , function(e) {
        e.preventDefault();
        self.form = $(this);
        add_comment();
    });

    $(document).on('click', '.view-next, .view-prev' , function(e) {
        e.preventDefault();
        self.page = $(this).attr('page');
        self.update();
    });

    $(document).on('click', '.reply-button' , function(e) {
        e.preventDefault();
        let comment_id = $(this).attr('comment');
        let comment_container = $(".reply-form-" + comment_id);

        if ($(comment_container).is(':empty')){
            $.ajax(self.urls["add_comment"], {
                type: 'get',
                data: { 'article_id': self.article_id, 'comment_id': comment_id},
                dataType: 'html',
                success : function(html) {
                    $(".reply-form-" + comment_id).html(html);
                },
                error: function() {
                    alert("Error");
                }
            });
        }
        else if ($(comment_container).is(':hidden')){
            comment_container.show();
        }
        else {
            comment_container.hide();
        }
    });
    return {'init': init, 'update': update};
}());

