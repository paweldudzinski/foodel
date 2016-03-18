# -*- coding: utf-8 -*-
<%namespace name="shared" file="modules/shared.mako" />
<%namespace name="modals" file="modules/modals.mako" />
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
        <link rel="shortcut icon" type="image/png" href="static/foodel.ico"/>
        ${shared.css_and_modernizr_files()}
        %if product:
            ${shared.product_ogs(product)}
        %else:
            ${shared.site_ogs()}
        %endif
        ${self.maps_js()}
    </head>
    <body>
        ${shared.outdated()}        
        <section class="wide">
            <header class="links-and-search-area">
                <section class="main-content">
                    <div class="logo-and-links">
                        ${shared.logo()}
                        ${shared.header_links(req.user)}
                        <div style="clear:both;"></div>
                    </div>
                </section>
           <hr />
           <header class="links-and-search-area">
                <section class="main-content"> 
                    <div class="captions">
                    	<h1>LOKALNE JEDZENIE DLA CIEBIE</h1>
                    	<h2>Wymieniaj i kupuj domowe jedzenie od sąsiada.</h2>
                    </div>
                    ${shared.search()}
                </section>
            </header>
         </section>
            ${shared.title_shelf(title=title or u'Uzupełnij')}
            ${next.body()}
       
        ${shared.js_files()}
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
