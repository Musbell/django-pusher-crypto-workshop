var pusherConnect = (function () {

  Pusher.logToConsole = true;
  var _pusher;

  return function(){

    if (_pusher){
      return _pusher
    }

    _pusher = new Pusher(window.APP_CONF.pusher.appKey, {
      encrypted: true,
      // cluster: window.APP_CONF.pusher.cluster,
      // authEndpoint: window.APP_CONF.pusher.authEndpoint,
      // auth: {
      //   headers: {
      //     'X-CSRFToken': window.APP_CONF.csrfToken
      //   }
      // }
    });
    return _pusher;
  }
})();
