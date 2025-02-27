from django.urls import path
from . import views

urlpatterns = [
    path("set_editor/", views.SetRoleAsEditor.as_view(), name="set_editor"),
    path("role/", views.GetRoleView.as_view(), name="role/")
]
