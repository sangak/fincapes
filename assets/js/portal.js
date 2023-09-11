;(function($) {
    'use strict';
    $(function() {
        let body = $('body');

        feather.replace();

        if ($('.sidebar .sidebar-body').length) {
            const sidebarBodyScroll = new PerfectScrollbar('.sidebar-body');
        }

        $('.sidebar-toggler').on('click', function(e) {
            e.preventDefault();
            $('.sidebar-header .sidebar-toggler').toggleClass('active not-active');
            if (window.matchMedia('(min-width: 992px)').matches) {
                e.preventDefault();
                body.toggleClass('sidebar-folded');
            } else if (window.matchMedia('(max-width: 991px)').matches) {
                e.preventDefault();
                body.toggleClass('sidebar-open');
            }
        });

        $('.settings-sidebar-toggler').on('click', function(e) {
            $('body').toggleClass('settings-open');
        });

        $("input:radio[name=sidebarThemeSettings]").click(function() {
            $('body').removeClass('sidebar-light sidebar-dark').addClass($(this).val());
        });

        $(".sidebar .sidebar-body").hover(
        function () {
            if (body.hasClass('sidebar-folded')){
                body.addClass("open-sidebar-folded");
            }
        },
        function () {
            if (body.hasClass('sidebar-folded')){
                body.removeClass("open-sidebar-folded");
            }
        });

        $(document).on('click touchstart', function(e){
            e.stopPropagation();

            if (!$(e.target).closest('.sidebar-toggler').length) {
                var sidebar = $(e.target).closest('.sidebar').length,
                    sidebarBody = $(e.target).closest('.sidebar-body').length;
                if (!sidebar && !sidebarBody) {
                    if ($('body').hasClass('sidebar-open')) {
                        $('body').removeClass('sidebar-open');
                    }
                }
            }
        });

        $('[data-toggle="horizontal-menu-toggle"]').on("click", function() {
            $(".horizontal-menu .bottom-navbar").toggleClass("header-toggled");
        });

        var navItemClicked = $('.horizontal-menu .page-navigation >.nav-item');
        navItemClicked.on("click", function(event) {
            if (window.matchMedia('(max-width: 991px)').matches) {
                if (!($(this).hasClass('show-submenu'))) {
                    navItemClicked.removeClass('show-submenu');
                }
                $(this).toggleClass('show-submenu');
            }
        });



        $(window).scroll(function() {
            if(window.matchMedia('(min-width: 992px)').matches) {
                var header = $('.horizontal-menu');
                if ($(window).scrollTop() >= 60) {
                    $(header).addClass('fixed-on-scroll');
                } else {
                    $(header).removeClass('fixed-on-scroll');
                }
            }
        });

        $('.sidebar .sidebar-body').hover(function () {
            $('body').addClass('overflow-hidden');
        }, function () {
            $('body').removeClass('overflow-hidden');
        });
    });
})(jQuery);