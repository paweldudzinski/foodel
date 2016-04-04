# -*- coding: utf-8 -*
<%namespace name="shared" file="shared.mako" />
<%def name="wizard_box()" filter="trim">
    <div class="wizard-box">
    </div>
</%def>

<%def name="login_box(details=False)" filter="trim">
    <div class="login-box">
        <br />
        <section>
        %if req.user:
            <div style="width:90%;">
                <div>
                    <div style="float:left; margin-right:15px;">
                        ${shared.avatar(req.user)}
                    </div>
                    <div style="float:left;">
                        <strong>${req.user.user_name()}</strong><br />
                        ${h.email_truncate(req.user.email, 24)}<br />
                        <div style="text-align:left; width:100%; font-size:0.8em;">
                            <a href="${request.route_path('logout')}">Wyloguj</a>
                        </div>
                    </div>
                    <div style="clear:both; padding-top:20px;"></div>
                </div>
                %if details:
                    <div class="logged-details">
                        <a href="${request.route_path('pa_edit_me')}">Edycja profilu:</a><br />
                        <div class="line" style="margin:6px 0px;"></div>
                    
                        <a href="${request.route_path('my_product_for_sale')}">Produktów do sprzedaży:</a><strong>
                        ${req.user.get_product_for_sales_count()}</strong><br />
                        
                        <a href="${request.route_path('my_product_for_exchange')}">Produktów do wymiany:</a><strong>
                        ${req.user.get_product_for_exchange_count()}</strong><br />
                        
                        <div class="line" style="margin:6px 0px;"></div>
                        
                        <a href="${request.route_path('my_orders_sold', kind='zakonczone')}">Moja sprzedaż</a><br />       
                        <a href="${request.route_path('my_orders_bought', kind='zakonczone')}">Moje zakupy</a>
                          
                        <div class="line" style="margin:6px 0px;"></div>
                        
                        <a href="${request.route_path('my_threads')}">Wiadomości</a>
                        (nowych: <strong>${req.user.get_number_of_unread_messages()}</strong>)
                        
                        <div class="line" style="margin:6px 0px;"></div>
                        
                        <a href="${req.user.profile_link(req)}">Pokaż mój profil</a>
                    </div>
                %else:
                    <br />
                    <a class="btn btn-primary btn-medium" href="${request.route_path('pa_home')}">PANEL KLIENTA</a>
                %endif
            </div>
        %else:
            <form action="${request.route_path('login')}" method="POST">
                <div class="fleft input-label">Twój e-mail:</div>
                <div class="fleft input-field"><input type="email" name="email" id="email" /></div>
                <div style="clear:both;"></div>
                <div class="fleft input-label">Hasło:</div>
                <div class="fleft input-field"><input type="password" name="password" id="password" /></div>
                <div style="clear:both;"></div>
                <div style="margin:5px 0px 10px 0px; text-align:center; width:100%;">
                    <input name="form.submitted" class="btn btn-primary btn-medium" type="submit" value="ZALOGUJ" />
                </div>
                <div style="text-align:center; width:100%; font-size:0.8em;">
                    <a href="${request.route_path('register')}">Zarejestruj nowe konto</a>&nbsp;&nbsp;::&nbsp;&nbsp;<a href="#">Przypomnij mi hasło</a>
                </div>
            </form>
        %endif
        </section>
    </div>
</%def>

