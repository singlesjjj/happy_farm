/*Toast Init*/


$(document).ready(function() {
	"use strict";
	
    $("body").removeAttr('class').removeClass("bottom-center-fullwidth").addClass("top-center-fullwidth");
	$.toast({
		heading: '账号密码错误',
		text: '您使用的账号密码有误，请确认后重试',
		position: 'top-center',
		loaderBg:'#3cb878',
		icon: 'error',
		hideAfter: 5000,
		stack: 6
	});
});
          
