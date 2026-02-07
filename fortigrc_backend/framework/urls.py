from django.urls import path
from .views import FrameworkListView, DashboardStatsView

urlpatterns = [
    path('framework/', FrameworkListView.as_view(), name='framework-list'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
