$('#load-more').on('click', function(){
    let lastPostId = $('.last-post').attr('data-postid');
    let data = {
        lastPostId:lastPostId
    }

    $.ajax({
        method: "GET",
        dataType: "json",
        data: data,
        url: '{% url "load-more-post" %}',
        success: function(data){
            console.log(data)
        }
    })
})