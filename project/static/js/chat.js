var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        socket.emit('joined', {});
    });
    
    $('#send_msg').click(function(e) {
        text = $('#m_text').val();
        var el = $("#m_text").emojioneArea();
        el[0].emojioneArea.setText(''); 
        socket.emit('text', {msg: text});
    });

    socket.on('message', function(data) {
        $('#m_list').append("<li class='subtitle'>" + data.msg + "</li>" );
        // $('#m_list').animate({scrollTop: $('#m_list').prop("scrollHeight")}, 300);
    });

    $('#clear_msg').click(function(e) {
        var el = $("#m_text").emojioneArea();
        el[0].emojioneArea.setText('');
    });

    socket.on('disconnect', function() {
        socket.emit('disconnected', {});
    });
});
