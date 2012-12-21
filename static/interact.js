window.jQuery(function($) {
    $("#submit").attr("disabled", "disabled");
    $("#file1")
        .hide()
        .after($("<button>")
            .addClass('btn')
            .text("Pick a File")
            .click(function(e) { 
                e.preventDefault();
                $("#file1").click();
            })
        );
    var step = 1;
    function order(id1, id2) {
        var lesser = $("#"+id1);
        var greater = $("#"+id2);
        var v1 = lesser.val();
        var v2 = greater.val();
        lesser.val(Math.min(v1, v2));
        greater.val(Math.max(v1, v2));
    }
    function highlight(t) {
        var el = $(".highlight");
        x1 = Number($("#x1").val()) + t.offsetLeft;
        x2 = Number($("#x2").val()) + t.offsetLeft;
        y1 = Number($("#y1").val()) + t.offsetTop;
        y2 = Number($("#y2").val()) + t.offsetTop;
        el
            .css('left', Math.min(x1,x2) + "px")
            .css('top', Math.min(y1,y2) + "px")
            .css('width', Math.abs(x2-x1) + "px")
            .css('height', Math.abs(y2-y1) + "px");

    }
    function clicked(e) {
        var x = e.offsetX;
        var y = e.offsetY;
        $("#x"+step).val(x);
        $("#y"+step).val(y);

        if ( step == 1) {
            $("#submit").attr("disabled", "disabled");
            $("#editor .highlight").remove();
            $("#editor").append( $("<div class='highlight'>"));
            highlight(x+this.offsetLeft, y+this.offsetTop,
                        x+this.offsetLeft+1, y+this.offsetTop+1);
            step = 2;
        }
        else if ( step == 2) {
            order("x1", "x2");
            order("y1", "y2");
            highlight(this);
            $("#submit").removeAttr("disabled");
            
            step = 1;
        }
    }
    function moved(e) {
        if(step != 2) return;
        var x = e.offsetX;
        var y = e.offsetY;
        $("#x2").val(x);
        $("#y2").val(y);
        highlight(this);
    }
    function editor() {
        $("#editor").empty();
        step = 1;
        $("#submit").attr('disabled', 'disabled');

        var files = $("#file1")[0].files;
        if (!files) return;
        var file = files[0];
        if (!file) return;
        var reader = new FileReader;
        reader.onload = function (e) {
            if (!e) return;
            $("#editor").append(
                $("<img id='bldImg'>")
                    .attr("src", e.target.result)
                    .click(clicked)
                    .mousemove(moved)
            );
            $("#editor").css('width', $("#bldImg").width() + 20);
        };
        reader.readAsDataURL(file);
    }
    $("#file1").change(editor);
    editor();
});

