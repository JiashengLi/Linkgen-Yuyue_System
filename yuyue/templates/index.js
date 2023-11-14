/*!global gettext, interpolate, ngettext*/
$(document).ready(function(){
    //$('#add_yuyue_div').hide()
   // $('#payment_div').hide()
    //$('#alert_div').hide()
    $('#wenjuan_div').hide()
   // $('#qrcode_div').hide()
           $.post("/yuyue_wx",{url:encodeURIComponent(location.href.split('#')[0])},function(data,status){
              var info = jQuery.parseJSON(data)
    
    $('.del_table').click(function () {
        if(confirm("确定删除该预约？")){
        $.post("/yuyue_detail",{
        opt:"del",
        table_id:$(this).attr("id"),
        },function(data,status){
        if(data=="已删除该预约"){
        alert(data); 
        window.location.reload()
        }
        else{
        alert(data);
        }
        });
        }
    })
    $('.pay_table').click(function () {
      // $(this).after($(this).attr("id"));
        $('#pay_yuyue').attr('pay_bill',$(this).attr("id"));
        $.get("/yuyue_list",{table_id:$(this).attr("id")},function(data,status){
        //           var info = jQuery.parseJSON(data)
        $('#payment_panel').empty();
        $('#payment_panel').append(data);
        $('#main_div').hide()
        $('#yuyue_bt').hide()
        $('#payment_div').show()
        // $('#payment_div')[0].scrollIntoView(true);
        });
    })
    $('.wenjuan_table').click(function () {
        // $(this).after($(this).attr("id"));
        $('#wenjuan_sub').attr('wenjuan_id',$(this).attr("id"));
        $('#main_div').hide()
        $('#yuyue_bt').hide()
        $('#wenjuan_div').show()
        // $('#payment_div')[0].scrollIntoView(true);
    })
    $('.qrcode_table').click(function () {
        $.post("/yuyue_detail",{
        opt:"qrcode",
        table_id:$(this).attr("id"),
        },function(data,status){
        $('#qrcode_img').attr('src',data);
        $('#main_div').hide()
        $('#yuyue_bt').hide()
        $('#qrcode_div').show()
        // $('#payment_div')[0].scrollIntoView(true);
        });
    })
    $('#qrcode_cancel').click(function () {
        window.location.reload()
        // $('#qrcode_img').attr('src','');
        // $('#qrcode_div').hide()
        // $('#main_div').show()
        // $('#yuyue_bt').show()
        // $('#payment_div')[0].scrollIntoView(true);
    })
    $('#wenjuan_sub').click(function () {
        // $(this).after($(this).attr("id"));
        if($("input[name='checked']").is(':checked')) {
            // do something
        $.post("/yuyue_detail",{
        opt:"wenjuan",
        table_id:$(this).attr("wenjuan_id"),
        wenjuan_1:$("input[name='1']:checked").val(),
        wenjuan_2:$("input[name='2']:checked").val(),
        wenjuan_3:$("input[name='3']:checked").val(),
        wenjuan_4:$("input[name='4']:checked").val(),
        wenjuan_5:$("input[name='5']:checked").val(),
        wenjuan_6:$("input[name='6']:checked").val(),
        wenjuan_7:$("input[name='7']:checked").val(),
        },function(data,status){
        if(data=="问卷提交成功"){
        alert(data); 
        window.location.href=window.location.href;
        // window.location.reload()
        }
        else{if(data=="请联系工作人员了解相关政策"){
        alert(data); 
        window.location.href=window.location.href;
        // window.location.reload()
        }
        else{
        alert(data);
        }}
        });
        }
        else{
        alert("请确认您所填的信息准确");
        }
    })
    $('#add_yuyue').click(function () {
    // $(this).after($(this).attr("id"));
        $.post("/yuyue_list",{name:$("#id_name").val(),
        age:$("#id_age").val(),
        sex:$("#id_sex").val(),
        phone:$("#id_phone").val(),
        id_type:$("#id_id_type").val(),
        id_code:$("#id_id_code").val(),
        yuyue_date:$("#id_yuyue_date").val(),
        yuyue_time:$("#id_yuyue_time").val(),
        },function(data,status){
        if(data=="预约信息提交成功"){
        alert(data); 
        window.location.reload()
        }
        else{
        alert(data);
        }
        });
    })
    $('#alert_show').click(function () {
        window.location.href="yuyue_alert";
        $('#alert_div')[0].scrollIntoView(true);
    })
    $('#alert_cancel').click(function () {
        window.location.href="yuyue_wx";
        $('#add_yuyue_div')[0].scrollIntoView(true);
    })
    $('#list_show').click(function () {
        $('#add_yuyue_div').hide()
        $('#main_div').show()
        $('#yuyue_bt').show()
        $('#main_div')[0].scrollIntoView(true);
    })
    $('#list_cancel').click(function () {
        window.open("preorder.html");
        $('#add_yuyue_div')[0].scrollIntoView(true);
    })
    $('#pay_cancel').click(function () {
        $('#pay_yuyue').attr('pay_bill','')
        $('#main_div').show()
        $('#yuyue_bt').show()
        $('#payment_div').hide()
    })
    $('#pay_yuyue').click(function () {
        $.post("/yuyue_detail",{
        opt:"pay",
        table_id:$(this).attr('pay_bill'),
        },function(data,status){
        var info = jQuery.parseJSON(data)
        function onBridgeReady(){
        WeixinJSBridge.invoke(
            'getBrandWCPayRequest', {
                "appId":info.appId,     //公众号名称，由商户传入     
                "timeStamp":info.timeStamp,         //时间戳，自1970年以来的秒数     
                "nonceStr":info.nonceStr, //随机串     
                "package":info.package,     
                "signType":info.signType,         //微信签名方式：     
                "paySign":info.paySign //微信签名 
            },
            function(res){
            if(res.err_msg == "get_brand_wcpay_request:ok" ){
        $.post("/yuyue_detail",{
        opt:"pay_done",
        table_id:$('#pay_yuyue').attr('pay_bill'),
        prepay_id:info.package,
        },function(data,status){
        if(data=="已支付该预约"){
        // alert(data); 
        window.location.reload()
        }
        else{
        alert("支付状态更新失败，请联系管理员确认收款");
        }
        })
        $('#pay_yuyue').attr('pay_bill','')
        $('#main_div').show()
        $('#payment_div').hide()
            // 使用以上方式判断前端返回,微信团队郑重提示：
                    //res.err_msg将在用户支付成功后返回ok，但并不保证它绝对可靠。
            } 
        else{
        alert("支付异常");
        }
        }); 
        }
        if (typeof WeixinJSBridge == "undefined"){
        if( document.addEventListener ){
            document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
        }else if (document.attachEvent){
            document.attachEvent('WeixinJSBridgeReady', onBridgeReady); 
            document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
        }
        }else{
        onBridgeReady();
        }
        });
    })
        // config信息验证后会执行ready方法，所有接口调用都必须在config接口获得结果之后，config是一个客户端的异步操作，所以如果需要在页面加载时就调用相关接口，则须把相关接口放在ready函数中调用来确保正确执行。对于用户触发时才调用的接口，则可以直接调用，不需要放在ready函数中。
    });
    })