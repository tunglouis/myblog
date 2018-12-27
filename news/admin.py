from django.contrib import admin
from django.db.models import Q #2
from django.utils.translation import ugettext_lazy as _
from .models import Categories, News #3

# Register your models here.
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'status', 'sort_order')
    search_fields = ['name', ]
    none_type = type(None)

    def get_form(self, request, obj=None, **kwargs):
        request.obj = obj

        if isinstance(obj, self.none_type) is True:
            self.exclude = ("sort_order", )
        else:
            self.exclude = None

        return super(CategoriesAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'parent_category':
            if not isinstance(request.obj, self.none_type):
                kwargs['queryset'] = Categories.objects.filter(~Q(
                    slug__exact=request.obj.slug), parent_category__isnull=True,
                                                               slug__exact=request.obj.slug)
            elif request.method == 'GET':
                kwargs['queryset'] = Categories.objects.filter(parent_category__isnull=True)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category', 'status')
    date_hierarchy = 'created_at' #1
    search_fields = ['title', 'categories__name']

    def get_category(self, obj): #2
        return obj.categories.name

    get_category.short_description = _('Categories') #3
    get_category.admin_order_field = 'category__name' #4

    list_filter = (
        ('categories', admin.RelatedFieldListFilter), #5
    )

    date_hierarchy = None #1

    def get_list_display(self, request):
        if News.objects.all().count() > 0: #2
            self.date_hierarchy = 'created_at'
        else:
            self.date_hierarchy = None

        return super(NewsAdmin, self).get_list_display(request)