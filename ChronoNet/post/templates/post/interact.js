function formatTime(timeLeft) {
    if (timeLeft < 0) {
        timeLeft = 0
    }
    timeLeft /= 1000;
    var days = Math.floor(timeLeft / 86400);
    var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
    var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600)) / 60);
    var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

    stringTimeLeft = days + " days, " + hours + " hours, " + minutes + " minutes, " + seconds + " seconds";
    return stringTimeLeft;
}

// MUST MATCH THE REWARD FUNCTION IN THE BACKEND
function getVoteReward(timeAlive) {
    //https://www.desmos.com/calculator/auygmpre7k

    var maxReward = 30; // minutes
    var minReward = 1; // minutes
    var time_decay = 5;

    // reward :: days -> minutes

    timeAlive /= 1000;
    var days = timeAlive / 86400;

    reward = minReward + (maxReward - minReward) / (1.0 + (days ** 2) / time_decay);
    return reward;
}

var ajaxTimer = 1;
var ajaxTimerMax = 10; // seconds

function onceASecond() {
    // get all the IDs of elements with expiration dates
    var postIDs = $(".expiration_display").map(function () {
        return $(this).attr("postID");
    }).get();

    // only make ajax call every couple of seconds
    if (ajaxTimer <= 0) {
        updateTimes(postIDs);
        ajaxTimer = ajaxTimerMax;
    } else {
        ajaxTimer--;
    }

    for (let i = 0; i < postIDs.length; i++) {
        displayTime(postIDs[i]);
    }
}

function displayTime(postID) {
    var time_display = $('.expiration_display[postID=' + postID + ']');

    var expires = Date.parse(time_display.attr("expires"));
    var now = new Date();
    var timeLeft = expires - now;
    if (timeLeft < 0) { // delete the post
        post_container = $('.post_container[postID=' + postID + ']');
        post_container.fadeOut(1000);
        return;
    }
    var timeLeftFormatted = formatTime(timeLeft);
    time_display.html(timeLeftFormatted);

    // TODO : get reward based on time alive
    var created = Date.parse(time_display.attr("created"));
    var now = new Date();
    var reward = getVoteReward(now - created);

    like_button = $('.vote_button[vote="like"][postID=' + postID + ']');
    dislike_button = $('.vote_button[vote="dislike"][postID=' + postID + ']');

    if (like_button.hasClass("active")) {
        like_button.tooltip().attr('data-original-title', "- " + reward.toFixed(0) + " minutes");
        dislike_button.tooltip().attr('data-original-title', "- " + (2*reward).toFixed(0) + " minutes");
    } else {
        if (dislike_button.hasClass("active")) {
            like_button.tooltip().attr('data-original-title', "+ " + (2*reward).toFixed(0) + " minutes");
            dislike_button.tooltip().attr('data-original-title', "+ " + reward.toFixed(0) + " minutes");
        } else {
            like_button.tooltip().attr('data-original-title', "+ " + reward.toFixed(0) + " minutes");
            dislike_button.tooltip().attr('data-original-title', "- " + reward.toFixed(0) + " minutes");
        }
    }
}

function updateTimes(postIDs) {
    $.ajax({
        type: 'POST',
        url: "{% url 'get_posts_time' %}",
        data: { 'post_ids': postIDs, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
        success: function (response) {
            // response format:
            // {
            //     "postIDs": [int],
            //     "expirations": [string],
            // }
            for (let i = 0; i < response.postIDs.length; i++) {
                updateTime(response.postIDs[i], response.expirations[i]);
            }
        },
        error: function (response) {
            console.log(response);
        }
    });
}

// updates time value for each post (does not update the display)
function updateTime(postID, expires) {
    time_display = $('.expiration_display[postID=' + postID + ']');
    time_display.attr("expires", expires);
}

window.onload = onceASecond()
setInterval(onceASecond, 1000);

$(".vote_button").click(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    // make POST ajax call
    postID = $(this).attr('postID');
    vote = $(this).attr('vote');
    $.ajax({
        type: 'POST',
        url: "{% url 'make_vote' %}",
        data: { 'post_id': postID, 'vote': vote, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
        success: function (response) {
            // response format:
            // {
            //     "views_left": int,
            //     "expires": string,
            //     "vote_state": "like" | "dislike" | "none" ,
            //     "post_id": int
            // }

            // update time and display
            updateTime(postID, response.expires);
            displayTime(postID);

            // update display of like button
            like_button = $('[vote="like"][postID=' + postID + ']');
            dislike_button = $('[vote="dislike"][postID=' + postID + ']');
            like_button.removeClass("active");
            dislike_button.removeClass("active");
            if (response.vote_state == "like") {
                like_button.addClass("active")
            } else if (response.vote_state == "dislike") {
                dislike_button.addClass("active");
            }

            // update tooltip
            like_button.tooltip('hide');
            dislike_button.tooltip('hide');
        },
        error: function (response) {
            alert(response["responseJSON"]["error"]);
        }
    })
})

$(".delete_post_button").click(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    // make POST ajax call
    postID = $(this).attr('postID');
    $.ajax({
        type: 'POST',
        url: "{% url 'delete_post' %}",
        data: { 'post_id': postID, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
        success: function (response) {
            // get post container
            post_container = $('.post_container[postID=' + postID + ']');

            // delete post
            post_container.remove();
        },
        error: function (response) {
            console.log(response);
        }
    })
})

// this enables the hovering
$(function () {
    $('[data-toggle="tooltip"]').tooltip({
        trigger : 'hover'
    });
})