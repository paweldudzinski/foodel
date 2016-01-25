# -*- coding: utf-8 -*
<%namespace name="modals" file="modals.mako" />

<%def name="messages()" filter="trim">
    %for msg in req.session.pop_flash():
    <%
       cls = "alert"
       i = msg.find(":")
       if i != -1:
           t = msg[:i].strip().lower()
           if t in ["error", "info", "success"]:
               cls += " alert-" + t
           msg = msg[i+1:].strip()  
    %>
    <div class="${cls}">
      ${msg |n}
    </div>
    %endfor
</%def>

<%def name="avatar(user, prefix='avatar_')" filter="trim">
    %if user.avatars:
        <div class="avatar ${prefix}avatar" style="background:url(${user.avatars[0].get_url(prefix=prefix)}) #7d919a center no-repeat;"></div>
    %else:
        <div class="avatar icon s07-no-avatar"></div>
    %endif
</%def>

<%def name="menu_entry(href, link_name, class_sufix, add_class='')" filter="trim">
<div class="menu-relativeposition">
    <div class="main-link-icons ${add_class}">
        <a href="${href}" class="whitelink whitelink-${class_sufix}" title="${link_name}"></a><br />
        <a class="lobster main-link bluish" href="${href}">${link_name}</a>
    </div>
</div>
</%def>

<%def name="cerata(mb, border=False)" filter="trim">
    <div class="cerata" style="margin-bottom:${mb}px; ${'border-top:1px dashed #2e0808' if border else ''}"></div>
</%def>

<%def name="register_simple_input(name, type, text_label, value=None, disabled=False, with_null_option=True,
                                  readonly=False, select_values=None, selected_value=None, special_id=None,
                                  quantity_measures=[])">
    <div class="register-label fleft">${text_label}:</div>
    <div class="register-input fleft">
    %if type == 'select' and select_values:
        <select autocomplete="off" name="${name}" id="${special_id or name}" style="width:323px;">
            %if with_null_option:
                <option value="">--- wybierz ---</option>
            %endif
            %for value, name in select_values:
            <option ${'selected="selected"' if selected_value==value else ''} value="${value}">${name}</option>
            %endfor
        </select>
    %elif type == 'select' and not select_values:
        <select name="${name}" id="${special_id or name}" style="width:323px;">
            <option value="">--- najpierw wybierz coś powyżej ---</option>
        </select>
    %elif type == 'textarea':
        <textarea style="width:310px; height:150px;" name="${name}" id="${name}">${value or ''}</textarea>
    %else:
        <input ${'disabled="disabled"' if disabled else ''} style="${'width:130px;' if quantity_measures else ''}"
               ${'readonly="readonly"' if readonly else ''} 
               type="${type}" name="${name}" id="${special_id or name}" value="${value or ''}" />
    %endif
    
    %if quantity_measures:
        / <select name="quantity_measure" id="quantity_measure" style="width:165px;">
            %for qm in quantity_measures:
                <option ${'selected="selected"' if selected_value == qm[0] else ''} value="${qm[0]}">${qm[1]}</option>
            %endfor
        </select>
    %endif
    
    </div>
    <div style="clear:both; padding-top:10px;"></div>
</%def>

<%def name="register_hours_input(title, hour_name, minute_name, hvalue, mvalue)" filter="trim">
    <%
        hvalue = hvalue or 12
        mvalue = mvalue or 0
    %>
    <div class="register-label fleft">${title}:</div>
    <div class="register-input fleft">
            <select autocomplete="off" name="${hour_name}" id="${hour_name}" style="width:55px;">
                %for hour in xrange(24):
                    <option ${'selected="selected"'if int(hour) == int(hvalue) else ''}
                     value="${hour}">${hour if int(hour) >=10 else '0%s' % (hour)}</option>
                %endfor
            </select>
            :
            <select autocomplete="off" name="start_minute" id="${minute_name}" style="width:55px;">
                %for minute in xrange(0, 60, 5):
                    <option ${'selected="selected"'if int(minute) == int(mvalue) else ''}
                     value="${minute}">${minute if int(minute) >= 10 else '0%s' % (minute)}</option>
                %endfor
            </select>
        </div>
    <div style="clear:both; padding-top:10px;"></div>
</%def>

<%def name="no_photo_in_product_list()" filter="trim">
    <div class="photo-green-border no-product-for-list">
        <div>?</div>
    </div>
