# -*- coding: utf-8 -*
<%namespace name="shared" file="shared.mako" />
<%namespace name="modals" file="modals.mako" />
<%namespace name="ms" file="main_site.mako" />

<%def name="event_descripton_display(e)" filter="trim">
    <div class="newest">
    <div class="product-description-details">
        <h2 style="margin-top:0px; margin-bottom:2px; line-height:30px;">
            ${e.title}
        </h2>
        <p style="margin-top:10px;">${e.description}<p>
        <div class="social-icons-area">
        <div class="fb-like" data-href="http://www.foodel.pl${e.get_sef_url()}" data-layout="button" data-action="like" data-show-faces="true" data-share="true"></div>
        
        %if e.get_main_photo_object():
        <a href="http://www.pinterest.com/pin/create/button/?url=http://www.foodel.pl${e.get_sef_url()}&media=http://www.foodel.pl${e.get_main_photo_url('big_')}&description=${e.description}"
            data-pin-do="buttonPin"
            data-pin-config="none">
            <img src="//assets.pinterest.com/images/pidgets/pin_it_button.png" />
        </a>        
        %endif
        </div>
        
        <div class="entry" style="margin-top:10px;">
            <div class="icon sprite-05-details-owner"></div>
            <strong>Dodany przez: </strong>
            <a href="${e.user.profile_link(req)}">${e.user.user_name()}</a>
            <br />
        </div>
        %if e.localisation:
            <div class="entry">
                <div class="icon sprite-05-details-location"></div>
                <strong>Lokalizacja: </strong>
                <a target="_blank" href="https://maps.google.com/?q=${e.mlang},${e.mlong}&z=8">
                    %if e.street:
                        ${e.street},
                    %endif
                    ${e.localisation}
                </a>
                <br />
            </div>
        %endif
        %if e.event_starts:
            <div class="entry">
                <div class="icon sprite-05-details-location"></div>
                <strong>Data wydarzenia: </strong>
                ${e.event_starts.strftime('%d-%m-%Y')},
                ${h.get_hour_from_string(e.event_time)}
                <br />
            </div>
        %endif
        %if e.facebook_url:
            <div class="entry">
                <div class="icon sprite-05-details-location"></div>
                <a target="_blank" href="${e.facebook_url}">Kliknij tu żeby zobaczyć wydarzenie na Facebooku</a>
                <br />
            </div>
        %endif
        %if e.localisation and e.is_eligible_for_map():
        <div class="entry" style="margin-top:10px;">
            <div id="map-canvas"></div>
        </div><br />
        %endif
    </div>
    <div class="product-image-details">
        %if e.get_main_photo_object():
            <div class="main-photo">
                <a title="${e.title}" href="${e.get_main_photo_url('big_')}" class="cbox">
                <img class="photo-bluish-border"
                     src="${e.get_main_photo_url('big_')}" 
                     title="${e.title}" 
                     alt="${e.title}">
                </a>
            </div>
        %else:
            ${shared.no_photo_in_product_details()}
        %endif
        <div style="clear:both;"></div>
    </div>
    </div>
</%def>

