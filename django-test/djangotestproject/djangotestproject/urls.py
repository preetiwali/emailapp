"""djangotestproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from testapp import views

urlpatterns = [
    path('', views.IndexPageController, name='index_page'),
    path('firstPage', views.firstPageController, name="first_page"),

    path('htmlPages', views.HtmlPageController, name='html_page'),

    path('htmlPagesWithData', views.HtmlPageControllerWithData, name='html_page_data'),

    path('htmlWithDataPass/<str:url_data', views.PassingDataController, name='html_data_pass'),

    path('addData', views.addData, name='add_data'),

    path('add_users', views.add_users, name='add_users'),

    path('add_subscribers', views.add_subscribers, name='add_subscribers'),

    path('show_all_data', views.show_all_data, name='show_all_data'),

    path('update_user/<str:user_id>', views.update_user, name='update_user'),

    path('edit_user', views.edit_user, name='edit_user'),

    path('delete_user/<str:user_id>', views.delete_user, name='delete_user'),

    path('edit_subscriber', views.edit_subscriber, name='edit_subscriber'),

    path('update_subscriber/<str:subscriber_id>', views.update_subscriber, name='update_subscriber'),

     path('delete_subscriber/<str:subscriber_id>', views.delete_subscriber, name='delete_subscriber'),

    path('register_user/', views.RegisterUser, name='register_user'),

    path('login_user/', views.LoginUser, name='login_user'),

    path('save_user', views.SaveUser, name='save_user'),

    path('do_login_user', views.DoLoginUser, name='do_login_user'),

    path('homePage/', views.HomePage, name='homepage'),

    path('logout/', views.LogoutUser, name='logout'),

    path('admin/', admin.site.urls),

    path('send_mail_plain', views.SendPlainMail, name='send_mail_plain'),

    path('send_mail_plain_with_file', views.send_mail_plain_with_file, name='send_mail_plain_with_file'),

    path('set_session', views.setSession, name='set_session'),

    path('view_session', views.view_session, name='view_session'),

    path('del_session', views.del_session, name='del_session'),


]
