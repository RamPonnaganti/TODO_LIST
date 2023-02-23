from django.urls import path
from .views import HomeView, AddTodoView, DeleteTodoView,ChangeTodoView, LoginView, SignupView, SignoutView

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('add/',AddTodoView.as_view(), name='add_todo'),
    path('delete/<int:pk>/',DeleteTodoView.as_view(),name='deletetodo'),
    path('change/<int:id>/<str:status>/', ChangeTodoView.as_view(), name='change_todo'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signout/', SignoutView.as_view(), name='signout'),
]

