from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Course, Category
from .forms import CourseForm
from learn.models import CourseProgress, FavoritesCourses
from course_construct.utils import AuthorRequiredMixin


class CatalogView(ListView):
    model = Course
    template_name = "courses/list.html"
    context_object_name = "course_items"

    def get_queryset(self):
        queryset = super().get_queryset().filter(available=True)
        type_slugs = self.request.GET.getlist("category")
        search_query = self.request.GET.get("q")

        if type_slugs:
            queryset = queryset.filter(category__slug__in=type_slugs)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(category__name__icontains=search_query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["selected_categories"] = self.request.GET.getlist("category")

        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/detail_course.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            is_enrolled = CourseProgress.objects.filter(
                student=user, course=self.object
            ).exists()
            is_favorite = FavoritesCourses.objects.filter(
                student=user, course=self.object
            ).exists()
            context["is_enrolled"] = is_enrolled
            context["is_favorite"] = is_favorite
        else:
            context["is_enrolled"] = False
            context["is_favorite"] = False
        return context


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("construct:main", kwargs={"course_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class CourseDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Course
    template_name = "courses/confirm_delete.html"
    context_object_name = "course"
    success_url = reverse_lazy("users:profile")
