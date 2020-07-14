from django.contrib import admin
from django.urls import path
from Connect.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include, url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('login/', Login, name="login"),
    path('contact-us/', Contact, name="contact"),
    path('AddQuery/', Contact_Us, name="contact-us"),
    path('Contact_Company/<int:comp_id>/', Contact_Company, name="contact-company"),
    path('', Home, name="home"),
    path('logout/', Logout, name="logout"),
    path('Register/', Register, name="register"),
    path('all_professionals/<str:what>/', All_Profession, name="professional"),
    path('professional_html/<str:what>/', All_Professional_Html, name="professional_html"),
    path('connection/<str:action>/<int:u_id>/', Manage_your_connections, name="connections"),
    path('in/<str:Username>/', UserProfile, name="UserProfile"),
    path('in/Edit/<str:Username>/', Update_User_Details, name="UpdateUserProfile"),

    path('add_company/', Add_Company, name="addCompany"),
    path('List_Of_companies/', All_companies, name="all_companies"),
    path('Detail/<int:c_id>/', Company_details, name="company_details"),
    path('Update/Detail/<int:c_id>/', Upddate_Company_details, name="Upddate_Company_details"),

    path('job_lists', Job_Lists, name="job_lists"),
    path('job_details', Job_Details, name="job_details"),

    path('post_new_blog/', NewPost, name="post"),
    path('likes/<int:b_id>/<str:Username>/', Like_By_Me, name="likes"),

    path('follow_company/<int:c_id>/', Company_Followers, name="follow_company"),
    path('follow/<str:action>/<int:u_id>/', Manage_Followers, name="follow"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

