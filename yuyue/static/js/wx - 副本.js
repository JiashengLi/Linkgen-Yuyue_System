/*!global gettext, interpolate, ngettext*/
    $(document).ready(function(){
$('#payment_div').hide()
       $.post("/yuyue_wx",{},function(data,status){
          var info = jQuery.parseJSON(data)
wx.config({
    // beta: true,// 必须这么写，否则wx.invoke调用形式的jsapi会有问题
    debug: true, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
    appId: info.appId, // 必填，企业微信的corpID
    timestamp: info.timestamp, // 必填，生成签名的时间戳
    nonceStr: info.nonceStr, // 必填，生成签名的随机串
    signature: info.signature,// 必填，签名，见附录1
    jsApiList: ["scanQRCode"] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
});
wx.ready(function(){
$('#id_qcode').click(function () {
wx.scanQRCode({
    needResult: 1, // 默认为0，扫描结果由微信处理，1则直接返回扫描结果，
    scanType: ["qrCode","barCode"], // 可以指定扫二维码还是一维码，默认二者都有
    success: function (res) {
    var result = res.resultStr; // 当needResult 为 1 时，扫码返回的结果
$('#id_qcode').val(result)
}
});
})
$('.pay_table').click(function () {
// $(this).after($(this).attr("id"));
$('#pay_yuyue').attr('pay_bill',$(this).parent().attr("id"));
$.get("/yuyue_list",{opt:"show",table_id:$(this).parent().attr("id")},function(data,status){
//           var info = jQuery.parseJSON(data)
$('#payment_panel').empty();
$('#payment_panel').append(data);
$('#main_div').hide()
$('#payment_div').show()
// $('#payment_div')[0].scrollIntoView(true);
});
})
$('.del_table').click(function () {
if(confirm("确定删除该预约？")){
$.post("/yuyue_detail",{opt:"delete",table_id:$(this).parent().attr("id")},function(data,status){
if(data=="预约已删除"){
alert(data); 
window.location.reload()
}
else{
alert(data);
}
});
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
$('#pay_cancel').click(function () {
$('#pay_yuyue').attr('pay_bill','')
$('#main_div').show()
$('#payment_div').hide()
}）
$('#pay_yuyue').click(function () {
$.post("/yuyue_detail",{
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
      // 使用以上方式判断前端返回,微信团队郑重提示：
            //res.err_msg将在用户支付成功后返回ok，但并不保证它绝对可靠。
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
$('#pay_yuyue').attr('pay_bill','')
$('#main_div').show()
$('#payment_div').hide()
})
    // config信息验证后会执行ready方法，所有接口调用都必须在config接口获得结果之后，config是一个客户端的异步操作，所以如果需要在页面加载时就调用相关接口，则须把相关接口放在ready函数中调用来确保正确执行。对于用户触发时才调用的接口，则可以直接调用，不需要放在ready函数中。
});
wx.error(function(res){
$('#result').html(res)
    // config信息验证失败会执行error函数，如签名过期导致验证失败，具体错误信息可以打开config的debug模式查看，也可以在返回的res参数中查看，对于SPA可以在这里更新签名。

});
})
})