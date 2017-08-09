/*Toast Init*/


$(document).ready(function() {
	"use strict";
	
    $("body").removeAttr('class').removeClass("bottom-center-fullwidth").addClass("top-center-fullwidth");
	$.toast({
		heading: '连接失败',
		text: '登录连接失败，请稍后重试',
		position: 'top-center',
		loaderBg:'#3cb878',
		icon: 'error',
		hideAfter: 5000,
		stack: 6
	});
});
          
