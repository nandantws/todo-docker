from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, TodoCollectionViewSet,TodoViewSet

router = DefaultRouter()
router.register('todos', TodoCollectionViewSet,basename='todos')
router.register('todo', TodoViewSet,basename='todo')

urlpatterns = [
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login')
]

urlpatterns += router.urls
