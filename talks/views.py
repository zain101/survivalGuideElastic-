from __future__ import absolute_import
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.views import generic
from django.db.models import Count
from datetime import date
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet, AutoQuery
from django.template.defaultfilters import slugify

from braces import views
from . import models
from . import forms
import simplejson as json

tmp = 1


def autocomplete(request):
    sqs = SearchQuerySet().filter(content=AutoQuery(request.GET.get('q', '')))
    suggestion = sqs.spelling_suggestion()
    print "Correction: ", suggestion
    sqs = SearchQuerySet().autocomplete(content_auto=suggestion)
    # suggestion = models.Note.objects.get(slug=slugify(suggestion))
    # print "Slug: ", suggestion
    # sqs = SearchQuerySet().more_like_this(suggestion)
    print "sqs: ", sqs
    suggestions = []
    #suggestions = [result.title for result in sqs]
    for i in sqs:
        print i.object.title, i
        suggestions.append(i.object.title)
    print "suggestions: ", suggestions
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')


class MyAutoSearchView(generic.TemplateView):
    template_name = "talks/search_auto.html"


class MySearchView(SearchView):
    """My custom search view."""
    template_name = "talks/search.html"
    form_class = forms.DateRangeSearchForm
    model = models.Note
    context_object_name = 'Note'

    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        # further filter queryset based on some set of criteria
        tmp = queryset#queryset.filter(pub_date__gte=date(2015, 1, 1))
        print "QuerySet: ", tmp
        return queryset

    # if results.query.backend.include_spelling:
    # context['suggestion'] = forms.get_suggestion()

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        # do something
        print "Context: ", context
        return context


class RestrictToUserMixin(object):

    def get_queryset(self):
        queryset = super(RestrictToUserMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class TalkListListView(
    views.LoginRequiredMixin,
    RestrictToUserMixin,
    generic.ListView
):
    model = models.TalkList

    def get_queryset(self):
        queryset = super(TalkListListView, self).get_queryset()
        queryset = queryset.annotate(talk_count=Count('talks'))
        return queryset


class TalkListDetailView(
        views.LoginRequiredMixin,
        RestrictToUserMixin,
        generic.DetailView
):
    form_class = forms.TalkForm
    model = models.TalkList
    http_method_names = ['get', 'post']
    model = models.TalkList
    prefetch_related = ('talks', )

    def get_context_data(self, **kwargs):
        context = super(TalkListDetailView, self).get_context_data(**kwargs)
        context.update({'form': self.form_class(self.request.POST or None)})
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = self.get_object()
            talk = form.save(commit=False)
            talk.talk_list = obj
            talk.save()
        else:
            return self.get(request, *args, **kwargs)
        return redirect(obj)

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse('A talk List')

    # def get_queryset(self):
    #     queryset = super(TalkListDetailView, self).get_queryset()
    #     queryset = queryset.filter(user=self.request.user)
    #     return queryset


class TalkListCreateView(
    views.LoginRequiredMixin,
    views.SetHeadlineMixin,
    generic.CreateView
):
    form_class = forms.TalkListForm
    headline = 'Create'
    model = models.TalkList

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TalkListCreateView, self).form_valid(form)


class TalkListUpdateView(
        RestrictToUserMixin,
        views.LoginRequiredMixin,
        views.SetHeadlineMixin,
        generic.UpdateView
):
    form_class = forms.TalkListForm
    headline = 'Update'
    model = models.TalkList


class TalkListRemoveTalkView(
    views.LoginRequiredMixin,
    generic.RedirectView
):

    model = models.Talk

    def get_redirect_url(self, *args, **kwargs):
        return self.talklist.get_absolute_url()

    def get_object(self, pk, talklist_pk):
        try:
            talk = self.model.objects.get(
                pk=pk,
                talk_list_id=talklist_pk,
                talk_list__user=self.request.user
            )
        except models.Talk.DoesNotExist:
            raise Http404
        else:
            return talk

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            kwargs.get('pk'), kwargs.get('talklist_pk'))
        self.talklist = self.object.talk_list
        messages.success(
            request,
            u'{0.name} was removed from {1.name}'.format(
                self.object, self.talklist)
        )
        self.object.delete()
        return super(TalkListRemoveTalkView, self).get(request, *args, **kwargs)


class TalkListScheduleView(
    RestrictToUserMixin,
    views.PrefetchRelatedMixin,
    generic.DetailView
):
    model = models.TalkList
    prefetch_related = ('talks',)
    template_name = 'talks/schedule.html'


def myAjaxView(request):
    tmp = tmp + 1
    return HttpResponse()
