from dal_select2.views import Select2QuerySetView
from duals.models import schools
from post.models import *
class schoolsAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return schools.objects.none()

        qs = schools.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
class position_categoryAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return position_category.objects.none()

        qs = position_category.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs