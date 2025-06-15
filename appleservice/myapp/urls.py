from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.home, name = "Home"),
    path("login/", views.login_panel, name = "Login"),
    path("register/", views.register_panel, name = "Register"),
    path("ustawienia/", views.settings_panel, name = "Settings"),
    path("rezerwacja/", views.visit_panel, name = "Rezerwacja"),
    path("dashboard/zlecenia/", views.zlecenia_panel, name = "Zlecenia"),
    path("dashboard/faktury/", views.faktury_panel, name = "Faktury"),
    path("dashboard/magazyn/", views.magazyn_panel, name = "Magazyn"),
    path("dashboard/zlecenia/view/<str:zl_id_zlecenia>/", views.zlecenia_view, name = "Zlecenia_view"),
    path("dashboard/faktury/view/<str:zl_id_zlecenia>/", views.faktury_view, name = "Faktury_view"),
    path("dashboard/", views.dashboard_panel, name = "_dashboard"),
    path("logout/", views.logout_view, name = "_logout")
]
