# -*- coding: utf-8 -*-
<%inherit file="common_base.mako" />
<%namespace name="shared" file="modules/shared.mako" />
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
   		${shared.footer()}
    ${shared.js_files()}
    ${self.jquery_additional()}
<div id="fb-root"></div>
</body>
