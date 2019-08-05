from django.urls import path
from ERP.core import views as v

app_name = 'core'

urlpatterns = [
    path('', v.index, name='index'),
    ]
