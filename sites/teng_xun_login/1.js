(function(){window.onerror=function(f,b,a){var e=location.protocol=="https:"?"https://ssl.qq.com/ptlogin/cgi-bin/ptlogin_report?":"http://log.wtlogin.qq.com/cgi-bin/ptlogin_report?";var c=document.createElement("img");var d=encodeURIComponent(f+"|_|"+b+"|_|"+a+"|_|"+window.navigator.userAgent);c.src=e+"id=195279&msg="+d+"&v="+Math.random()}})();var g_cdn_js_fail=false;var pt={};pt.str={no_uin:"您还没有输入帐号！",no_pwd:"您还没有输入密码！",no_vcode:"您还没有输入验证码！",inv_uin:"请输入正确的帐号！",inv_vcode:"请输入完整的验证码！",qlogin_expire:"您所选择号码对应的QQ已经失效，请检查该号码对应的QQ是否已经被关闭。",other_login:"帐号登录",h_pt_login:"帐号密码登录",otherqq_login:"QQ帐号密码登录"};pt.ptui={s_url:"http\x3A\x2F\x2Ft.qq.com\x2F",proxy_url:"http\x3A\x2F\x2Ft.qq.com\x2Fproxy_t.html",jumpname:encodeURIComponent(""),mibao_css:encodeURIComponent(""),defaultUin:"",lockuin:parseInt("0"),href:"https\x3A\x2F\x2Fxui.ptlogin2.qq.com\x2Fcgi-bin\x2Fxlogin\x3Fappid\x3D46000101\x26style\x3D23\x26lang\x3D\x26low_login\x3D1\x26hide_border\x3D1\x26hide_title_bar\x3D1\x26hide_close_icon\x3D1\x26border_radius\x3D1\x26self_regurl\x3Dhttp\x253A\x2F\x2Freg.t.qq.com\x2Findex.php\x26proxy_url\x3Dhttp\x3A\x2F\x2Ft.qq.com\x2Fproxy_t.html\x26s_url\x3Dhttp\x253A\x252F\x252Ft.qq.com\x252F\x26daid\x3D6",login_sig:"",clientip:"",serverip:"",version:"201203081004",ptui_version:encodeURIComponent("10135"),isHttps:false,cssPath:"https://ui.ptlogin2.qq.com/style.ssl/23",domain:encodeURIComponent("qq.com"),fromStyle:parseInt(""),pt_3rd_aid:encodeURIComponent("0"),appid:encodeURIComponent("46000101"),lang:encodeURIComponent("2052"),style:encodeURIComponent("23"),low_login:encodeURIComponent("1"),daid:encodeURIComponent("6"),regmaster:encodeURIComponent(""),enable_qlogin:"1",noAuth:"0",target:(isNaN(parseInt("1"))?{_top:1,_self:0,_parent:2}["1"]:parseInt("1")),csimc:encodeURIComponent("0"),csnum:encodeURIComponent("0"),authid:encodeURIComponent("0"),auth_mode:encodeURIComponent("0"),pt_qzone_sig:"0",pt_light:"0",pt_vcode_v1:"1",pt_ver_md5:"000D5A63AFD8E43E31F56095BF5ABDAC41EDDBFB1BD451D648BD1F54",gzipEnable:"1"}; function cleanCache(e){var t=document.createElement("iframe");3==e.split("#").length&&(e=e.substring(0,e.lastIndexOf("#"))),t.src=e,t.style.display="none",document.body.appendChild(t)}function loadScript(e,t,n){var o=document.createElement("script");o.type="text/javascript",o.charset="utf-8",o.onload=o.onerror=o.onreadystatechange=function(){return window[n]?void(loadJs.onloadTime=+new Date):void(this.readyState&&("loaded"!==this.readyState&&"complete"!==this.readyState||window[n])||(t&&t(),o.onerror=o.onreadystatechange=null))},o.src=e,document.getElementsByTagName("head")[0].appendChild(o)}function ptuiV(e){e!=window.pt.ptui.ptui_version&&cleanCache("/clearcache.html#"+location.href)}function checkVersion(){var e=document.createElement("script");e.src="/ptui_ver.js?v="+Math.random()+"&ptui_identifier="+pt.ptui.pt_ver_md5,document.body.appendChild(e)}function loadJs(){1!=loadJs.hasLoad&&(loadJs.hasLoad=!0,loadScript("../js/10135/c_login_2.js?max_age=604800&ptui_identifier=000D5A63AFD8E43E31F56095BF5ABD0123B03F5E4D5E37616D2851AF7B",function(){window.g_cdn_js_fail=!0;var e=new Image;e.src=location.protocol+"//ui.ptlogin2.qq.com/cgi-bin/report?id=242325&union=256043";var t="../js/"+pt.ptui.ptui_version+"/c_login_2.js?max_age=604800&ptui_identifier=000D5A63AFD8E43E31F56095BF5ABD0123B03F5E4D5E37616D2851AF7B";loadScript(t,function(){var t=document.getElementById("login_button");t&&(t.disabled=!0),e.src=location.protocol+"//ui.ptlogin2.qq.com/cgi-bin/report?id=280504"},"ptuiCB")},"ptuiCB"),ready())}function ready(){window.setTimeout(checkVersion,1500)}document.addEventListener&&document.addEventListener("DOMContentLoaded",loadJs),window.onload=loadJs,window.setTimeout(loadJs,5e3);