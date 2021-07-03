/*  ---------------------------------------------------
    Template Name: Foodeiblog
    Description:  Foodeiblog Blog HTML Template
    Author: Colorlib
    Author URI: https://colorlib.com
    Version: 1.0
    Created: Colorlib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Humberger Menu
    $(".humberger__open").on('click', function () {
        $(".humberger__menu__wrapper").addClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").addClass("active");
    });

    $(".humberger__menu__overlay").on('click', function () {
        $(".humberger__menu__wrapper").removeClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").removeClass("active");
    });

    //Search Switch
    $('.search-switch').on('click',function() {
        $('.search-model').fadeIn(400);
    });

    $('.search-close-switch').on('click',function() {
        $('.search-model').fadeOut(400,function() {
            $('#search-input').val('');
        });
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
        Carousel Slider
    --------------------*/
    var hero_s = $(".hero__slider");
    hero_s.owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: false,
        nav: true,
        navText: ["<span class='arrow_carrot-left'><span/>", "<span class='arrow_carrot-right'><span/>"],
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

})(jQuery);

$('#load-more').on('click', function(){
    let lastPostId = $('.last-post').attr('data-postid')
    let data = {
        lastPostId:lastPostId
    }

    $('.post').removeClass('last-post')
    $('.post').removeAttr('data-postid')

    $.ajax({
        method: "GET",
        dataType: "json",
        data: data,
        success: function(data){
            let result = data['data']
            if(!result){
                $('.load-more').css('display', 'none')
            }
            else{
                $.each(result, function(key, obj){
                    let post =  '<div class="categories__post__item">'+
                                    '<div class="categories__post__item__pic small__item set-bg" style="background-image: url('+ obj['image_url'] +');">'+
                                        '<div class="post__meta">'+
                                            '<h4>'+obj['create_at_day']+'</h4>'+
                                            '<span>'+obj['create_at_month']+'</span>'+
                                        '</div>'+
                                    '</div>'+
                                    '<div class="categories__post__item__text">'+
                                    '<span class="post__label">'+obj['category']+
                                    '</span>'+
                                        '<h3><a href="'+obj['url']+'">'+obj['title']+'</a></h3>'+
                                        '<ul class="post__widget">'+
                                            '<li>by <span>'+obj['author']+'</span></li>'+
                                            '<li>'+obj['count_comment']+' Comment</li>'+
                                        '</ul>'+
                                        '<p>'+obj['mini_text']+'</p>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'
                    if(obj['last_post']){
                        $('.all_posts').append(
                            '<div class="col-lg-6 col-md-6 col-sm-6 post last-post" data-postid="'+obj['id']+'">'+ post
                            )
                    }
                    else{
                        $('.all_posts').append(
                            '<div class="col-lg-6 col-md-6 col-sm-6 post" data-postid="'+obj['id']+'">'+ post
                            )
                    }

                   if(obj['last_id'] - lastPostId <= 3 ){
                        $('.load-more').css('display', 'none')
                    }
                })
            }
        }
    })
})