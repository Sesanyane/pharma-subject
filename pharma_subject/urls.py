from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import pharma_subject_admin

app_name = 'pharma_subject'

urlpatterns = [
    path('admin/', pharma_subject_admin.urls),
    path('', RedirectView.as_view(url='admin/'), name='home_url'),
]
