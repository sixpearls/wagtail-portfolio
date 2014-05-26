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

class ProjectImage(Orderable):
    project = ParentalKey('portfolio.Project',related_name='images')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,related_name='+')
    caption = RichTextField(blank=True)

    def __unicode__(self):
        return self.project.__unicode__() + u'\'s ' + self.image.__unicode__() + u' image'

    panels = [
        ImageChooserPanel('image'),
    ]

class PortfolioMetaFieldKey(models.Model):
    text = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "MetaField Keys"

    def __unicode__(self):
        return self.text

register_snippet(PortfolioMetaFieldKey)

class ProjectCategoryMetaFieldDefaultKeys(Orderable):
    category = ParentalKey('portfolio.ProjectCategory',related_name='default_metafields')
    key = models.ForeignKey(PortfolioMetaFieldKey,related_name="default_to")

    class Meta:
        verbose_name_plural = "Portfolio Default MetaKeys"

    def __unicode__(self):
        return self.category.__unicode__() + u'\'s default key ' + self.key.__unicode__()

    panels=[
        SnippetChooserPanel('key', PortfolioMetaFieldKey),
    ]

class ProjectMetaField(Orderable):
    key = models.ForeignKey(PortfolioMetaFieldKey)
    value = models.CharField(max_length=255)
    project = ParentalKey('portfolio.Project',related_name='metafields')

    def __unicode__(self):
        return self.project.__unicode__() + u'\'s ' + self.key.__unicode__() + u': ' + self.value

class Project(Page):
    description = RichTextField(blank=True)

    indexed_fields = ('description', ) 
    # possibly "metafields.list('values')" (a callable to return list of values)
    # or create some other Project function -- look at how wagtail does tag indexing

    def __init__(self, *args, **kwargs):
        parent = kwargs.pop('parent',None)
        super(Project, self).__init__(*args, **kwargs)
        if parent is not None:
            self.metafields = [ ProjectMetaField(key=metafieldkey) \
            for metafieldkey in \
            PortfolioMetaFieldKey.objects.filter(default_to__category=parent).order_by('default_to__sort_order') ]


Project.content_panels = Page.content_panels + [
    FieldPanel('description'),
    InlinePanel(Project, 'metafields', label="MetaFields"),
    InlinePanel(Project, 'images', label="Images"),
]

class ProjectCategory(Page):
    class Meta:
        verbose_name_plural = 'Portfolio Categories'

    subpage_types = ['portfolio.Project']

ProjectCategory.content_panels = Page.content_panels + [
    InlinePanel(ProjectCategory, 'default_metafields', label="Default MetaFields"),
]

class ProjectCategoryIndex(Page):
    subpage_types = ['portfolio.ProjectCategory']
    template = "portfolio/index.html"