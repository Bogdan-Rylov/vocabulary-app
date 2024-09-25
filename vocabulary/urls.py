from django.urls import path

from vocabulary.views import (
    home,
    WordListListView,
    WordListDetailView,
    WordListCreateView,
    WordListUpdateView,
    WordListDeleteView,
    AllWordsListView,
    WordListWordsListView,
    WordDetailView,
    WordCreateView,
    WordUpdateView,
    WordDeleteView,
)

app_name = "vocabulary"

urlpatterns = [
    path("", home, name="home"),
    path("word-lists/", WordListListView.as_view(), name="word-list-list"),
    path(
        "word-lists/<int:pk>/details/",
        WordListDetailView.as_view(),
        name="word-list-detail"
    ),
    path(
        "word-lists/create/",
        WordListCreateView.as_view(),
        name="word-list-create"
    ),
    path(
        "word-lists/<int:pk>/update/",
        WordListUpdateView.as_view(),
        name="word-list-update"
    ),
    path(
        "word-lists/<int:pk>/delete/",
        WordListDeleteView.as_view(),
        name="word-list-delete"
    ),

    path("all-words/", AllWordsListView.as_view(), name="all-words-list"),
    path(
        "all-words/<int:pk>/",
        WordDetailView.as_view(),
        name="word-detail-in-all"
    ),
    path(
        "all-words/create/",
        WordCreateView.as_view(),
        name="word-create-in-all"
    ),
    path(
        "all-words/<int:pk>/update/",
        WordUpdateView.as_view(),
        name="word-update-in-all"
    ),
    path(
        "all-words/<int:pk>/delete/",
        WordDeleteView.as_view(),
        name="word-delete-in-all"
    ),

    path(
        "word-lists/<int:word_list_pk>/words/",
        WordListWordsListView.as_view(),
        name="word-list-words-list"
    ),
    path(
        "word-lists/<int:word_list_pk>/words/<int:pk>/",
        WordDetailView.as_view(),
        name="word-detail-in-list"
    ),
    path(
        "word-lists/<int:word_list_pk>/words/create/",
        WordCreateView.as_view(),
        name="word-create-in-list"
    ),
    path(
        "word-lists/<int:word_list_pk>/words/<int:pk>/update/",
        WordUpdateView.as_view(),
        name="word-update-in-list"
    ),
    path(
        "word-lists/<int:word_list_pk>/words/<int:pk>/delete/",
        WordDeleteView.as_view(),
        name="word-delete-in-list"
    ),
]
