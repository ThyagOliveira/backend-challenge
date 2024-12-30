from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookUploadView


router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path("", include(router.get_urls())),
    path('upload/', BookUploadView.as_view(), name='upload-books'),
]