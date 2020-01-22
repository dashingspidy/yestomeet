$(document).ready(function(){
    $('#description').bind("cut copy paste", function(e) {
        e.preventDefault();
    });

    $(document).on('click', '.notification > button.delete', function() {
        $(this).parent().addClass('is-hidden');
        return false;
    });

    $('input#photo').bind('change', function() {
        var file_size = this.files[0].size;
        var $el = $('input#photo');
        
        if (file_size > 5242880) {
            $('#er').show();
            $el.wrap('<form>').closest('form').get(0).reset();
            $el.unwrap();
        };
    });

    $(".em").emojioneArea();
});

document.addEventListener('DOMContentLoaded', function () {
                var $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
                if ($navbarBurgers.length > 0) {

                    $navbarBurgers.forEach(function ($el) {
                      $el.addEventListener('click', function () {
                        var target = $el.dataset.target;
                        var $target = document.getElementById(target);
                        $el.classList.toggle('is-active');
                        $target.classList.toggle('is-active');
                      });
                    });
                }
            });