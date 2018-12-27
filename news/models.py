from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.text import slugify
from datetime import date

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=254, verbose_name=_('name'))
    slug = models.SlugField(max_length=254, unique=True, blank=True, editable=True)
    parent_category = models.ForeignKey("self", verbose_name=_('Parent category'),
                                        null=True, blank=True,
                                        on_delete=models.CASCADE) #1
    sort_order = models.PositiveSmallIntegerField(default=10, verbose_name=_('Sort order'))
    status = models.BooleanField(default=0, verbose_name=_('Status'))

    def __str__(self):
        return self.name

    @staticmethod
    def extra_filters(obj): #2
        if not obj.parent_category:
            return {'parent_category__isnull': True}
        return {'parent_category': obj.parent_category}

    def save(self, *args, **kwargs): #3
        self.slug = slugify(self.name) #4
        if self.parent_category_id is not None: #5
            Categories.objects.filter(parent_category=self.id).update(parent_category=None)

        if not self.id: #6
            try:
                filters = self.__class__.extra_filters(self)
                self.sort_order = self.__class__.objects.filter(
                    **filters
                ).order_by("-sort_order")[0].sort_order + 10
            except IndexError:
                self.sort_order = 0

        super(Categories, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['sort_order']
class News(models.Model):
    categories = models.ForeignKey(Categories, null=True, verbose_name=_('Category'),
                                   on_delete=models.CASCADE)
    title = models.CharField(max_length=254, verbose_name=_('name'))
    slug = models.SlugField(max_length=254, unique=True, blank=True, editable=True)
    short_description = models.TextField(verbose_name=_('Short description'))
    description = models.TextField(verbose_name=_('Description'))
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    publish_at = models.DateTimeField(verbose_name=_('Publish at'),)
    upload_to = 'img/news/{0}/{1}'.format(date.today().year, date.today().month)
    feature_img = models.ImageField(upload_to=upload_to, blank=True, null=True, max_length=254,
                                      verbose_name=_('Feature Image'))
    status = models.BooleanField(default=0, verbose_name=_('Status'))
    views_count = models.IntegerField(default=0, verbose_name=_('Views count'))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
        ordering = ['-publish_at']
        get_latest_by = 'created_at'