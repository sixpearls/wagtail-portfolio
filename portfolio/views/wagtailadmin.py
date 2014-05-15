#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache, cache_page
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required

from django.core.urlresolvers import reverse

from wagtail.wagtailsnippets.models import get_snippet_content_types
from wagtail.wagtailsnippets.permissions import user_can_edit_snippet_type

from wagtail.wagtailsnippets.views import snippets
from wagtail.wagtailsnippets.views.snippets import get_snippet_type_name, get_snippet_type_description, \
                                                get_content_type_from_url_params, get_snippet_edit_handler

from django.contrib.contenttypes.models import ContentType

from portfolio.models import Project, ProjectCategory, MetaFieldKey, ProjectMetaFieldValue

def list_projects(request):
    return snippets.list(request, 'portfolio', 'project')

def edit_project(request,pk):
    return snippets.edit(request, 'portfolio', 'project', pk)

def delete_project(request,pk):
    return snippets.delete(request, 'portfolio', 'project', pk)

@permission_required('wagtailadmin.access_admin')
def choose_project_category(request):
    content_type = ContentType.objects.get_for_model(Project)
    if not user_can_edit_snippet_type(request.user, content_type):
        raise PermissionDenied

    return render(request, 'portfolio/project/choose_category.html', {
        'categories': ProjectCategory.objects.all(),
    })

@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def add_project(request):
    content_type = ContentType.objects.get_for_model(Project)
    if not user_can_edit_snippet_type(request.user, content_type):
        raise PermissionDenied

    snippet_type_name = get_snippet_type_name(content_type)[0]

    print "get: ", request.GET

    if 'category_id' not in request.GET:
        return HttpResponseRedirect(reverse('portfolio_choose_category'))

    model = Project
    
    category = ProjectCategory.objects.get(pk=request.GET['category_id'])
    instance = Project(category=category)
    instance.metafields = [ ProjectMetaFieldValue(key=metafieldkey) \
        for metafieldkey in \
        MetaFieldKey.objects.filter(pk__in=category.default_metafields.all().values_list('key',flat=True)) ]

    # IMPROVE: Had to copy and paste to recreate functionality. Everything from
    # here down is from wagtail/wagtailsnippets/views/snippets.py `create` func
    # above is only a slight modification. Each step should be a view mixin / func
    edit_handler_class = get_snippet_edit_handler(model)
    form_class = edit_handler_class.get_form_class(model)

    if request.POST:
        form = form_class(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                _("{snippet_type} '{instance}' created.").format(
                    snippet_type=capfirst(get_snippet_type_name(content_type)[0]), 
                    instance=instance
                )
            )
            return redirect('wagtailsnippets_list', content_type.app_label, content_type.model)
        else:
            messages.error(request, _("The snippet could not be created due to errors."))
            edit_handler = edit_handler_class(instance=instance, form=form)
    else:
        form = form_class(instance=instance)
        edit_handler = edit_handler_class(instance=instance, form=form)

    return render(request, 'wagtailsnippets/snippets/create.html', {
        'content_type': content_type,
        'snippet_type_name': snippet_type_name,
        'edit_handler': edit_handler,
    })