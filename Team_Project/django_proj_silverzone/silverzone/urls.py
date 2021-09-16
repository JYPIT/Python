from django.urls import path
from silverzone import views

urlpatterns = [
    path("main/", views.main_page, name="main_page"),
    path("main/qnas/", views.qna_list, name="qna_list"),
    path("main/qnas/post/", views.qna_post, name="qna_post"),
    path("main/qnas/<int:pk>/edit/", views.qna_edit, name="qna_edit"),
    path("main/qnas/<int:pk>/", views.qna_content, name="qna_content"),
    path("main/qnas/<int:qna_pk>/reviews/",
         views.review_list, name="review_list"),
    path("main/qnas/<int:qna_pk>/reviews/new/",
         views.review_new, name="review_new"),
    path("qnas/<int:qna_pk>/reviews/<int:pk>/edit/",
         views.review_edit, name="review_edit"),
    path("qnas/<int:qna_pk>/reviews/<int:pk>/delete/",
         views.review_delete, name="review_delete"),
    path("main/purpose/", views.purpose, name="purpose"),
    path("main/analysis/", views.analysis, name="analysis"),
    path("main/rank/", views.rank, name="rank"),
    path("main/recommend/", views.recommend, name="recommend"),
]