<%def name="chunk_of_categories(mosaic)" filter="trim">
	%if not mosaic:
		<i>Nic nie znaleziono :(</i>
	%endif
	
	%for i, m in mosaic.iteritems():
		<%
			category = m['category']
			product = m['product']
			href = request.route_path('home_show_products', id=category.id, sef=h.make_sef_url(category.name))
		%>
		<div class="tile">
			<div class="pale-box" style="width:215px; margin:0px auto;">
				<div class="in-tile">
					<div style="width:100%; text-align:left;">
						<div style="padding:9px;">
							<a title="Pokaż co tam jest" href=${href}>
								<span class="lobster" style="font-size:18px;">
									${h.smart_truncate(category.name, 40)}
								</span>
							</a>
						</div>
					<a class="product-photo" title="${product.name}" href=${href} style="position:relative; display:block;">

						<div class="mosaic-arrow arrow arrow-down"></div>
						<img src="${product.get_main_photo_url('big_')}" 
							 title="${product.name}" 
							 alt="${product.name}"
							 style="max-width:215px; margin:0px auto; margin-bottom:10px;">
					</a>
					</div>
				</div>
				<div class="in-tile-desc">
					${h.smart_truncate(product.description, 200)}
				</div>
			</div>
		</div>
	
	%endfor
</%def>

<%def name="chunk_of_products(products, title='', exchange_offers=False, force_width=None, distances=False)" filter="trim">
    <section class="newest">
        <div class="newest-products" style="${'width:%s%%'%(force_width) if force_width else ''}">
            %if not products:
                <i>Nic nie znaleziono :(</i>
            %endif

            %for p in products:
        
                <div class="tile">
                    <div class="pale-box" style="width:215; margin:0px auto;">
                        <div class="in-tile">
                            <div style="width:100%; text-align:left;">
                                <div style="padding:9px;">
                                    <a title="Pokaż w pełnej krasie" href="${p.get_sef_url()}">
                                        <span class="lobster" style="font-size:18px;">
                                            ${h.smart_truncate(p.name, 40)}
                                        </span>
                                    </a>
                                </div>
                            <a class="product-photo" title="${p.name}" href="${p.get_sef_url()}" style="position:relative; display:block;">
                                %if p.specifics:
                                    <div class="product-apla-opacity"></div>
                                    <div class="product-apla">
                                        <ul class="vertical-ul">
                                        %for s in p.get_specifics():
                                            <li title="${s.name.capitalize()}" class="icon s14-spec${s.id}"></li>
                                        %endfor
                                        <br />
                                        <span class="apla-distance">${"%.1f"%(p.distance)} km od Ciebie</span>
                                        </ul>
                                    </div>
                                %endif

                                <div class="mosaic-arrow arrow arrow-down"></div>
                                <img src="${p.get_main_photo_url('big_')}" 
                                     title="${p.name}" 
                                     alt="${p.name}"
                                     style="max-width:215px; margin:0px auto; margin-bottom:10px;">
                            </a>
                            </div>
                            %if not exchange_offers:
                                <div class="details">
                                    %if 'bez' not in p.until_when_available():
                                        <span class="bluish">${p.until_when_available()}</span> &bull;
                                    %endif
                                    %if p.price:
                                        <span class="bluish">${p.price}PLN / ${p.get_measure()}</span>
                                    %else:
                                        <span class="bluish">do wymiany</span>
                                    %endif
                                    &bull;
                                    <span class="bluish">zostało: ${p.quantity}</span>
                                </div>
                                <div class="in-tile-desc">
                                    ${h.smart_truncate(p.description, 200)}
                                </div>
                            %endif
                        </div>
                    </div>
                </div>
            %endfor
        </div>
        <div style="clear:both;"></div>
        %if not exchange_offers:
            ${shared.paginator(products)}
        %endif
    </section>
</%def>

<%def name="caphel(main, container, mains_as_title=False)" filter="trim">
    %for id, data in container.iteritems():
        <%
                href = request.route_path(routing or 'home_show_products', id=id, sef=h.make_sef_url(data['name']))
        %>
        <a href="${href}" class="mosaic">
            %for i, p in enumerate(data['products']):
                <div class="caphel caphel-${i+1}" style="background:url(${p.get_main_photo_url('small_')}) center no-repeat;"></div>
            %endfor
        %if i < 3:
            %for i in range(i+1,4):
                <div class="caphel caphel-${i+1}"></div>
            %endfor
        %endif
        <div class="counter bluish">${data['counter']}</div>
        <div class="mosiaic-title">
        %if mains_as_title:
            <span class="mains-as-title lobster">${data['name']}</span>
        %else:
            ${data['name']}
        %endif
        </div>
        <div class="mosaic-arrow2 arrow arrow-down"></div>
        </a>
    %endfor
</%def>

<%def name="mosaic(container, mains=None, coupled=[], profile=None, title='')" filter="trim">
    <section class="newest">
        <div class="newest-products">
            %if profile:
                <div class="mosaic" style="background-color:#cdeeff">
                <div class="mosiaic-title">&nbsp;</div>
                <div class="mosaic-avatar">
                    ${shared.avatar(profile, prefix='small_')}
                    <div class="lobster">${profile.user_name()}</div>
                    <div class="aside">
                    Sprzedaje: <strong>${profile.get_product_for_sales_count()}</strong> &bull;
                    Wymienia: <strong>${profile.get_product_for_exchange_count()}</strong>
                    </div>
                </div>
                </div>
            %endif
            %if mains:
                ${caphel(main, mains, mains_as_title=True)}
            %endif
            ${caphel(main, container)}
            <%
                truncate = 10 - len(container)
                if truncate < 0:
                    truncate = 0
            %>
            
            %for c in coupled[:truncate]:
                ${caphel(main, c)}
            %endfor
        </div>
    </section><br /><br /><br />
</%def>

<%def name="comments(p)" filter="trim">
    <a name="comments"></a>
    %for comment in p.comments.limit(15):
        <div class="user-comment comment-${'owner' if comment.is_owners(p) else 'regular'}">
        <div class="comment-details">${comment.details()}</div>
        ${comment.comment}<br />
        </div>
    %endfor
    %if not p.comments:
        <i>Nie ma jeszcze komentarzy</i><br />
    %endif
    %if req.user:
        <form id="comment-form" action="${request.route_path('save_comment', id=p.id)}">
            <textarea name="comment" class="comment-textarea"></textarea><br />
            <input type="submit" value="Komentuj" class="btn btn-primary lobster">
        </form>
    %endif
    %if not req.user:
        <i>Żeby dodać komentarz musisz się zalogować</i><br />
    %endif
</%def>

