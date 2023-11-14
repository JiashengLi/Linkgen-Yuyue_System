/*!global gettext, interpolate, ngettext*/
    $(document).ready(function(){
$('#add_yuyue_div').hide()
$('#payment_div').hide()
$('#alert_div').hide()
$('#wenjuan_div').hide()
       $.post("/yuyue_wx",{},function(data,status){
          var info = jQuery.parseJSON(data)
wx.config({
    // beta: true,// 必须这么写，否则wx.invoke调用形式的jsapi会有问题
    debug: false, // true, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
    appId: info.appId, // 必填，企业微信的corpID
    timestamp: info.timestamp, // 必填，生成签名的时间戳
    nonceStr: info.nonceStr, // 必填，生成签名的随机串
    signature: info.signature,// 必填，签名，见附录1
    jsApiList: ["scanQRCode"] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
});
wx.ready(function(){
$('.test_table').click(function () {
var table_id = $(this).attr("id")
// alert(table_id); 
wx.scanQRCode({
    needResult: 1, // 默认为0，扫描结果由微信处理，1则直接返回扫描结果，
    scanType: ["qrCode","barCode"], // 可以指定扫二维码还是一维码，默认二者都有
    success: function (res) {
    var result = res.resultStr; // 当needResult 为 1 时，扫码返回的结果
// alert(table_id); 
$.post("/yuyue_detail",{
opt:"barcode",
table_id:table_id,
barcode:result
},function(data,status){
if(data=="成功绑定条码"){
alert(data); 
window.location.reload()
}
else{
alert(data);
}
});
}
});
})
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
window.location.reload()
}
else{if(data=="请联系工作人员了解相关政策"){
alert(data); 
window.location.reload()
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
$('#add_yuyue_div').hide()
$('#alert_div').show()
$('#alert_div')[0].scrollIntoView(true);
})
$('#alert_cancel').click(function () {
$('#alert_div').hide()
$('#add_yuyue_div').show()
$('#add_yuyue_div')[0].scrollIntoView(true);
})
$('#list_show').click(function () {
$('#add_yuyue_div').hide()
$('#main_div').show()
$('#yuyue_bt').show()
$('#main_div')[0].scrollIntoView(true);
})
$('#list_cancel').click(function () {
$('#main_div').hide()
$('#yuyue_bt').hide()
$('#add_yuyue_div').show()
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
wx.error(function(res){
$('#result').html(res)
    // config信息验证失败会执行error函数，如签名过期导致验证失败，具体错误信息可以打开config的debug模式查看，也可以在返回的res参数中查看，对于SPA可以在这里更新签名。

});
})
})