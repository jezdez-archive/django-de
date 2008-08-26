# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from tagging.models import Tag, TaggedItem
from tagging.fields import TagField

from django_de.apps.ticker import textutils

class EntryManager(models.Manager):
    def public(self):
        return self.filter(status=Entry.STATUS_OPEN)

class Entry(models.Model):

    STATUS_CLOSED = 0,
    STATUS_DRAFT = 1
    STATUS_OPEN = 2
    
    STATUS_CHOICES = (
        (STATUS_CLOSED, 'Geschlossen'),
        (STATUS_DRAFT, 'Vorlage'),
        (STATUS_OPEN, 'Veröffentlicht'),
    )
    objects = EntryManager()

    # Title and Slug
    title = models.CharField('Titel', max_length=255)
    slug = models.SlugField('Slug', blank=True)

    content = models.TextField('Inhalt')
    content_processed = models.TextField('Inhalt (geparsed)', blank=True)
    source_url = models.URLField('Quelle', blank=True)

    # Date Fields
    published = models.DateTimeField(_('Published'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    # Status Fields
    status = models.SmallIntegerField(_('Status'),
        choices=STATUS_CHOICES,
        default=STATUS_OPEN)

    # Related
    tags = TagField()
    author = models.ForeignKey(User)

    class Meta:
        ordering = ('-published',)
        permissions = (
            ('can_change_foreign', 'Can change foreign entry'),
            ('can_publish', 'Publish instantly'),
        )

    def get_author(self):
        return self.author.username

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def get_related(self):
        return TaggedItem.objects.get_related(self, Entry.objects.entries_by_user(request=None))

    def get_related_tags(self):
        return Tag.objects.related_for_model(self.tags, Entry)

    def get_next(self):
        return self.get_next_by_published(status=self.STATUS_OPEN)

    def get_prev(self):
        return self.get_previous_by_published(status=self.STATUS_OPEN)

    def __unicode__(self):
        return self.title

    def save(self):
        self.slug = slugify(self.title)
        self.content_processed = textutils.textfilter(self.content)
        super(Entry, self).save()

    @permalink
    def get_absolute_url(self):
        return ('ticker_details', (), {
            'id': str(self.id),
            'slug': self.slug,
        })

