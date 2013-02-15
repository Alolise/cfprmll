(function ($) {
  Drupal.behaviors.rmllTheme = {
    attach: function (context, settings) {
      $('#wrapper div.leftcol div.button a').each(function(i, e) {
        var h = $(this).attr('href');
        var e = $(this).attr('class');
        if (e == 'exter') {
          // void
        } else {
          $(this).parent().click(function() {
            window.location = h;
          });
        }
      });
      $('#librelogos div.scrollableArea img').unbind('click');
      $('#librelogos div.scrollableArea img').click(function() {
        window.open($(this).attr('alt'), '_blank');
      });
      $('#librelogos div.scrollableArea a').contents().unwrap();
      var librelogos = $('#librelogos div.scrollableArea img').get().sort(function(){
        return Math.round(Math.random())-0.5;
      });
      if ($.isArray(librelogos) && librelogos.length > 0)
        $(librelogos).appendTo(librelogos[0].parentNode).show();
      $('#librelogos div.scrollableArea img').each(function(i, e) {
        $(this).show();
      });
      $('#librelogos').smoothDivScroll({
        autoScroll: 'onstart',
        autoScrollDirection: 'endlessloopright',
        autoScrollStep: 1,
        autoScrollInterval: 75,
        visibleHotSpots: ''
      });
    }
  };
}(jQuery));
