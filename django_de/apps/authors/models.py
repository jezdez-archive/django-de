﻿from django.db import models
from django.utils.translation import ugettext_lazy as _

class Author(models.Model):
    name = models.CharField(_('name'), core=True, max_length=50, unique=True)
    slug = models.SlugField(_('slug'), prepopulate_from=('name',), help_text=_('for direct access on an author\'s page'))
    email = models.EmailField(_('email adress'))
    url = models.URLField(_('personal website'), null=True, blank=True, verify_exists=False)
    bio = models.TextField(_('bio'), help_text=_('HTML please, optional'), null=True, blank=True)

    class Admin:
        list_display = ('name', 'email', 'url')
        search_fields = ('name', 'bio')

    class Meta:
        verbose_name = _('Author')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/author/#%s' % (self.slug)