from django.views.generic import ListView, DetailView
from .models import Course, Category
from django.db.models import Q


class CatalogView(ListView):
    model = Course
    template_name = "courses/list.html"
    context_object_name = "course_items"

    def get_queryset(self):
        queryset = super().get_queryset()
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
        return context
