from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MasonWordsSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#     url(r'^show_words/(?P<category_id>\w+)', 'MasonWordsSite.views.get_words', name='get_words'),
    url(r'^postCognitiveTask/', 'MasonWordsSite.views.postCognitiveTask', name='postCognitiveTask'),
    url(r'^demographic/', RedirectView.as_view(url='/static/demographic.html')),
    url(r'^postDemographic', 'MasonWordsSite.views.postDemographic', name='postDemographic'),
    url(r'^get_words/', 'MasonWordsSite.views.get_words', name='get_words'),
    url(r'^getSelctionWords/(?P<categoryID>\w+)', 'MasonWordsSite.views.getSelctionWords', name='getSelctionWords'),
    url(r'^displaywords/', RedirectView.as_view(url='/static/displaywords.html')),
    url(r'^postDisplayWords', 'MasonWordsSite.views.postDisplayWords', name='postDisplayWords'),
    url(r'^questionnaire/', RedirectView.as_view(url='/static/questionnaire.html')),
    url(r'^questionnaire2/', RedirectView.as_view(url='/static/questionnaire2.html')),
    url(r'^game/', RedirectView.as_view(url='/static/game.html')),
    url(r'^postGame', 'MasonWordsSite.views.postGame', name='postGame'),
    url(r'^postRuminationTest', 'MasonWordsSite.views.postRuminationTest', name='postRuminationTest'),
    url(r'^save_fat', 'MasonWordsSite.views.save_fat', name='save_fat'),
    url(r'^feedback/', RedirectView.as_view(url='/static/feedback.html')),    
    url(r'^postFeedback', 'MasonWordsSite.views.postFeedback', name='postFeedback'),
    url(r'^goodbye/', RedirectView.as_view(url='/static/goodbye.html')),
    url(r'^duplicate_worker/', RedirectView.as_view(url='/static/sorry.html?type=dup')),
    url(r'^failed_math/', RedirectView.as_view(url='/static/sorry.html?type=math')),
    url(r'^error/', RedirectView.as_view(url='/static/sorry.html?type=error')),
    url(r'^get_uuid/', 'MasonWordsSite.views.get_uuid', name='get_uuid'),
    url(r'^logs/(?P<uuid>\w+)', 'MasonWordsSite.views.getLogs', name='getLogs'),
    url(r'^logs/', 'MasonWordsSite.views.getLogs', name='getLogs'),
    url(r'^get_summary/(?P<uuid>\w+)', 'MasonWordsSite.views.getWorkerSummary', name='getWorkerSummary'),
    url(r'^get_english_dict/', 'MasonWordsSite.views.getEnglishDict', name='getEnglishDict'),   
    url(r'^remarks', 'MasonWordsSite.views.getRemarks', name='getRemarks'),
    url(r'^admin/', include(admin.site.urls)),
)

