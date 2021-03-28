$(document).ready(function(){

    $("[data-role=follow_button]").submit(function(e){
        e.preventDefault(); 
        var form = $(this);
        let url = form.attr("action");
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            dataType: "json",
            success: function(response) {
                var btn = form.find("input[type='submit']");
                if (response.followed) {
                    btn.css("background-color", "#c4c4c4");
                    btn.val("UNFOLLOW");
                } else {
                    btn.css("background-color", "#f7c10f");
                    btn.val("FOLLOW");
                }
            }
        })
    })

    $("[data-role=like_ann]").submit(function(e){
        e.preventDefault(); 
        var form = $(this);
        let url = form.attr("action");
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            dataType: "json",
            success: function(response) {
                var btn = form.find("button[type='submit']");
                var btn_text = form.find("span[id='like_state']")
                if (response.liked) {
                    btn.addClass('liked_ajax').removeClass('like_ajax');
                    btn_text.text(" LIKED");
                    
                } else {
                    btn.addClass('like_ajax').removeClass('liked_ajax');
                    btn_text.text(" LIKE");
                }
            }
        })
    })

    $("[data-role=rsvp_show]").submit(function(e){
        e.preventDefault(); 
        var form = $(this);
        let url = form.attr("action");
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            dataType: "json",
            success: function(response) {
                var btn = form.find("button[type='submit']");
                var btn_text = form.find("span[id='rsvp_state']")
                if (response.attending) {
                    btn.addClass('going').removeClass('rsvp');
                    btn_text.text(" I'M GOING");
                    
                } else {
                    btn.addClass('rsvp').removeClass('going');
                    btn_text.text(" RSVP");
                }
            }
        })
    })

    $("[data-role=new_date]").submit(function(e){
        e.preventDefault(); 
        var tour_form = $(this);
        let url = tour_form.attr("action");
        $.ajax({
            type: "POST",
            url: url,
            data: tour_form.serialize(),
            dataType: "json",
            success: function(){
                $('.tour_table tbody').load("/artist/show_new_show/");
                $('.shows_count').load("/artist/show_new_show_count/");
                $("#tour_form")[0].reset();
                $("#tour_show").click();
            }
        })
    })

    $("[data-role=new_ann]").submit(function(e){
        e.preventDefault(); 
        var ann_form = $(this);
        let url = ann_form.attr("action");
        $.ajax({
            type: "POST",
            url: url,
            data: ann_form.serialize(),
            dataType: "json",
            success: function(){
                $('.ann_table tbody').load("/artist/show_new_ann/");
            }
        })
    })

    $(".delete_ann").click(function(e) {
        e.preventDefault(); 
        var ann_id = $(this).attr('data-role');
        let url = $(this).attr("href");
        $.ajax({
            url: url,
            data: { ann_id:ann_id },
            success: function(){
                $('#ann_'+ann_id).fadeOut(500, "swing")
            }
        });
    });

    $(".delete_tour").click(function(e) {
        e.preventDefault(); 
        var tour_id = $(this).attr('data-role');
        let url = $(this).attr("href");
        $.ajax({
            url: url,
            data: { tour_id:tour_id },
            success: function(){
                $('#tour_'+tour_id).fadeOut(500, "swing");
                $('.shows_count').load("/artist/show_new_show_count/");
            }
        });
    });

    $(".fan_cancel").click(function(e) {
        e.preventDefault(); 
        var tour_id = $(this).attr('data-role');
        let url = $(this).attr("href");
        $.ajax({
            url: url,
            data: { tour_id:tour_id },
            success: function(){
                $('#fan_tour_'+tour_id).fadeOut(500, "swing");
                $('.shows_count').load("/fan/show_new_show_count_fan/");
                $('.rewards').load("/fan/rewards/");
            }
        });
    });

    $("#tour_show").click(function () {
            if ($("#tour_display").hasClass("tour_visible")) {
                $("#tour_display").removeClass("tour_visible");
                
            } else {
                $("#tour_display").addClass("tour_visible");
            }
    });

});