function setCookie(name, value, expires) {
  var cookieString = name + '=' + value;
  if (expires) {
    var expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() + expires); // 过期时间为expires天后
    cookieString += '; expires=' + expiryDate.toUTCString();
  }
  document.cookie = cookieString;
}
function getCookie(cookieName) {
  var cookies = document.cookie.split("; ");
  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i].split("=");
    if (cookie[0] === cookieName) {
      return cookie[1];
    }
  }
  return "";
}