from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.views.generic import simple
# from  news_and_events.views import NewsAndEventsViews

urlpatterns = patterns('',
    
    # news and events items
    (r"^(?P<slug>[-\w]+)/$", 'projects.views.project'),
    # (r'^projects/page(?P<page>[0-9]+)/$', list_detail.object_list, {'template_object_name': 'project'}),
    url(r'^', simple.direct_to_template, {'template': 'projects/filter.html'}, name='projects-filter')
    # url(r'^(?P<entity>)/$', projects_by_entity, name='projects-by-entity')
