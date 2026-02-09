from django.urls import path
from .views import FrameworkListView, DashboardStatsView, ExecutiveReportView

urlpatterns = [
    path('framework/', FrameworkListView.as_view(), name='framework-list'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('reports/executive/', ExecutiveReportView.as_view(), name='executive-report'),
]
