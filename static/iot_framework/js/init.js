/**
 * Created by hanter on 2016. 6. 11..
 */

$(document).ready(function() {
    highlightCurrentMenu();

    $('.onloading').click(function() {
        //$.LoadingOverlay('show');
    });

});

function openModal(msg, title, action) {
    if (title==undefined || title==null || title=='') {
        $('#alertModalTitle').text('Alert');
    }
    if (msg==undefined || msg==null || msg=='') {
        msg = 'Alert.';
    }
    $('#alertModalTitle').text(title);
    //$('#alertModal .modal-body').text(msg);
    $('#alertModal .modal-body').empty();
    $('#alertModal .modal-body').html(msg);

    if (action != undefined && action != null && jQuery.isFunction(action)) {
        $('#alertModal .modal-alert-close').off('click');
        $('#alertModal .modal-alert-close').unbind('click');
        $('#alertModal .modal-alert-close').click(action);
        $('#alertModal').modal({backdrop: 'static', keyboard: false});
    } else {
        $('#alertModal .modal-alert-close').off('click');
        $('#alertModal .modal-alert-close').unbind('click');
        $('#alertModal').modal();
    }

}

function checkTextOnlyAlphabetsAndNumber(text) {
    var regExp = /^[a-zA-Z0-9_ ,-]+$/;
    return regExp.test(text);
}

function makeNoticePopover(element, msg) {
    element.popover({
        title: "Notice",
        content: msg,
        placement: "bottom",
        trigger: "manual"
    }).data('bs.popover')
        .tip()
        .addClass('popover-info');
    element.popover("show");
    setTimeout(function () {
        element.popover('destroy');
    }, 4000);
}

function highlightCurrentMenu() {
    var paths = jQuery(location).attr('pathname').split('/');

    if(paths.length >= 2) {
        var topMenuPath = paths[1];

        switch(topMenuPath) {
            case 'user':
                $('#nav_user').addClass('selected');
                break;
            case 'device_model':
                $('#nav_device_model').addClass('selected');
                break;
            case 'device_item':
                $('#nav_device_item').addClass('selected');
                break;
            case 'connection':
                $('#nav_connection').addClass('selected');
                break;
            case 'context':
                $('#nav_context').addClass('selected');
                break;
            case 'statistics':
                $('#nav_statistics').addClass('selected');
                break;
        }
    }
}

//Timestamp -> Datetime Format
String.prototype.string = function(len){var s = '', i = 0; while (i++ < len) { s += this; } return s;};
String.prototype.zf = function(len){return "0".string(len - this.length) + this;};
Number.prototype.zf = function(len){return this.toString().zf(len);};
Date.prototype.format = function(f) {
    if (!this.valueOf()) return " ";

    var d = this;

    return f.replace(/(yyyy|yy|MM|dd|E|hh|mm|ss|ccc|a\/p)/gi, function($1) {
        switch ($1) {
            case "yyyy": return d.getFullYear();
            case "yy": return (d.getFullYear() % 1000).zf(2);
            case "MM": return (d.getMonth() + 1).zf(2);
            case "dd": return d.getDate().zf(2);
            case "HH": return d.getHours().zf(2);
            case "hh": return ((h = d.getHours() % 12) ? h : 12).zf(2);
            case "mm": return d.getMinutes().zf(2);
            case "ss": return d.getSeconds().zf(2);
            case "ccc": return d.getMilliseconds().zf(3);
            default: return $1;
        }
    });
};