<%def name="procuct_descripton_display(p, exchange_offers=[])" filter="trim">
    <div class="newest">
    <div class="product-description-details">
        <h2 style="margin-top:0px; margin-bottom:2px; line-height:30px;">
            ${p.name}
        </h2>
        
        %if p.specifics:
            <ul class="vertical-ul" style="margin:0px; text-align:left;">
            %for s in p.get_specifics():
                <li title="${s.name.capitalize()}" class="icon s14-spec${s.id}"></li>
            %endfor
            </ul>
        %endif
        
        <p style="margin-top:10px;">${p.description}<p>
        
        <div class="social-icons-area">
        <div class="fb-like" data-href="http://www.foodel.pl${p.get_sef_url()}" data-layout="button" data-action="like" data-show-faces="true" data-share="true"></div>
        
        %if p.get_main_photo_object():
        <a href="http://www.pinterest.com/pin/create/button/?url=http://www.foodel.pl${p.get_sef_url()}&media=http://www.foodel.pl${p.get_main_photo_url('big_')}&description=${p.description}"
            data-pin-do="buttonPin"
            data-pin-config="none">
            <img src="//assets.pinterest.com/images/pidgets/pin_it_button.png" />
        </a>        
        %endif
        </div>
        %if p.product_votes:
        <p style="margin-top:20px;">${shared.grade_hats(p.calculate_grades())}</p>
        %endif
        <div class="product-action-details">
        
        <div class="entry">
            <div class="icon sprite-05-details-owner"></div>
            <strong>Dodany przez: </strong>
            <a href="${p.user.profile_link(req)}">${p.owner_name()}</a>
            <br />
        </div>
        %if p.localisation:
            <div class="entry">
                <div class="icon sprite-05-details-location"></div>
                <strong>Lokalizacja: </strong>
                <a target="_blank" href="https://maps.google.com/?q=${p.mlang},${p.mlong}&z=8">${p.localisation}</a>
                <br />
            </div>
        %endif

        <div class="entry">
            <div class="icon sprite-05-details-price"></div>
            <strong>Sposób wymiany: </strong>${p.BARGAINS.get(p.bargain_type)}<br />
            %if p.price:
                <div class="icon sprite-05-details-price" style="visibility:hidden;"></div>
                <strong>Cena: </strong>${p.price} PLN / ${p.get_measure()}<br />
            %endif
        </div>
        <div class="entry">
            <div class="icon sprite-05-details-shipping"></div> 
            <strong>Sposób dostawy: </strong>${p.SHIPPINGS.get(p.shipping_method)}<br />
        </div>
        <div class="entry">
            <div class="icon sprite-05-details-availability"></div>
            <strong>Dostępność: </strong>${p.AVAILABILITIES.get(p.availability)}
            <br />
        </div>
        <div class="entry">
            <div class="icon sprite-05-details-availability"></div>
            <strong>Jednostka miary: </strong>${p.get_measure()}
            (zostało: ${p.quantity or 1})
            <br />
        </div>
        <div class="entry">
            <div class="icon sprite-05-details-availability"></div>
            <strong>Czas trwania oferty: </strong>${p.until_when_available()}
            <br />
        </div><br />
        %if p.localisation and p.is_eligible_for_map():
        <div class="entry">
            <div id="map-canvas"></div>
        </div><br />
        %endif
        
        %if not p.is_mine(req.user):
            %if req.user:
                ${modals.modal_send_message(p.owner_name(), p.user.id, p.id)}
                <a style="width:180px;" href="#" data-reveal-id="message-modal" data-animation="fade" class="lobster btn btn-large btn-primary regular-font" style="max-width:200px;">
            %else:
                ${modals.modal_login()}
                <a style="width:180px;" href="#" data-reveal-id="login-modal" data-animation="fade" class="lobster btn btn-large btn-primary regular-font log-in-popup" style="max-width:200px;">
            %endif
                Kontakt z ${p.owner_name()}</a>
            <div style="padding-top:5px;"></div>
            %if req.user:
                %if product.kind == product.BARGAIN_EXCHANGE:
                    ${modals.modal_exchange(p)}
                    <a style="width:180px;" href="#" data-reveal-id="exchange-modal" data-animation="fade" class="lobster btn btn-large btn-primary regular-font" style="max-width:200px;">
                %else:
                    ${modals.modal_buy(p)}
                    <a style="width:180px;" href="#" data-reveal-id="buy-modal" data-animation="fade" class="lobster btn btn-large btn-primary regular-font" style="max-width:200px;">
                %endif
            %else:
                ${modals.modal_login()}
                <a style="width:180px;" href="#" data-reveal-id="login-modal" data-animation="fade" class="lobster btn btn-large btn-primary regular-font log-in-popup" style="max-width:200px;">
            %endif
                Chcę to!</a>
        %endif
        </div>
    </div>
    <div class="product-image-details">
        %if p.get_main_photo_object():
            <div class="main-photo">
                <a title="${p.name}" href="${p.get_main_photo_url('big_')}" class="cbox">
                <img class="photo-bluish-border"
                     src="${p.get_main_photo_url('big_')}" 
                     title="${p.name}" 
                     alt="${p.name}">
                </a>
            </div>
        %else:
            ${shared.no_photo_in_product_details()}
        %endif
        <div style="clear:both;"></div>
        <div style="text-align:left;">
        <div style="display:inline-block; margin:0px auto;">
        %for i, photo in enumerate(p.get_aside_photo_objects()):
            <div class="product-aside-image-details">
                <a title="${p.name}" href="${photo.get_url('big_')}" class="cbox">
                <img class="photo-bluish-border"
                     src="${photo.get_url('small_')}" 
                     title="${p.name}" 
                     alt="${p.name}"
                     style="${'margin-right:5px;' if i == 0 else ''}">
                </a>
            </div>
        %endfor
        <div style="clear:both;"></div>
        </div>
        </div>
    </div>
    <div style="clear:both;"></div>
    <hr style="margin:0px;" />
    %if exchange_offers:
        <section class="product-offers">
            <h3 style="margin-top:0px;">Oferowane za ten produkt:</h3>
            ${ms.chunk_of_products(exchange_offers, exchange_offers=True, force_width=60)}
        </section>
        <section class="product-comments">
            <h3 style="margin-top:0px;">Pytamy, komentujemy, targujemy się :</h3>
            ${ms.comments(p)}
        </section>
        <div style="clear:both;"></div>
    %else:
        <section class="product-comments-alone">
            <h3 style="margin-top:0px;">Pytamy, komentujemy, targujemy się :</h3>
            ${ms.comments(p)}
        </section>
    %endif
    </div>
</%def>

<%def name="show_recommended(product)" filter="trim">
    %for p in product.recommended:
        <a title="${p.name}" href="${p.get_sef_url()}">
        <img class="photo-red-border"
             src="${p.get_main_photo_url('small_')}" 
             title="${p.name}" 
             alt="${p.name}"
             style="margin-top:10px;">
        </a>
    %endfor
</%def>
