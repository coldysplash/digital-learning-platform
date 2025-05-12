from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include("courses.urls", namespace="courses")),
    path("users/", include("users.urls", namespace="users")),
    path("learn/", include("learn.urls", namespace="learn")),
    path("construct/", include("course_construct.urls", namespace="construct")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
