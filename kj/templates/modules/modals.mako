# -*- coding: utf-8 -*
<%namespace name="shared" file="shared.mako" />

<%def name="modal_exchange(product)" filter="trim">
    <div id="exchange-modal" class="reveal-modal" style="width:600px; margin-left:-325px;">
        <form id="exchange-form" action="${request.route_path('exchange', id=product.id)}" method="POST">
            <h2><span class="bluish lobster">Chcesz się wymienić na:</span> ${product.name}</h2>
            <div style="margin:0px 0px 10px 0px;">
                Sprzedający: ${product.owner_name()}
            </div>
            <div style="float:left; font-size:1.2em; color:#000; margin:4px 5px 0px 0px; display:none;">Ile chcesz tego wymienić?</div>
            <div style="float:left;">
                <select  name="quantity" id="quantity" autocomplete="off" style="width:70px;  display:none;">
                    %for i in xrange(product.quantity or 1):
                        <option value="${i+1}">${i+1}</option>
                    %endfor
                </select>
                <input id="product_for_exchange" type="hidden" name="product_for_exchange" value="" /> 
            </div>
            <div style="clear:both;"></div>
            <div style="font-size:1.2em; color:#000; margin-top:10px;">Wybierz przedmiot na który chcesz się wymienić:</div>
            <div class="exchange-content">
                %if logged_user_products:
                    %for user_product in logged_user_products:
                        <a id="${user_product.id}" href="#" class="exchange-a onconfirm" rel="Na pewno chcesz się wymienić na ${user_product.name}?">
                        ${shared.photo_in_product_list(user_product)}
                        ${h.smart_truncate(user_product.name, 50)}<br />
                        </a>
                    %endfor
                %else:
                    <br />
                    <span style="color:#cc0000;">Żeby się wymieniać musisz mieć przynajmniej jeden dodany produkt.</span>
                %endif
            </div>
        </form>
    </div>
</%def>

<%def name="modal_buy(product)" filter="trim">
    <div id="buy-modal" class="reveal-modal" style="width:600px; margin-left:-325px;">
        <form action="${request.route_path('buy', id=product.id)}" method="POST">
        <h2><span class="bluish lobster">Chcesz kupić:</span> ${product.name}</h2>
        <div style="margin:0px 0px 10px 0px;">
            Sprzedający: ${product.owner_name()}
        </div>
        <div style="float:left; font-size:1.2em; color:#000; margin:4px 5px 0px 0px;">Ile chcesz kupić?</div>
        <div style="float:left;">
            <select  name="quantity" id="quantity" autocomplete="off" style="width:70px;">
                %for i in xrange(product.quantity or 1):
                    <option value="${i+1}">${i+1}</option>
                %endfor
            </select>
            %if product.price:
                x <span id="price-tag">${product.price}</span> PLN
                <span id="unit-price-tag">${product.price}</span>
            %endif
            (${product.get_measure()})
        </div>
        <div style="clear:both;"></div>
        <div style="font-size:1.2em; color:#000; margin-top:10px;">Wiadomość do sprzedającego:</div>
        <div class="message-content">
            <textarea name="msg" style="height:100px;"></textarea>
            %if product.kind == product.BARGAIN_EXCHANGE:
                <input type="submit" value="Wymień się!" class="btn lobster btn-medium btn-primary regular-font" />
            %else:
                <input type="submit" value="Kup!" class="btn lobster btn-medium btn-primary regular-font" />
            %endif
        </div>
        </form>
    </div>
</%def>

<%def name="cookies()" filter="trim">
	<div id="cookies-modal" class="reveal-modal" style="width:580px; margin-left:-325px; font-size:0.8em;">
		Drogi Użytkowniku, w ramach naszej strony stosujemy pliki cookies.
		Ich celem jest świadczenie usług na najwyższym poziomie,
		w tym również dostosowanych do Twoich indywidualnych potrzeb.
		Korzystanie z witryny bez zmiany ustawień przeglądarki dotyczących cookies oznacza,
		że będą one umieszczane w Twoim urządzeniu. W każdej chwili możesz dokonać zmiany ustawień przeglądarki
		dotyczących cookies - więcej informacji na ten temat znajdziesz w polityce prywatności.<br />
		<div style="width:100%; text-align:center; margin:0px auto; margin-top:10px; margin-bottom:20px;">
		<a href="#" id="cookies-accept" class="close-modal btn btn-small btn-primary">Rozumiem i akceptuję</a>
		</div>
	</div>
</%def>


<%def name="modal_login()" filter="trim">
    <div id="login-modal" class="reveal-modal" style="width:580px; margin-left:-325px;">
        <div class="login-box" style="border:none !important;">
        <h2>Zaloguj sie</h2>
        <form action="${request.route_path('login')}" method="POST">
            <input type="hidden" name="from_modal" value="1" />
            <div class="fleft input-label">Twój e-mail:</div>
            <div class="fleft input-field"><input type="email" name="email" id="email" /></div>
            <div style="clear:both;"></div>
            <div class="fleft input-label">Hasło:</div>
            <div class="fleft input-field"><input type="password" name="password" id="password" /></div>
            <div style="clear:both;"></div>
            <div style="margin:5px 0px 10px 0px; text-align:center; width:100%;">
                <input name="form.submitted" style="width:80px;" class="btn btn-primary btn-medium" type="submit" value="ZALOGUJ" />
            </div>
            <div style="text-align:center; width:100%; font-size:0.8em;">
                <a href="${request.route_path('register')}">Zarejestruj nowe konto</a>
                &nbsp;&nbsp;::&nbsp;&nbsp;
                <a href="#">Przypomnij mi hasło</a>
            </div>
        </form>
        </div>
        <div class="login-box" style="border:none !important;">
        <h2>..albo użyj Facebook'a</h2>
        <div style="width:100%; text-align:center; margin-top:25px;">
        <a href="#" class="icon s15-fb-login" onclick="fb_login()" title="zaluguj przez Facebook"></a>
        </div>
        </div>
        <div style="clear:both;"></div>
    </div>
</%def>

<%def name="modal_send_message(username, user_id, product_id)" filter="trim">
    <div id="message-modal" class="reveal-modal" style="width:600px; margin-left:-325px;">
        <form action="${request.route_path('send_message', user_id=user_id, product_id=product_id)}" method="POST">
        <h2>Napisz wiadmosc do ${username}</h2>
        <div class="message-content">
            <textarea name="msg"></textarea>
            <input type="submit" value="Wyślij wiadomość" class="btn btn-medium btn-primary regular-font" />
        </div>
        </form>
    </div>
</%def>

<%def name="grade_product()" filter="trim">
    <div id="grade-modal" class="reveal-modal" style="width:350px; padding:20px;"></div>
</%def>
