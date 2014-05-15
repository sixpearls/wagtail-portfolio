from django.conf import settings
from django.conf.urls import include, url
from django.core import urlresolvers
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin import hooks
from wagtail.wagtailadmin.menu import MenuItem

from portfolio.urls import wagtailadmin as wagtailadmin_urls

# IMPROVE: too much boilerplate here? maybe neceesary

def register_admin_urls():
    return [
        url(r'^portfolio/', include(wagtailadmin_urls)),
    ]
hooks.register('register_admin_urls', register_admin_urls)

def construct_main_menu(request, menu_items):
    # if request.user.has_perm('wagtailimages.add_image'): # FIX PERMISSION CHECK

    menu_items.append(
        MenuItem(_('Portfolio'), 
        urlresolvers.reverse('portfolio_list_projects'), 
        classnames='icon icon-image',
        order=550)
    )

    menu_items.append(
        MenuItem(_('--Categories'), 
        urlresolvers.reverse('wagtailsnippets_list',args=('portfolio','projectcategory',)), 
        classnames='icon icon-cog',
        order=550)
    )

    menu_items.append(
        MenuItem(_('--MetaKeys'), 
        urlresolvers.reverse('wagtailsnippets_list',args=('portfolio','metafieldkey',)), 
        classnames='icon icon-redirect',
        order=550)
    )

hooks.register('construct_main_menu', construct_main_menu)
