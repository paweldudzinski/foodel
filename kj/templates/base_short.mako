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
