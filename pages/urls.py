from django.urls import path, re_path
from django.views import static
from django.conf import settings
from django.views.generic.base import RedirectView
from . import views

handler400 = views.bad_request
handler403 = views.forbidden
handler404 = views.not_found
handler500 = views.internal_server_error
handler502 = views.bad_gateway

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT }, name='static'),
    re_path(r'^favicon.ico$', RedirectView.as_view(url='static/pages/favicon.ico')),
    path('', views.index, name='index'),
    path('changelog/', views.changelog, name='changelog'),
    path('introduction/', views.introduction, name='introduction'),
    path('special_thanks/', views.special_thanks, name='special_thanks'),
    path('fanmade_charts/', views.fanmade_charts, name='fanmade_charts'),
    path('fanmade_charts/phigros/', views.fanmade_charts_phigros, name='fanmade_charts_phigros'),
    path('phira/', views.phira, name='phira'),
    path('phira/ranking/', views.phira_ranking, name='phira_ranking'),
    path('phira/getfile/', views.phira_download, name='phira_download'),
    path('phizone/', views.phizone, name='phizone'),
    path('phizone/ranking/', views.phizone_ranking, name='phizone_ranking'),
    path('phizone/vote/', views.phizone_vote, name='phizone_vote'),
    path('phizone/best/', views.phizone_best, name='phizone_best'),
    path('notanote', views.notanote, name='notanote'),
    path('notanote/best/', views.notanote_best, name='notanote_best'),
    path('notanote/best/instruction/', views.notanote_best_instruction, name='notanote_best_instruction'),
    path('notanote/rank/', views.notanote_rank, name='notanote_rank'),
    path('notanote/pcdownload/', views.notanote_pcdownload, name='notanote_pcdownload'),
    path('programming/', views.programming_index, name='programming_index'),
    re_path(r'^programming/(?P<id>\d+)/$', views.programming, name='programming'),
    path('randomnum/', views.randomnum, name='randomnum'),
    path('posts/', views.posts_index, name='posts_index'),
    re_path(r'^posts/(?P<id>\d+)/$', views.posts, name='posts'),
]
