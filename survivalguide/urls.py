from django.conf.urls import patterns, include, url
from views import HomePageView, LoginView, LogOutView, SignUpView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'surv ivalguide.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', HomePageView.as_view(), name='home'),
                       url(r'^accounts/register/$',
                           SignUpView.as_view(), name='signup'),
                       url(r'^accounts/login/$',
                           LoginView.as_view(), name='login'),
                       url(r'^accounts/logout/$',
                           LogOutView.as_view(), name='logout'),
                       url(r'^talks/',
                           include('talks.urls', namespace='talks')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
