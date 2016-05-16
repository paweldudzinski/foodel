# -*- coding: utf-8 -*-
<%namespace name="shared" file="modules/shared.mako" />
<%namespace name="modals" file="modules/modals.mako" />
<%namespace name="ms" file="modules/main_site.mako" />
<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Foodel! Kocham jedzenie</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">
        ${shared.css_and_modernizr_files()}
    </head>
    <body class="admin-body">
        ${shared.outdated()}
        <section class="wide-short">
            <header class="links-and-search-area">
                <section class="main-content">
                    <div class="logo-and-links">
                        ${shared.logo()}
                        ${shared.zip_code(h.provided_zip_code(req))}
                        ${shared.header_links(req.user)}
                        <div style="clear:both;"></div>
                    </div>
                </section>
            </header>
            <div class="line" style="margin-top:10px;"></div>
            <section class="content main-content">
				${shared.title_shelf(title=title or u'Uzupełnij')}
                ${next.body()}
                <div style="clear:both;"></div>
                <br /><br />
            </section>
            ${shared.footer()}
        </section>

        ${shared.js_files()}
        ${self.jquery_additional()}
    </body>
</html>

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
