from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.events import BeforeRender

from sqlalchemy import engine_from_config

from .security import groupfinder

from .lib import helpers
from .lib.threads import start_all_threads

from .db import *


def add_renderer_globals(event):
    event['h'] = helpers


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(
        settings=settings,
        root_factory='.db.RootFactory',
        session_factory=UnencryptedCookieSessionFactoryConfig('kjsecret'))

    config.include('pyramid_mako')
    config.add_mako_renderer('.html')
    config.add_mako_renderer('.ajax')

    authn_policy = AuthTktAuthenticationPolicy(
        'so_secret',
        callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('static', 'kj:static', cache_max_age=3600)

    # ROUTING
    config.add_route('responsive', '/responsive')
    config.add_route('home', '/')
    config.add_route('home_add', '/dodaj')
    config.add_route('home_buy', '/kupie')
    config.add_route('home_change', '/zamienie')
    config.add_route('home_events', '/wydarzenia')
    config.add_route('home_event', '/wydarzenie/{id}/{sef}')
    config.add_route('home_show_subcategories', '/wszystkie/{id}/{sef}')
    config.add_route('home_buy_show_subcategories', '/kupie-wszystkie/{id}/{sef}')
    config.add_route('home_exchange_show_subcategories', '/zamienie-wszystkie/{id}/{sef}')
    config.add_route('home_show_products', '/produkty/{id}/{sef}')
    config.add_route('home_show_buy_products', '/kupie-produkty/{id}/{sef}')
    config.add_route('home_show_exchange_products', '/zamienie-produkty/{id}/{sef}')

    config.add_route('terms_and_conditions', '/regulamin')
    config.add_route('privacy_policy', '/polityka-prywatnosci')

    config.add_route('login', '/zaloguj')
    config.add_route('logout', '/wyloguj')
    config.add_route('fb_login', '/zaloguj-fb')
    config.add_route('fb_image', '/fb_image')
    config.add_route('register', '/zarejestruj')
    config.add_route('register_thanks', '/zarejestrowano-potwierdz')
    config.add_route('register_email_thanks', '/zarejestrowano')
    config.add_route('register_email_failed', '/blad-w-rejestracji')
    config.add_route('register_confirm', '/potwierdz/{id}/{md5}')
    config.add_route('registered_already', '/rejestracja-juz-taki-mamy')
    config.add_route('save_user', '/zapisz-uzytkownika')
    config.add_route('save_edited_user', '/zapisz-uzytkownika-po-edycji')

    config.add_route('profile_link', '/bazarek/{id}/{sef}')

    config.add_route('my_product_for_sale', '/moje-produkty-do-sprzedazy')
    config.add_route('my_product_for_exchange', '/moje-produkty-do-wymiany')

    config.add_route('show_product', '/produkt/{id}/{sef}')
    config.add_route('delete_product', '/usun-produkt/{id}/{user}')
    config.add_route('edit_product_for_sale', '/edytuj-produkt/{id}/{user}')
    config.add_route('save_product_for_sale', '/zapisz-produkt')

    config.add_route('add_sale', '/sprzedaje')
    config.add_route('add_exchange', '/zamieniam')
    config.add_route('save_edited_product_for_sale', '/zapisz-edytowany-produkt/{id}')

    config.add_route('delete_photo', '/usun-glowne-zdjecie/{id}')

    config.add_route('show_sale', '/kupie-zamienie')
    config.add_route('show_food', '/chce-jesc')
    config.add_route('show_lessons', '/ucze-sie')

    config.add_route('send_message', '/wyslij-wiadomosc/{user_id}/{product_id}')
    config.add_route('my_threads', '/moje-wiadomosci')
    config.add_route('inbox', '/moje-wiadomosci/przychodzace')
    config.add_route('outbox', '/moje-wiadomosci/wychodzace')
    config.add_route('archive', '/moje-wiadomosci/archiwalne')
    config.add_route('archive_message', '/moje-wiadomosci/archiwizuj/{id}')
    config.add_route('show_thread_messages', '/wiadomosc/{id}')
    config.add_route('reply', '/odpowiedz/{id}')

    config.add_route('buy', '/kup/{id}')
    config.add_route('exchange', '/wymien/{id}')
    config.add_route('save_comment', '/zapisz-komentarz/{id}')

    config.add_route('my_orders_sold', '/moja-sprzedarz/{kind}')
    config.add_route('my_orders_bought', '/moje-zakupy/{kind}')
    config.add_route('orders_for_grading', '/ocen')
    config.add_route('ajax_get_order_to_grade', '/ocen-order/{id}')
    config.add_route('save_grade', '/zapisz-ocene/{order_id}/{grade}')
    config.add_route('change_order_state', '/zmien-stan-zamowienia/{id}')
    config.add_route('transactions_apply_filter', '/t-filtr')

    config.add_route('my_events', '/moje-wydarzenia')
    config.add_route('add_event', '/dodaj-wydarzenie')
    config.add_route('save_event', '/zapisz-wydarzenie')
    config.add_route('save_edited_event', '/zapisz-wydarzenie-po-edycji/{id}')
    config.add_route('delete_event', '/usun-wydarzenie/{id}')
    config.add_route('edit_event', '/edytuj-wydarzenie/{id}')

    config.add_route('load_subcategories', '/doladuj-podkategorie/{id}')
    config.add_route('load_subcategories2', '/doladuj-podkategorie2/{id}')
    config.add_route('load_cities', '/doladuj-miasta/{id}')

    config.add_route('maps', '/mapa')

    config.add_route('search', '/szukaj')

    config.add_route('profile', '/profil/{id}/{sef}')

    config.add_route('forbidden', '/forbidden')

    config.add_route('pa_home', '/pa')
    config.add_route('pa_edit_me', '/edycja-szczegolow-profilu')

    config.add_route('category_coupling', '/secret-as21d2j')
    config.add_route('save_couple', '/zapisz-sparowane')
    config.add_route('load_couple', '/doladuj-sparowane/{id}')
    config.add_route('edit_couple', '/edytuj-sparowane/{id}')
    config.add_route('save_edited_couple', '/zapisz-wyedytowane-sparowane/{id}')
    config.add_route('leads', '/leads')
    config.add_route('save_lead', '/zapisz-lead')
    config.add_route('edit_lead', '/edytuj-lead/{id}')
    config.add_route('save_edited_lead', '/zapisz-edytowany-lead/{id}')
    config.add_route('delete_lead', '/usun-lead/{id}')

    config.set_request_factory(RequestWithUserAttribute)
    config.add_subscriber(add_renderer_globals, BeforeRender)

    config.scan()

    start_all_threads()

    return config.make_wsgi_app()
