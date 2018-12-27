from django.contrib.admin import RelatedFieldListFilter
from django.utils.translation import ugettext_lazy as _


class CategoryFilter(RelatedFieldListFilter):
    news_model = None

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__%s__exact' % (field_path, field.target_field.name)
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        super(CategoryFilter, self).__init__(field, request, params,
                                                model, model_admin,
                                                field_path)
        self.news_model = model

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None and not self.lookup_val_isnull,
            'query_string': changelist.get_query_string(
                {},
                [self.lookup_kwarg, self.lookup_kwarg_isnull]
            ),
            'display': _('All'),
        }

        for pk_val, val in self.lookup_choices:
            if self.news_model.objects.filter(categories=pk_val).count() > 0:
                yield {
                    'selected': self.lookup_val == str(pk_val),
                    'query_string': changelist.get_query_string({
                        self.lookup_kwarg: pk_val,
                    }, [self.lookup_kwarg_isnull]),
                    'display': val,
                }