</%def>

<%def name="no_photo_in_product_details()" filter="trim">
    <div class="photo-red-border no-product-for-details">
        <div>?</div>
    </div>
</%def>

<%def name="mail(user)" filter="trim">
    %if user:
        <a href="${request.route_path('my_threads')}" class="icon s09-mail"></a>
    %endif
</%def>

<%def name="brown_section_header(text, icon)" filter="trim">
    <div class="icon sprite-09-browns-${icon}"></div>
    <div class="brown-text lobster"><div>${text.capitalize()}</div></div>
    <div style="clear:both;"></div>
</%def>

<%def name="photo_in_product_list(product)" filter="trim">
    %if product.get_main_photo_url('tiny'):
    <div style="height:40px; width:40px; text-align:center; display:inline-block;">
    <img style="height:40px; max-width:40px; *width:40px; zoom:1" 
         class="photo-green-border"
         src="${product.get_main_photo_url('tiny_')}" 
         title="${product.name}" 
         alt="${product.name}">
    </div>
    %else:
        ${no_photo_in_product_list()}
    %endif
</%def>

<%def name="orders_buttons(counts_container, action, show_grading=False)" filter="trim">
<div class="fleft">
    <a href="${request.route_path(action, kind='zakonczone')}" class="btn btn-primary btn-small">Zakończone (${counts_container['F']})</a>
    <a href="${request.route_path(action, kind='anulowane')}" class="btn btn-primary btn-small">Anulowane (${counts_container['C']})</a>
    %if show_grading and gradable_orders and len(gradable_orders) > 0:
        <a href="${request.route_path('orders_for_grading')}" class="btn btn-success btn-small">Do oceny (${len(gradable_orders)})</a>
    %endif
</div>
<div class="fright">
    <form id="transactions-filter" action="${request.route_path('transactions_apply_filter')}" method="POST">
        <span style="font-size:0.9em; font-weight:bold;">Pokaż:</span>
        <select name="time" id="time" class="select-filter">
            %for t in TIMES_SORTED:
                <option ${'selected="selected"' if str(t) == str(tfilters['time']) else ''} 
                        value="${t}">${TIMES[t]}</option>
            %endfor
        </select>&nbsp;&nbsp;&nbsp;
        <span style="font-size:0.9em; font-weight:bold;">Sortuj po:</span>
        <select name="sort" id="sort" class="select-filter">
            %for s in TYPE_SORTED_SORTED:
                <option ${'selected="selected"' if str(s) == str(tfilters['type']) else ''}
                        value="${s}">${TYPE_SORTED[s]}</option>
            %endfor
        </select>
    </form>
</div>
<div style="clear:both;"></div>
</%def>

<%def name="grade_hats(count)" filter="trim">
    %for i in xrange(0,count):
        <div class="icon s11-hat-on" style="margin-right:3px;"></div>
    %endfor
    %for k in xrange(i+1, 5):
        <div class="icon s11-hat-off" style="margin-right:3px;"></div>
    %endfor
</%def>

<%def name="js_files()" filter="trim">
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js"></script>
    <script src="${req.static_url('kj:static/js/vendor/jquery.jgrowl.js')}"></script>
    <script src="${req.static_url('kj:static/js/vendor/bootstrap.min.js')}"></script>
    <script src="${req.static_url('kj:static/js/vendor/jquery.colorbox.js')}"></script>
    <script src="${req.static_url('kj:static/js/vendor/imagesloaded.js')}"></script>
    <script src="${req.static_url('kj:static/js/vendor/jquery.masonry.min.js')}"></script>
    <script src="${req.static_url('kj:static/js/vendor/jquery.reveal.js')}"></script>
    <script src="${req.static_url('kj:static/js/vendor/datepicker.js')}"></script>
    <script type="text/javascript" src="//assets.pinterest.com/js/pinit.js"></script>
    <script src="${req.static_url('kj:static/js/main.js')}"></script>
</%def>

