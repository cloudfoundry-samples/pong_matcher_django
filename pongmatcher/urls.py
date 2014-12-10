from django.conf.urls import url
from pongmatcher import views

urlpatterns = [
        url(r'^all', views.wipe),
        url(r'^match_requests$', views.match_request_list),
        url(r'^match_requests/([\w-]+)$', views.match_request_detail),
        url(r'^matches/([\w-]+)$', views.match_detail),
        url(r'^results$', views.result_list),
        ]
