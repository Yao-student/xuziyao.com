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
    path('fanmade_charts/', views.fmcharts, name='fmcharts'),
    re_path(r'^fanmade_charts/(?P<category>\w+)/(?P<id>\d+)/$', views.fmcharts_download, name='fmcharts_download'),
    path('fanmade_charts/phigros/', views.fmchartsphi, name='fmchartsphi'),
    path('phira/', views.phira, name='phira'),
    path('phira/ranking/', views.prranking, name='prranking'),
    path('phira/getfile/', views.prgetfile, name='prgetfile'),
    path('phizone/', views.phizone, name='phizone'),
    path('phizone/ranking/', views.pzranking, name='pzranking'),
    path('phizone/vote/', views.pzvote, name='pzvote'),
    path('phizone/best/', views.pzbest, name='pzbest'),
    path('notanote', views.notanote, name='notanote'),
    path('notanote/best/', views.nanbest, name='nanbest'),
    path('notanote/best/v1.7.0', views.nanbest_v1_7_0, name='nanbest_v1.7.0'),
    path('notanote/rankcalc/', views.nanrankcalc, name='nanrankcalc'),
    path('notanote/rankcalc/v1.7.0', views.nanrankcalc_v1_7_0, name='nanrankcalc_v1.7.0'),
    path('programming/', views.programming_index, name='programming_index'),
    re_path(r'^programming/(?P<id>\d+)/$', views.programming, name='programming'),
    path('randomnum/', views.randomnum, name='randomnum'),
    path('posts/', views.posts_index, name='posts_index'),
    re_path(r'^posts/(?P<id>\d+)/$', views.posts, name='posts'),
]
