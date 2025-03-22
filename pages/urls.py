from django.urls import path, re_path
from django.views import static
from django.conf import settings
from django.views.generic.base import RedirectView
from . import views

handler400 = views.bad_request
handler403 = views.forbidden
handler404 = views.not_found
handler500 = views.internal_server_error
handler502 = views.bad_gatway

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT }, name='static'),
    re_path(r'^favicon.ico$', RedirectView.as_view(url='static/pages/favicon.ico')),
    path('', views.index, name='index'),
    path('introduction/', views.introduction, name='introduction'),
    path('phira/', views.phira, name='phira'),
    path('phira/ranking/', views.prranking, name='prranking'),
    path('phira/getfile/', views.prgetfile, name='prgetfile'),
    path('phizone/', views.phizone, name='phizone'),
    path('phizone/ranking/', views.pzranking, name='pzranking'),
    path('phizone/vote/', views.pzvote, name='pzvote'),
    path('phizone/best/', views.pzbest, name='pzbest'),
    path('notanote', views.notanote, name='notanote'),
    path('notanote/best/', views.nanbest, name='nanbest'),
    path('notanote/rankcalc/', views.nanrankcalc, name='nanrankcalc'),
    path('randomnum/', views.random_num, name='randomnum'),
    path('diaries/', views.diaries_index, name='diaries_index'),
    re_path(r'^diaries/(?P<id>.+)/$', views.diaries, name='diaries'),
    path('programming/', views.programming_index, name='programming_index'),
    re_path(r'^programming/(?P<id>.+)/$', views.programming, name='programming'),
]