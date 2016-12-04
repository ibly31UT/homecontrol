from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^layout$', views.LayoutView.as_view(), name='layout'),
    url(r'^control$', views.ControlView.as_view(), name='control'),
]
