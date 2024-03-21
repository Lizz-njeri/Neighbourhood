from django.urls import path, include
from . import views
from .views import *
from . import views as app_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
      #AUTHENTICATION
    path('register/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('account/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # MAIN PAGE                                      
    path('', views.index, name='index'),

    # PROFILE SECTION
    path('profile/', views.profile, name='users-profile'),
    

    #HOOD SECTION
    path('all-hoods/', views.hoods, name='hood'),
    path('new-hood/', views.create_hood, name='new-hood'),

    # JOIN HOOD && LEAVE HOOD SECTION
    path('join_hood/<id>', views.join_hood, name='join-hood'),
    path('leave_hood/<id>', views.leave_hood, name='leave-hood'),

    # HOOD DETIALS SECTION
    path('hood-details/<hood_id>', views.hood_details, name='hood-details'),

    # CREATE POST SECTION
    path('<hood_id>/new-post', views.create_post, name='post'),

    # CREATE BUSINESS SECTION
    path('<hood_id>/new-business', views.create_business, name='business'),

    # HOOD MEMBERS SECTION
    path('<hood_id>/members', views.hood_members, name='members'),

    # SEARCH SECTION
    path('search/', views.search_business, name='search'),

]