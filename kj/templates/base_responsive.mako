# -*- coding: utf-8 -*-
<%namespace name="shared" file="modules/shared.mako" />
<%namespace name="modals" file="modules/modals.mako" />
<!DOCTYPE html>
<html>
  <head>
	<title>Foodel</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="shortcut icon" type="image/png" href="static/foodel.ico"/>
	<!-- Bootstrap -->
	${shared.css_and_modernizr_files(scaffold_bootstrap=True)}
  </head>
  <body>
	<h1>Hello, world!</h1>
	<script src="http://code.jquery.com/jquery.js"></script>
	<script src="js/bootstrap.min.js"></script>
	
	
	<section class="wide"></section>
	
	
	
	${shared.js_files(scaffold_bootstrap=True)}
    ${self.jquery_additional()}
    <div id="fb-root"></div>
  </body>
</html>

<%def name="maps_js()" filter="trim"></%def>

<%def name="jquery_additional()"></%def>
<%
    flash_messages = req.session.pop_flash()
    flash_messages = "<br />".join(x for x in flash_messages)
%>
%if flash_messages:
    <script>
        $.jGrowl('${flash_messages}');
    </script>
%endif

<script>
window.fbAsyncInit = function() {
    FB.init({
        appId   : '212226432300981',
        oauth   : true,
        status  : true, // check login status
        cookie  : true, // enable cookies to allow the server to access the session
        xfbml   : true // parse XFBML
    });
    
    /*
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            alert("yes");
            var uid = response.authResponse.userID;
            var accessToken = response.authResponse.accessToken;
        } else if (response.status === 'not_authorized') {
            alert("no");
        } else {
            alert("no");
        }
    }, true);
    */
  };

function fb_logout(){
    FB.logout();
}

function fb_login(){
    FB.login(function(response) {

        if (response.authResponse) {
            access_token = response.authResponse.accessToken; //get access token
            user_id = response.authResponse.userID; //get FB UID

            FB.api('/me', function(response) {
                $.getJSON("/zaloguj-fb", {response : response}, function(data) {
                    var json = $.parseJSON(data);
                    window.location = json.request_url;
                });
            });

        } else {
            console.log('User cancelled login or did not fully authorize.');

        }
    }, {
        scope: 'email,user_location,user_hometown'
    });
}
(function() {
    var e = document.createElement('script');
    e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
    e.async = true;
    document.getElementById('fb-root').appendChild(e);
}());
</script>
