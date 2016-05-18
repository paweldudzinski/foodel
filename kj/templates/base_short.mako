# -*- coding: utf-8 -*-
<%inherit file="common_base.mako" />
<%namespace name="shared" file="modules/shared.mako" />
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

