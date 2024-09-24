from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView

from vocabulary.forms import WordSearchForm, WordListSearchForm
from vocabulary.models import Word, WordList


@login_required
def home(request: HttpRequest) -> HttpResponse:
    user = request.user

    user_words = Word.objects.filter(user=user).all()
    num_words = user_words.count()
    num_lists = WordList.objects.filter(user=user).count()

    week_ago = timezone.now() - timedelta(days=7)
    num_week_words = user_words.filter(date_added__lte=week_ago).count()

    context = {
        "words": num_words,
        "word_lists": num_lists,
        "num_week_words": num_week_words,
    }

    return render(
        request, "vocabulary/home.html", context=context
    )


class WordListListView(LoginRequiredMixin, ListView):
    model = WordList
    context_object_name = "word_list_list"
    template_name = "vocabulary/word_list_list.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = WordListSearchForm(
            initial={"title": title}
        )

        return context

    def get_queryset(self):
        user = self.request.user
        queryset = WordList.objects.filter(user=user).all()
        form = WordListSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])

        return queryset


class WordListDetailView(LoginRequiredMixin, DetailView):
    model = WordList
    template_name = "vocabulary/word_list_detail.html"


class WordListCreateView(LoginRequiredMixin, CreateView):
    model = WordList
    fields = ("title",)
    template_name = "vocabulary/word_list_form.html"
    success_url = reverse_lazy("vocabulary:word-list-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WordListUpdateView(LoginRequiredMixin, UpdateView):
    model = WordList
    fields = ("title",)
    success_url = reverse_lazy("vocabulary:word-list-list")


class WordListDeleteView(LoginRequiredMixin, DeleteView):
    model = WordList
    template_name = "vocabulary/word_list_confirm_delete.html"
    success_url = reverse_lazy("vocabulary:word-list-list")


class AllWordsListView(LoginRequiredMixin, ListView):
    model = Word
    context_object_name = "word_list"
    template_name = "vocabulary/all_words_list.html"
    paginate_by = 10

    # Check the code below ->

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        text = self.request.GET.get("text", "")
        context["search_form"] = WordSearchForm(
            initial={"text": text}
        )

        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Word.objects.filter(user=user).all()
        form = WordSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(text__icontains=form.cleaned_data["text"])

        return queryset


class WordListWordsListView(LoginRequiredMixin, ListView):
    model = Word
    context_object_name = "word_list_items"
    template_name = "vocabulary/word_list.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        word_list_pk = self.kwargs.get("list_pk")
        context["word_list"] = WordList.objects.get(id=word_list_pk)

        text = self.request.GET.get("text", "")
        context["search_form"] = WordSearchForm(
            initial={"text": text}
        )

        return context

    def get_queryset(self):
        word_list_pk = self.kwargs.get("list_pk")
        queryset = WordList.objects.get(id=word_list_pk).words.all()

        form = WordSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(text__icontains=form.cleaned_data["text"])

        return queryset


class WordDetailView(LoginRequiredMixin, DetailView):
    model = Word

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        word_list_pk = self.kwargs.get("list_pk")
        if word_list_pk:
            context["word_list_pk"] = word_list_pk

        text = self.request.GET.get("text", "")
        context["search_form"] = WordSearchForm(
            initial={"text": text}
        )

        return context


class WordCreateView(LoginRequiredMixin, CreateView):
    model = Word
    fields = ("part_of_speech", "text", "transcription")
    # Change success_url, use get_success_url() instead
    success_url = reverse_lazy("vocabulary:all-words-list")

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        word_list_pk = self.kwargs.get("list_pk")
        if word_list_pk:
            context["word_list_pk"] = word_list_pk

        text = self.request.GET.get("text", "")
        context["search_form"] = WordSearchForm(
            initial={"text": text}
        )

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WordUpdateView(LoginRequiredMixin, UpdateView):
    model = Word
    fields = "__all__"
    success_url = reverse_lazy("vocabulary:all-words-list")


class WordDeleteView(LoginRequiredMixin, DeleteView):
    model = Word
    success_url = reverse_lazy("vocabulary:all-words-list")
