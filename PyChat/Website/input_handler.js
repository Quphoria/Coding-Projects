"use strict";
//Coded by Samuel Simpson
//DO NOT attempt to change this as the server has verification to check that clients are valid
function savecookie() {
  short_callback()
  var nick = document.getElementById ('text_2').value;
  console.log(nick);
  setCookie("ChatWebClientNickname",String(nick));
}

function setCookie(cname, cvalue) {
  var name = String(cname), value = String(cvalue), path = 'path', domain = 'domain', ATS_getExpire = function() { return 'ATS_getExpire'; };
  var curCookie = name + "=" + value + "; expires=" + "Tue, 19 Jan 2038 03:14:07 GMT" + ",path=" + path + ", domain=" + domain;
  document.cookie = curCookie;
  window.location.href="chat.html";
}

function short_callback() {
  var msg = document.getElementById ('text_2').value;
  //var c = msg.__getslice__ (0, 30, 1);
  var c = msg.slice(0,30,1);
  var outtext = "";
  var smsg = false;
  for (var charindex = 0; charindex < c.length; charindex++) {
    var letter = c[charindex];
    // console.log(letter);
    // console.log(c.charCodeAt(charindex));
    if (c.charCodeAt(charindex) == 10) {
      smsg = true;
    }
    else if (letter != '\\' && letter != "," && !smsg) {
      var outtext = outtext.concat(letter);
    }
  }
  document.getElementById ('text_2').value = outtext;
  if (smsg) {
    savecookie();
  }
}
