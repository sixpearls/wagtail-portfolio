#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from portfolio.views.projects import PortfolioProjectDetail, PortfolioCategoryDetail


urlpatterns = patterns('',
    url(r'^(?P<category_slug>[-\w/]+)/(?P<project_slug>[\w\.-]+)/$', PortfolioProjectDetail.as_view(), name='portfolio_project_detail'),
    url(r'^(?P<category_slug>[-\w/]+)/$', PortfolioCategoryDetail.as_view(), name='portfolio_category_detail'),
)