window.onload = function() {
    $.ajax({
        url:'/reload',
        success: function(response) {
            console.log("done");
        },
        error: function(response) {
            console.log('error in onload');
            console.log(response);
        }
    });
}

$(function() {
    $('#detect').click(function() {
        window.onload();
        var form_data = new FormData();
        var ins = document.getElementById('upload').files.length;

        for(var x=0; x< ins; x++) {
            form_data.append(x, document.getElementById('upload').files[x]);
            console.log(document.getElementById('upload').files[x]);
        }

        $.ajax({
            url: '/file',
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            type: "POST",
            data: form_data,
            success: function(response) {
                document.getElementById("next").disabled=false;
                console.log(response['filename']);
                $('#original').attr('src', '/static/uploads/'+response['filename']);
                document.getElementById('count').innerHTML = response['pred'];
            },
            error: function(response) {
                console.log('error in  detect');
                console.log(response);
            }
        });
    });

}),

$(function() {

    $('#next').click(function() {
        console.log('in next');
        $.ajax({
            url:'/next',
            success: function(response) {
                if(!response['response']) {
                    document.getElementById("next").disabled=true;
                    console.log('rigthmost');  
                }
                document.getElementById("previous").disabled=false;
                console.log(response['pred']);
                $('#original').attr('src', '/static/uploads/'+response['filename']);
                document.getElementById('count').innerHTML = response['pred'];
            },
            error: function(response) {
                console.log('error in next');
                console.log(response);
            }
        });
    });
}),

$(function() {
    $('#previous').click(function() {
        console.log('in previous');
        $.ajax({
            url:'/previous',
            success: function(response) {
                if(!response['response']) {
                    document.getElementById("previous").disabled=true;
                    console.log('leftmost');  
                }
                document.getElementById("next").disabled=false;
                console.log(response['filename']);
                $('#original').attr('src', '/static/uploads/'+response['filename']);
                document.getElementById('count').innerHTML = response['pred'];
            },
            error: function(response) {
                console.log('error in previous');
                console.log(response);
            }
        });
    });
});