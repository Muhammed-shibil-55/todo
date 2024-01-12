from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("todos",views.TodosView,basename="todos")

urlpatterns=[
    path("register/",views.SignUpView.as_view()),
]+router.urls