from django.urls import path

from . import views

app_name = "construct"

# main and modules urls
urlpatterns = [
    path("course/<int:course_id>/", views.ConstructorCourseView.as_view(), name="main"),
    path(
        "course/<int:course_id>/module/create/",
        views.ModuleCreateView.as_view(),
        name="module_create",
    ),
    path("module/<int:pk>/", views.ModuleDetailView.as_view(), name="module"),
    path("module/<int:pk>/edit/", views.ModuleUpdateView.as_view(), name="module_edit"),
    path(
        "module/<int:pk>/delete/",
        views.module_delete,
        name="module_delete",
    ),
]

# lesson urls
urlpatterns += [
    path(
        "module/<int:module_id>/lesson/create/",
        views.LessonCreateView.as_view(),
        name="lesson_create",
    ),
    path("lesson/<int:pk>/", views.LessonDetailView.as_view(), name="lesson"),
    path("lesson/<int:pk>/edit/", views.LessonUpdateView.as_view(), name="lesson_edit"),
    path(
        "lesson/<int:pk>/delete/",
        views.lesson_delete,
        name="lesson_delete",
    ),
]

# lesson content urls
urlpatterns += [
    path(
        "lesson/<int:lesson_id>/content/text/create/",
        views.TextContentCreateView.as_view(),
        name="add_text",
    ),
    path(
        "lesson/<int:lesson_id>/content/file/create/",
        views.FileContentCreateView.as_view(),
        name="add_file",
    ),
    path(
        "lesson/<int:lesson_id>/content/link/create/",
        views.LinkContentCreateView.as_view(),
        name="add_link",
    ),
    path(
        "lesson/<int:lesson_id>/content/image/create/",
        views.ImageContentCreateView.as_view(),
        name="add_image",
    ),
    path(
        "lesson/<int:lesson_id>/content/<int:pk>/",
        views.ContentUpdateView.as_view(),
        name="content_edit",
    ),
    path(
        "lesson/<int:lesson_id>/content/<int:pk>/delete/",
        views.ContentDeleteView.as_view(),
        name="content_delete",
    ),
]

# test urls
urlpatterns += [
    path(
        "module/<int:module_id>/test/create/",
        views.TestCreateView.as_view(),
        name="test_create",
    ),
    path("test/<int:pk>/", views.TestDetailView.as_view(), name="test_detail"),
    path("test/<int:pk>/edit/", views.TestUpdateView.as_view(), name="test_edit"),
    path(
        "test/<int:pk>/delete/",
        views.test_delete,
        name="test_delete",
    ),
]

# questions ursl
urlpatterns += [
    path(
        "test/<int:test_id>/question/create/",
        views.QuestionCreateView.as_view(),
        name="add_question",
    ),
    path(
        "question/<int:pk>/detail/",
        views.QuestionDetailView.as_view(),
        name="question_detail",
    ),
    path(
        "question/<int:pk>/edit/",
        views.QuestionUpdateView.as_view(),
        name="question_edit",
    ),
    path(
        "question/<int:pk>/delete/",
        views.question_delete,
        name="question_delete",
    ),
]

# answers ursl
urlpatterns += [
    path(
        "question/<int:question_id>/answer/create",
        views.AnswerCreateView.as_view(),
        name="answer_create",
    ),
    path(
        "answer/<int:pk>/edit/",
        views.AnswerUpdateView.as_view(),
        name="answer_edit",
    ),
    path(
        "answer/<int:pk>/delete/",
        views.AnswerDeleteView.as_view(),
        name="answer_delete",
    ),
]
