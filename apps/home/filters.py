import django_filters

from .models import CATEGARIAPRODUCTO

class ListingFilter(django_filters.FilterSet):

    class Meta:
        model = CATEGARIAPRODUCTO
        fields = ['CP_CDESCRIPCION']
