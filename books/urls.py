from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views.books import BookViewSet, ReservationViewSet
from .views.authentication import LoginView


router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r"reservation", ReservationViewSet)

urlpatterns = [
    path("", include(router.get_urls())),
    path("login/", LoginView.as_view(), name="basic-login"),
]