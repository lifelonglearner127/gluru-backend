(function($) {
  $(document).ready(function() {
    $(".activate_ticket" ).on('click', function() {
      var id = $(this).attr("data-id");
      var action = $(this).attr('data-action')
      var data = {
        "ticket": {
          "is_deleted": action==='Activate'? false : true
        }
      };

      $.ajaxSetup({
        url: "/api/tickets/" + id+ "/",
        type: "PUT",
        contentType: "application/json; charset=utf-8",
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
      });
      $.ajax({
        data: JSON.stringify(data),
        success: function(data){
          location.reload();
        }
      });
    });

    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = $.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
    }
  });
})(window.jQuery || django.jQuery);