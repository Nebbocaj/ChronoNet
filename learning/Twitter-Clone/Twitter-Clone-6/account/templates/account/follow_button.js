$(".follow_button").click(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    // make POST ajax call
    button = $(this)
    profileID = button.attr('profileID')
    $.ajax({
        type: 'POST',
        url: "{% url 'follow' %}",
        data: {'profile_id': profileID,'csrfmiddlewaretoken': '{{ csrf_token }}'},
        success: function (response) {
            // expect response to have 'following' :: bool
            if (response.following) {
                button.html("Unfollow")
            } else {
                button.html("Follow")
            }
        },
        error: function (response) {
            alert(response["responseJSON"]["error"]);
        }
    })
})