<%def name="css_and_modernizr_files()" filter="trim">
    <link href='http://fonts.googleapis.com/css?family=Lobster&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" type="text/css" href='http://fonts.googleapis.com/css?family=Advent+Pro&subset=latin,latin-ext'>
    <link href='//fonts.googleapis.com/css?family=Open+Sans:400italic,800italic,400,700,800&amp;subset=latin,latin-ext' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" type="text/css" href="${req.static_url('kj:static/css/bootstrap.css')}">
    <link rel="stylesheet" type="text/css" href="${req.static_url('kj:static/css/bootstrap-responsive.min.css')}">
    <link rel="stylesheet" type="text/css" href="${req.static_url('kj:static/css/main.css')}">
    <link rel="stylesheet" type="text/css" href="${req.static_url('kj:static/css/colorbox.css')}">
    <link rel="stylesheet" type="text/css" href="${req.static_url('kj:static/css/jquery.jgrowl.css')}">
    <link rel="stylesheet" type="text/css" href="${req.static_url('kj:static/css/reveal.css')}">
    <link rel="stylesheet" type="text/css" href="${req.static_url('kj:static/css/datepicker.css')}">
    <script src="${req.static_url('kj:static/js/vendor/modernizr-2.6.2-respond-1.1.0.min.js')}"></script>
</%def>

<%def name="header_links(user)" filter="trim">
	<div class="main-link-icons ">
		%if user:
			${avatar(user)}<br />
        	<span class="lobster main-link" style="color:#fff;">${user.user_name()}</span> 
        %else:
        	<a data-reveal-id="login-modal" data-animation="fade" href="#" class="whitelink whitelink-events" title="zaloguj"></a><br>
	        <a data-reveal-id="login-modal" data-animation="fade" href="#" class="lobster main-link">zaloguj</a>
	        ${modals.modal_login()}
        %endif
    </div>
	${menu_entry(request.route_path('home_buy'), u'kupię', 'group')}
	${menu_entry(request.route_path('home_change'), u'zamienię', 'buy')}
	${menu_entry(request.route_path('home_add'), u'dodaj produkt', 'add')}
</%def>

<%def name="top_shelf(user)" filter="trim">
    <section class="login-info-bar-prolong top-top">
    <section class="login-info-bar main-content">
        %if user:
            ${user.user_name()} 
            ::
            <a class="seledine" href="${request.route_path('pa_home')}">moje konto</a>
            %if user and user.get_number_of_unread_messages():
                ${mail(user)}
            %endif
            ::
            <a class="seledine" href="${request.route_path('logout')}">wyloguj</a>
        %else:
            <a class="seledine" data-reveal-id="login-modal" data-animation="fade" href="#">zaloguj się</a>
            ${modals.modal_login()}
            ::
            <a class="seledine" href="${request.route_path('register')}">zarejestruj się</a>
        %endif
    </section>
    <div class="line"></div>
    </section>
</%def>

<%def name="title_shelf(title)" filter="trim">
    <section class="title-bar-prolong">
        <div class="line"></div>
        <section class="title-bar main-content">&nbsp;&raquo; ${title |n}</section>
        <div class="line"></div>
    </section>
</%def>


<%def name="outdated()" filter="trim">
    <!--[if lt IE 7]>
        <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
    <![endif]-->
</%def>

<%def name="paginator(collection)" filter="trim">
    %if collection.page_count > 1:
    <div class="paginator">
        ${collection.pager(format='$link_first $link_previous ~2~ $link_next $link_last')}
    </div>
    %endif
</%def>

<%def name="search()" filter="trim">
<div class="search-input-container">
	Wpisz swój kod pocztowy:
    <form id="search-form" action="${request.route_path('search')}">
    <input type="text" name="keyword" class="lobster search-input" value="${keyword or ''}" />
    <a class="icon s16-icon-search search-button" href="#"></a>
    </form>
</div>
</%def>

<%def name="logo()" filter="trim">
    <a href="/" class="logo"></a>
</%def>

<%def name="product_ogs(product)" filter="trim">
    <meta property="og:title" content="${product.name}" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="${request.registry.settings.get('domain_url')}${product.get_sef_url()}" />
    <meta property="og:image" content="${request.registry.settings.get('domain_url')}${product.get_main_photo_url('big_')}" />
    <meta property="og:description" content="${product.description}" />
    <meta property="fb:admins" content="686553089" />
</%def>

<%def name="site_ogs()" filter="trim">
    <meta property="og:title" content="Foodel" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="${request.registry.settings.get('domain_url')}" />
    <meta property="og:image" content="${request.registry.settings.get('domain_url')}/static/images/f-logo.jpg" />
    <meta property="og:description" content="Foodel :: Platforma zakupu i wymiany jedzienia" />
    <meta property="fb:admins" content="686553089" />
</%def>
