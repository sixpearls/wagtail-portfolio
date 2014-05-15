#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache, cache_page
from django.views.decorators.http import require_http_methods

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from portfolio.models import Project, ProjectCategory

class PortfolioProjectDetail(DetailView):
    model = Project

    def get_object(self,queryset=None):
        self.category = get_object_or_404(ProjectCategory, slug=self.kwargs["category_slug"])
        return get_object_or_404(Project, slug=self.kwargs["project_slug"], category=self.category)


class PortfolioCategoryDetail(ListView):
    model = Project

    def get_queryset(self,*args,**kwargs):
        self.category = get_object_or_404(ProjectCategory, slug=self.kwargs["category_slug"])
        return Project.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PortfolioCategoryDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['category'] = self.category
        return context