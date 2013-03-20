from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('reviewboard.extensionbrowser.views',
    url(r'^$', 'browse_extensions', name="extensionbrowser"),
)
