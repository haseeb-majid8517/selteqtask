from django.urls import path, include
from rest_framework.routers import SimpleRouter
from selteq_task.users.views import *
router = SimpleRouter()
router.register("users", SignUpViewSet, basename="users")
router.register("tasks", TaskViewSet, basename="tasks")
app_name = "users"
urlpatterns = [

    path("", include(router.urls)),
    path(
            "user_login/",
            SignUpViewSet.as_view({"post": "email_login"}),
            name="user_login",
        ),

]
