/*

$(document).bind("ajaxSend", function () {
    $("body").showLoading();
}).bind("ajaxComplete", function () {
    $("body").hideLoading();
});

*/


function timeout_reload(time_second){
    setTimeout(function(){
        location.reload()
    }, time_second)
}

function GMTToDateString(time){
    let date = new Date(time);
    let Str=date.getFullYear() + '-' +
    (date.getMonth() + 1) + '-' +
    date.getDate()
    return Str
}

function GMTToMonth(time){
    let date = new Date(time);
    let Str=date.getFullYear() + '-' +
    (date.getMonth() + 1)
    return Str
}


function GMTTotimeString(time){
    let date = new Date(time);
    let Str=date.getFullYear() + '-' +
    (date.getMonth() + 1) + '-' +
    date.getDate() + ' ' +
    date.getHours() + ':' +
    date.getMinutes() + ':' +
    date.getSeconds()
    return Str
}

function getDateDistant(time_1){
    let date_1 = new Date(time_1).getTime();
    let now_1 = new Date().getTime();

    let timeDiff = parseInt(now_1) - parseInt(date_1);
    hour_diff =  Math.trunc(timeDiff/1000/60/60);
    if (hour_diff < 0){
        diff_string = Math.abs(hour_diff) + "小时后";
    }else{
        diff_string = Math.abs(hour_diff) + "小时前";
    }
    return diff_string;
}

$(document).ready(function(){
    $(document).on('click', '#closeLayerChildBtn', function(){
        var index = parent.layer.getFrameIndex(window.name);
        parent.layer.close(index);
    })

     $(document).on('click', '#addButton', function(){
        var index = parent.layer.getFrameIndex(window.name);
        var url = $(this).data('url');
        var board_title = $(this).data('title');
        var add_index = layer.open({
          type: 2,
          title:board_title,
         // skin: 'layui-layer-rim', //加上边框
         // area: ['90%', '90%'], //宽高
          content: url
        });
        layer.full(add_index)
    })
})

/*
toastr.options = {
  "closeButton": true,
  "debug": false,
  "progressBar": true,
  "positionClass": "toast-top-right",
  "onclick": null,
  "showDuration": "400",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}
*/

function openTabWidth(l) {
    var k = 0;
    $(l).each(function() {
        k += $(this).outerWidth(true)
    });
    return k
}


function openTabDeploy(n) {
    var o = openTabWidth($(n).prevAll()),
        q = openTabWidth($(n).nextAll());
    var l = openTabWidth($(".content-tabs", parent.document).children().not(".J_menuTabs"));
    var k = $(".content-tabs", parent.document).outerWidth(true) - l;
    var p = 0;
    if ($(".page-tabs-content", parent.document).outerWidth() < k) {
        p = 0
    } else {
        if (q <= (k - $(n).outerWidth(true) - $(n).next().outerWidth(true))) {
            if ((k - $(n).next().outerWidth(true)) > q) {
                p = o;
                var m = n;
                while ((p - $(m).outerWidth()) > ($(".page-tabs-content", parent.document).outerWidth() - k)) {
                    p -= $(m).prev().outerWidth();
                    m = $(m).prev()
                }
            }
        } else {
            if (o > (k - $(n).outerWidth(true) - $(n).prev().outerWidth(true))) {
                p = o - $(n).prev().outerWidth(true)
            }
        }
    }
    $(".page-tabs-content", parent.document).animate({
        marginLeft: 0 - p + "px"
    }, "fast")
}



function openTab() {
     var o = $(this).data("action"),
     m = $(this).data("index"),
     l = $(this).data("title") || $.trim($(this).text()),
     k = true;
     if (o == undefined || $.trim(o).length == 0) {
     return false
     }

     if (m == undefined || $.trim(m).length == 0) {
     console.log(m)
         console.log('m undefined...')
     return false
     }

     $(".J_menuTab", parent.document).each(function() {
         if ($(this).data("id") == o) {
             if (!$(this).hasClass("active")) {
                 $(this).addClass("active").siblings(".J_menuTab").removeClass("active");
                 openTabDeploy(this);
                 $(".J_mainContent .J_iframe", parent.document).each(function() {
                     if ($(this).data("id") == o) {
                         $(this).show().siblings(".J_iframe").hide();
                         return false
                     }
                 })
             }
             k = false;
             return false
         }
     });

     if (k) {
        var p = '<a href="javascript:;" class="active J_menuTab" data-id="' + o + '">' + l + ' <i class="fa fa-times-circle"></i></a>';
        $(".J_menuTab", parent.document).removeClass("active");
         var n = '<iframe class="J_iframe" name="iframe' + m + '" width="100%" height="100%" src="' + o + '" frameborder="0" data-id="' + o + '" seamless></iframe>';
         $(".J_mainContent", parent.document).find("iframe.J_iframe").hide().parents(".J_mainContent").append(n);
         $($(".J_menuTabs .page-tabs-content", parent.document)).append(p);
         openTabDeploy($(".J_menuTab.active", parent.document))
     }
     return false
 }
