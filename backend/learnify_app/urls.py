# external_courses/urls.py
from rest_framework.routers import DefaultRouter
from .views import CourseProxyViewSet

router = DefaultRouter()
router.register(r'api/learnify_app',CourseProxyViewSet,basename='learnify_app')

urlpatterns = router.urls
