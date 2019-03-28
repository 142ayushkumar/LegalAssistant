$(function () {
    if ($('[type="date"]').prop('type') != 'date') {
        $('[type="date"]').datepicker();
    }

    $('.category-select').select2();
    $('.category-select').select2({width: "100%", placeholder: "Categories"});

    $('.judge-select').select2();
    $('.judge-select').select2({width: "100%", placeholder: "Judges"});

    $('.act-select').select2();
    $('.act-select').select2({width: "100%", placeholder: "Acts"});

    $(".search-2 input").click(function() {
        if($(".maxi-header-2").is(":hidden")) {
            $(".maxi-header-2").fadeIn().css("filter", "drop-shadow(16px 16px 10px rgba(0,0,0,1));");


        }

    });
    $(".main,.close, .footer-2").click(function() {
        if($(".maxi-header-2").is(":hidden") == false) {
            $(".maxi-header-2").fadeOut();

        }
    });

});