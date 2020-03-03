;(function ($) {
  'use strict'

  // Sticky menu
  var $window = $(window)
  $window.on('scroll', function () {
    var scroll = $window.scrollTop()
    if (scroll < 300) {
      $('.sticky').removeClass('is-sticky')
    } else {
      $('.sticky').addClass('is-sticky')
    }
  })


  // Background Image JS start
  var bgSelector = $('.bg-img')
  bgSelector.each(function (index, elem) {
    var element = $(elem)

    var bgSource = element.data('bg')
    element.css('background-image', 'url(' + bgSource + ')')
  })

  // waypoint active js
  function teamMember () {
    if ($window.width() < 575) {
      $('.team-member').waypoint(
        function () {
          $(this.element).toggleClass('team-open')
        },
        {
          offset: '75%'
        }
      )
    }
  }
  teamMember()

  // Scroll to top active js
  $(window).on('scroll', function () {
    if ($(this).scrollTop() > 600) {
      $('.scroll-top').removeClass('not-visible')
    } else {
      $('.scroll-top').addClass('not-visible')
    }
  })
  $('.scroll-top').on('click', function (event) {
    $('html,body').animate(
      {
        scrollTop: 0
      },
      1000
    )
  })

  $window.resize(function () {
    teamMember()
  })

  // wow js active
  new WOW().init()
})(jQuery)
