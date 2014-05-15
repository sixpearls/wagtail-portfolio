#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings as site_settings
from django.utils.translation import ugettext, ugettext_lazy as _

from portfolio import settings

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from categories.models import CategoryBase

class PortfolioImage(Orderable):
    project = ParentalKey('portfolio.Project',related_name='images')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
    ]

class MetaFieldKey(models.Model):
    text = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "MetaField Keys"

    def __unicode__(self):
        return self.text

register_snippet(MetaFieldKey)

class MetaFieldDefaultKeys(Orderable):
    category = ParentalKey('portfolio.ProjectCategory',related_name='default_metafields')
    key = models.ForeignKey(MetaFieldKey)

    class Meta:
        verbose_name_plural = "Portfolio Default MetaKeys"

    panels=[
        SnippetChooserPanel('key', MetaFieldKey),
    ]

class ProjectCategory(CategoryBase):
    class Meta:
        verbose_name_plural = 'Portfolio Categories'

    def get_absolute_url(self):
        slug = '/'.join(self.get_ancestors(include_self=True).values_list('slug',flat=True))
        return reverse('portfolio_category_detail', args=(), kwargs={
            'category_slug': slug,
        })

ProjectCategory.panels = [
    FieldPanel('parent'),
    FieldPanel('name'),
    FieldPanel('slug'),
    FieldPanel('active'),
    InlinePanel(ProjectCategory, 'default_metafields', label="Default MetaFields"),
]
register_snippet(ProjectCategory)

class ProjectMetaFieldValue(Orderable):
    key = models.ForeignKey(MetaFieldKey)
    value = models.CharField(max_length=255)
    project = ParentalKey('portfolio.Project',related_name='metafields')

class Project(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)
    description = RichTextField(blank=True)

    category = models.ForeignKey(ProjectCategory)

    indexed_fields = ('description', ) 
    # possibly "metafields.list('values')" (a callable to return list of values)
    # or create some other Project function -- look at how wagtail does tag indexing

    def __unicode__(self):
        return self.title or u'untitled project'

    def get_absolute_url(self):
        return reverse('portfolio_project_detail', args=(), kwargs={ # ('PortfolioProjectDetail.as_view', (), {
            'category_slug': '/'.join(self.category.get_ancestors(include_self=True).values_list('slug',flat=True)),
            'project_slug': self.slug
        })

Project.panels = [
    FieldPanel('title'),
    FieldPanel('slug'),
    FieldPanel('description'),
    FieldPanel('category'),
    InlinePanel(Project, 'metafields', label="MetaFields"),
    InlinePanel(Project, 'images', label="Images"),
]

register_snippet(Project)