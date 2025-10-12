from django.urls import path, include
from rest_framework import routers
from formTasks import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet,'tasks')

urlpatterns=[
    path('data/', include(router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]