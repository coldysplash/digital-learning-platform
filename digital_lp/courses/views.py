from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Course, Category
from learn.models import CourseProgress, FavoritesCourses


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
