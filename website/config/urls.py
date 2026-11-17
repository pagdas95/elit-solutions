from django.urls import include, path

urlpatterns = [
    path("", include("web.urls")),
]

handler404 = "web.views.not_found"
