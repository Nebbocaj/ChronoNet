$(".vote_button").click(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    // make POST ajax call
    postID = $(this).attr('postID')
    vote = $(this).attr('vote')
    $.ajax({
        type: 'POST',
        url: "{% url 'make_vote' %}",
        data: {'post_id': postID,'vote':vote,'csrfmiddlewaretoken': '{{ csrf_token }}'},
        success: function (response) {
            selector = document.getElementById("views_left_post" + postID)
            $(selector).text(response.views_left)

            like_button = $('[vote="like"][postID=' + postID + ']');
            dislike_button = $('[vote="dislike"][postID=' + postID + ']');
            like_button.removeClass("active")
            dislike_button.removeClass("active")
            if (response.vote_state == "like") {
                like_button.addClass("active")
            } else if (response.vote_state == "dislike") {
                dislike_button.addClass("active")
            }
        },
        error: function (response) {
            alert(response["responseJSON"]["error"]);
        }
    })
})