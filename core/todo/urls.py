from django.urls import path,include
from todo.views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete
urlpatterns = [
    path('',TaskList.as_view(),name='tasks'),
    path('item/<int:pk>',TaskDetail.as_view(),name='items'),
    path('create-task/',TaskCreate.as_view(),name='create-task'),
    path('update-task/<int:pk>',TaskUpdate.as_view(),name='update-task'),
    path('delete-task/<int:pk>',TaskDelete.as_view(),name='delete-task'),
    ]