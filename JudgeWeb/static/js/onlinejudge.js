var OnlineJudge = (function ($) {
    'use strict';

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    return {csrftoken: getCookie('csrftoken')};
}(window.jQuery));

/**
 * Login
 */
OnlineJudge = (function ($, oj) {
    'use strict';

    $('#login_submit').click(function () {
        $('#login_submit').addClass('disabled');
        var submit_button_val = $('#login_submit').val();
        $('#login_submit').val('Waiting...');
        $.post('/user/login/', $('#login_form').serialize(), function (data) {
            var result = data['message'];
            if (result === 'OK') {
                location.reload();
            } else {
                $('#login_form input[name=username]').val('');
                $('#login_form input[name=password]').val('');
                alert(result);
                $('#login_submit').val(submit_button_val).removeClass('disabled');
            }
        });
    });

    return OnlineJudge;

}(window.jQuery, OnlineJudge));

/**
 * Problem
 */
OnlineJudge = (function ($, oj) {
    'use strict';

    function addFavProblem(problemId) {
        var problemRow = $('#problem_list tr[data-problem-id=' + problemId +']');
        problemRow.addClass('collect-pending');
        $.post('/problem/fav/', {'problem': problemId}, function (data) {
            problemRow.removeClass('collect-pending');
            if (data === 'True') {
                problemRow.addClass('collect');
            } else if(data === 'False') {
                problemRow.removeClass('collect');
            } else if(data === 'no_login') {
                alert('Login in first');
                location.reload();
            }
        });
    }

    $('#problem_list .fav').click(function () {
        addFavProblem($(this).parents('tr').data('problem-id'));
    });
    return OnlineJudge;

}(window.jQuery, OnlineJudge));
