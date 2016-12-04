var GRID_SETTINGS = {
    widget_base_dimensions: [220, 190],
    widget_margins: [10, 10],
    min_cols: 1,
    max_cols: 3,
    shift_widgets_up: false,
    helper: "clone",
    resize: {
        enabled: true,
        min_size: [1, 1],
        max_size: [3, 1],
        stop: saveLayout
    },
    draggable: {
        stop: saveLayout
    }
};

var GRID_SETTINGS_MOBILE = {
    widget_base_dimensions: [100, 100],
    widget_margins: [5, 5],
    max_cols: 3,
    max_size_x: 1,
    max_size_y: 1,
    collision: {
        wait_for_mouseup: false
    },
    resize: {
        enabled: false
    }
};

function getTemplateById(id){
    for(var i = 0; i < controls.length; i++){
        if(controls[i].id == id){
            return templates[i];
        }
    }

    return null;
}

function saveLayout(e, ui, $widget){
    layout.widgets = gridster.serialize();
    postWithJson("/hc/layout", layout, function(response){
        
    });
}

GRID_SETTINGS.serialize_params = function(widget, wgd){
    return { control_id: parseInt(widget.attr("id")), col: wgd.col, row: wgd.row, size_x: wgd.size_x, size_y: wgd.size_y }
};

function loadWidgets(){
    if(layout.widgets.length > 0){
        $.each(layout.widgets, function() {
            var template = getTemplateById(this["control_id"]);
            gridster.add_widget(template, this["size_x"], this["size_y"], this["col"], this["row"]);
        });
    }else{
        console.log("Failed to load widgets, empty list.");
    }
}

function bindEvents(){
    $("#toggleDragButton").click(function(){
        var button = $("#toggleDragButton");
        if(button.hasClass("btn-success")){
            button.removeClass("btn-success").addClass("btn-danger");
            button.html("Dragging Disabled");
            gridster.disable();
        }else{
            button.removeClass("btn-danger").addClass("btn-success");
            button.html("Dragging Enabled");
            gridster.enable();
        }
    });

    $(".addWidgetButton").click(function(){
        var controlId = $(this).attr("id");
        var template = getTemplateById(controlId);

        if(template != null){
            gridster.add_widget(template, 1, 1);
            saveLayout();
        }
    });

    /*var colorPickers = document.getElementsByClassName("colorPicker");
    var i;
    for(i = 0; i < colorPickers.length; i++){
        var colorPicker = $(colorPickers[i]);
        colorPicker.tinycolorpicker();
        colorPicker.bind("change", function(){
            var input = $(this).find("input");
            $("#colorPreview").css("background-color", input.attr("value"));
            $("#colorPreview").show();
            var d = new Date();
            lastPickerChange = d.getTime();
        });
        colorPicker.data("plugin_tinycolorpicker").setColor("#FF45CC");
    }*/

    /*$('.value-slider').slider({
      formatter: function(value) {
        return 'Current value: ' + value;
      }
    });*/

    $('.slider-selection').css('background', '#74C474');
    $('.slider-track-high').css('background', '#BBBBBB');

    /*$(document).on("click", ".widgetCloseButton", function(event){
        var widget = $(this).closest("li");
        gridster.remove_widget(widget);
        event.stopPropagation(); // stops the .widgetButton from receiving a click too
    });*/

    // Load input elements
    $(".control-tb").bootstrapSwitch();
    
    var colorPickers = document.getElementsByClassName("colorPicker");
    var i;
    for(i = 0; i < colorPickers.length; i++){
        var colorPicker = $(colorPickers[i]);
        colorPicker.tinycolorpicker();
        colorPicker.bind("change", function(){
            var input = $(this).find("input");
            $("#colorPreview").css("background-color", input.attr("value"));
            $("#colorPreview").show();
            var d = new Date();
            lastPickerChange = d.getTime();
        });
        colorPicker.data("plugin_tinycolorpicker").setColor("#FF45CC");
    }

    // Bind input element events
    $(".control-sb").on("click", function(evt){
      data = {"control_id": evt.target.id, "state": "pressed?"};
      postWithJson("/hc/control", data, function(response){
        window.alert("Successfully saved state: " + response["state"]);
      });
    });

    $(".control-rv").on("change", function(evt){
      data = {"control_id": evt.target.id, "state": "pressed?"};
      postWithJson("/hc/control", data, function(response){
        window.alert("Successfully saved state: " + response["state"]);
      });
    });

    $(".control-tb").on("click", function(evt){
      var state = $(evt.target).bootstrapSwitch("state");
      data = {"control_id": evt.target.id, "state": state};
      postWithJson("/hc/control", data, function(response){
        window.alert("Successfully saved state: " + response["state"]);
      });
    });
}

$(document).ready(function(){
    if(window.mobile){
        $.extend(GRID_SETTINGS, GRID_SETTINGS_MOBILE);
        console.log("Extended GRID_SETTINGS:");
        console.log(GRID_SETTINGS);
    }
    window.gridster = $(".gridster ul").gridster(GRID_SETTINGS).data("gridster");

    bindEvents();

    loadWidgets();
});

