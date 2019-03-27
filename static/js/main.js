$(function () {
    if ($('input[type="date"]').prop('type') != 'date') {
        $('input[type="date"]').datepicker();
    }

    $('.category-select').select2();
    $('.category-select').select2({width: "100%", placeholder: "Categories"});

    $('.judge-select').select2();
    $('.judge-select').select2({width: "100%", placeholder: "Judges"});

    $('.act-select').select2();
    $('.act-select').select2({width: "100%", placeholder: "Acts"});


    $(".recent-list ul li").click(function () {
        let c = $(this).attr("category");
        let j = $(this).attr("judge");
        let a = $(this).attr("acts");

        let f = $(this).attr("from");
        let t = $(this).attr("to");


        let x = JSON.parse(c);
        let y = JSON.parse(j);
        let z = JSON.parse(a);


        $(".category-select").val(x).trigger('change');
        $(".judge-select").val(y).trigger('change');
        $(".act-select").val(z).trigger('change');


        $("input[name=from]").val(f);
        $("input[name=to]").val(t);

    });

});