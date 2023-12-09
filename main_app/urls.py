from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "notion"
urlpatterns = [
    path('', views.MainView.as_view(), name="main"),
    path("<int:notion_id>/", views.get_notion, name="get_notion"),
    path("notions/", views.get_list_notions, name="get_notions"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("<int:notion_id>/delete", views.delete_notion, name="delete_notion"),
    path("<int:notion_id>/update", views.update_notion, name="update_notion"),
    path('add_friend/<int:friend_id>/', views.add_friend, name='add_friend'),
    path('remove_friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),
    path('friends/', views.list_friends, name='list_friends'),
    path('friend_notations/<int:friend_id>/', views.friend_notations, name='friend_notations'),
    path('<int:user_id>/profile/', views.get_profile, name='get_profile'),
    path('update_profile_pic/', views.update_profile_pic, name='update_profile_pic'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)