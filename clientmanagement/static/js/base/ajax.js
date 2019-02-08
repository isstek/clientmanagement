function sendPostAjax(link, data, success, failure, async = true) {
    data['csrfmiddlewaretoken'] = my_crsf_token;
    $.ajax({
        type: "POST",
        url: link,
        data: data,
        success: success,
        failure: failure,
        async: async
    })
}