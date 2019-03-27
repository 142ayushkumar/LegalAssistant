$(function() {
    $(window).scroll(function() {
        var sticky = $('.header'),
            scroll = $(window).scrollTop();
        var sticky2 = $('.sidebar');

        if (scroll >= 100) {
            sticky.addClass('hide-me');
            sticky2.addClass('move-me')
        }
        else {
            sticky.removeClass('hide-me');
            sticky2.removeClass('move-me');
        }
    });
});