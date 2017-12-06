from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^addphoto/$', views.addphoto, name='addphoto'),
	url(r'^members/$', views.ProfileListView.as_view(), name='members'),
	url(r'^(?P<pk>\d+)$', views.ProfileDetail, name='member-detail'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^search/$', views.searchBar, name='search'),
	url(r'^imageClick/$', views.imageClick, name='imageClick'),
	url(r'^addComment/$', views.addComment, name = 'addComment')
]