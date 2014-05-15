#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from portfolio.views import wagtailadmin


urlpatterns = [
    url(r'^$', wagtailadmin.list_projects, name='portfolio_list_projects'), # pass in model
    url(r'^choose_category/$', wagtailadmin.choose_project_category, name='portfolio_choose_category'),
    url(r'^add/$', wagtailadmin.add_project, name='portfolio_add_project'),
    url(r'^(\d+)/$', wagtailadmin.edit_project, name='portfolio_edit_project'), 
    url(r'^(\d+)/delete/$', wagtailadmin.delete_project, name='portfolio_delete_project'),
]
