from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import *
from django.db.models import Q



""" Sending Email Code block Start"""

from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
def SendEmailOld(email, msg):
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    html = get_template("mail.html").render({"msg": msg})
    #html = "<h1>Email</h1>"
    sub = "SocialMedia - New Contacted Person"
    send_mail(sub, " ", from_email, to_email, html_message=html)



def Home(request):
    return render(request, 'index.html')

def Login(request):
    if request.user.is_authenticated:
        return redirect("UserProfile", request.user.username)

    form = AddUser_Form()
    error = False
    if request.method == "POST":
        un = request.POST["un"]
        ps = request.POST["ps"]
        usr = authenticate(username=un, password=ps)
        if usr != None:
            login(request, usr)
            return redirect("UserProfile", usr.username)
        error = True
    Dict = {
        "error": error, "form": form
    }
    return render(request, "login.html", Dict)

def Logout(request):
    logout(request)
    return redirect("home")


def Contact(request):
    return render(request, "contact.html")


def Job_Details(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "job-board-details.html")

def Job_Lists(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "job-board.html")


def Register(request):
    if request.method == "POST":
        form = AddUser_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            un = request.POST["un"]
            ps = request.POST["ps"]
            email = data.email

            usr = User.objects.create_user(un, email, ps)
            data.usr = usr
            data.save()
            return redirect("login")
    return HttpResponse("Register Your Self")


def UserProfile(request, Username):
    if not request.user.is_authenticated:
        return redirect("login")

    usr = User.objects.filter(username=Username)

    c_user = User.objects.get(username=request.user.username)
    try:
        companies = Company_Model.objects.filter(usr=c_user)
        detail = Company_Model.objects.get(usr=c_user)
    except:
        companies = ""
        detail = ""

    if not usr:
        loggen_in_username = request.user.username
        return redirect("UserProfile", loggen_in_username)

    connection = None
    if request.user.username != Username:
        user1 = User.objects.get(username=Username)
        user2 = User.objects.get(username=request.user.username)
        UserData1 = UserDataBase.objects.get(usr=user1)
        UserData2 = UserDataBase.objects.get(usr=user2)

        #Find out who send and receieve the friend request
        connection = Connections.objects.filter(Q(sender=UserData1, receiver=UserData2) | Q(sender=UserData2, receiver=UserData1))
        if connection:
            connection = connection[0]

    blog_form = UserBlog_Form()
    Usr = usr[0]
    User_Detail = UserDataBase.objects.get(usr=Usr)

    requested_data = UserDataBase.objects.get(usr=c_user)

    all_posts = Blogs_Model.objects.filter(usr=Usr).order_by("-date")
    # (all_posts.count == 0)
    if not all_posts.exists():
        all_posts = ""

    ###### Count Follow Section #########
    Profile_user = User.objects.get(username=Username)
    Profile_user_data = UserDataBase.objects.get(usr=Profile_user)
    follow_request = User_Follow.objects.filter(followers=Profile_user_data)
    Follow_sent = User_Follow.objects.filter(following=Profile_user_data)

    user_is_following = User_Follow.objects.filter(followers=Profile_user_data, following=requested_data)
    if not user_is_following.exists():
        user_is_following = ""
    # ------ Count Follow Section End -------#

    like_by_me_Ids = []
    all_likes_by_me = BlogLikes.objects.filter(usr=request.user)
    for i in all_likes_by_me:
        like_by_me_Ids.append(i.blog.id)


    Dict = {
        "Profile": User_Detail, "connection": connection, "detail": detail, "companies": companies,
        "form": blog_form, "all_posts": all_posts, "like_by_me_Ids": like_by_me_Ids,
        "user_is_following": user_is_following, "follow_request": follow_request, "Follow_sent": Follow_sent
    }

    return render(request, "user_details.html", Dict)



def Update_User_Details(request, Username):
    if not request.user.is_authenticated:
        return redirect("login")

    loggen_in_username = request.user.username
    if Username != loggen_in_username:
        return redirect("UserProfile", loggen_in_username)

    usr = User.objects.filter(username=Username)
    Usr = usr[0]
    User_Detail = UserDataBase.objects.get(usr=Usr)

    form = Edit_User_Details(request.POST or None, request.FILES or None, instance=User_Detail)
    if form.is_valid():
        form.save()
        return redirect("UserProfile", loggen_in_username)

    Dict = {
        "Profile": User_Detail, "form": form
    }

    return render(request, "update_user_details.html", Dict)

def All_Profession(request, what):
    if not request.user.is_authenticated:
        return redirect("login")

    logged_in_user = User.objects.get(username = request.user.username)
    me = UserDataBase.objects.get(usr = logged_in_user)
    ###### Count Request Section #########
    con_request = Connections.objects.filter(receiver=me, status="Sent")
    con_sent = Connections.objects.filter(sender=me, status="Sent")
    con_friend = Connections.objects.filter(Q(sender=me, status="friend") | Q(receiver=me, status="friend")).order_by( "-date")

    #-----X Count Request Section End ---X_------#


    data = ""
    if what == "all":
        data = UserDataBase.objects.all()
    if what == "myreceived":
        connection = Connections.objects.filter(receiver=me, status = "Sent")
        User_Data = []
        for c in connection:
            ud = UserDataBase.objects.get(id = c.sender.id)
            User_Data.append(ud)
        data = User_Data
    if what == "Sent":
        connection = Connections.objects.filter(sender=me, status = "Sent")
        User_Data = []
        for c in connection:
            ud = UserDataBase.objects.get(id=c.receiver.id)
            User_Data.append(ud)
        data = User_Data
    if what == "Friends":
        connection = Connections.objects.filter(Q(sender=me, status = "friend") | Q(receiver=me, status = "friend")).order_by("-date")
        Data = []
        for c in connection:
            UserData = UserDataBase.objects.get(id = c.sender.id)
            if UserData.id != me.id:
                Data.append(UserData)

            UserData = UserDataBase.objects.get(id=c.receiver.id)
            if UserData.id != me.id:
                Data.append(UserData)
            data = Data
    Dict = {
        "all_users": data, "what": what, "con_request": con_request, "con_sent": con_sent,
        "con_friend": con_friend
    }
    return render(request, "professionals.html", Dict)



def All_Professional_Html(request, what):
    if not request.user.is_authenticated:
        return redirect("login")

    logged_in_user = User.objects.get(username=request.user.username)
    me = UserDataBase.objects.get(usr=logged_in_user)
    ###### Count Request Section #########

    con_request = Connections.objects.filter(receiver=me, status="Sent")
    con_sent = Connections.objects.filter(sender=me, status="Sent")
    con_friend = Connections.objects.filter(Q(sender=me, status="friend") | Q(receiver=me, status="friend")).order_by( "-date")

    #-----X Count Request Section End ---X_------#

    data = ""
    if what == "all":
        data = UserDataBase.objects.all()


    ###### Count Follow Section #########
    follow_request = User_Follow.objects.filter(followers=me)
    Follow_sent = User_Follow.objects.filter(following=me)
    #------ Count Follow Section End -------#


    Dict = {
        "all_users": data, "what": what, "con_request": con_request, "con_sent": con_sent,
        "con_friend": con_friend, "me": me, "follow_request": follow_request, "Follow_sent": Follow_sent
    }

    return render(request, "professionals_html.html", Dict)





def Manage_your_connections(request, action, u_id):
    if not request.user.is_authenticated:
        return redirect("login")

    if action == "Send_Request":
        senderUser = User.objects.get(username=request.user.username)
        sender = UserDataBase.objects.get(usr=senderUser)
        receiver = UserDataBase.objects.get(id=u_id)
        Connections.objects.create(sender=sender, receiver=receiver)
        return redirect("UserProfile", receiver.usr.username)

    if action == "Accept_Request" or action == "Reject_Request" or action == "Remove_Connection":
        ReceiverUser = User.objects.get(username=request.user.username)
        receiver = UserDataBase.objects.get(usr=ReceiverUser)
        sender = UserDataBase.objects.get(id=u_id)
        connection = Connections.objects.filter(sender=sender, receiver=receiver)
        if connection:
            for c in connection:
                if action == "Accept_Request":
                    c.status = "friend"
                    c.save()
                if action == "Reject_Request":
                    c.status = "rejected"
                    c.delete()
                if action == "Remove_Connection":
                    c.status = "rejected"
                    c.delete()

        return redirect("professional", "all")


def Add_Company(request):
    form = Add_Company_Details(request.POST, request.FILES)
    message = ""
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            added = request.POST['addedby']
            if request.user.username == added:
                usr = User.objects.get(username=request.user.username)
                data.usr = usr
                data.save()
                return redirect("UserProfile", request.user.username)
            else:
                message = "Only LoggedIn User \"{}\" can add company but you are trying to with \"{}\" user".format(request.user.username, added)
    return render(request, "add_company.html", {"form": form, "message": message})


def All_companies(request):
    if not request.user.is_authenticated:
        return redirect('login')

    companies = Company_Model.objects.all()

    Dict = {
        'companies': companies
    }

    return render(request, 'Companies.html', Dict)


def Company_details(request, c_id):
    detail = Company_Model.objects.get(id=c_id)
    f = request.user
    followers = UserDataBase.objects.get(usr=f)
    try:
        follower = Follow_Company.objects.get(user=followers, company=detail)
        count = Follow_Company.objects.filter(company=detail)
        followers = request.user
    except:
        count = ""
        followers = ""
        follower = ""
    Dict = {
        "detail": detail, "followers": followers, "count": len(count), "follower": follower
    }
    return render(request, 'companies-detail.html', Dict)


def Upddate_Company_details(request, c_id):
    detail = Company_Model.objects.get(id=c_id)
    company_form = Update_Company_Detail(request.POST or None, request.FILES or None, instance=detail)
    message =""
    if request.method == "POST":
        if company_form.is_valid():
            data = company_form.save(commit=False)
            added = request.POST['addedby']
            if request.user.username == added:
                data.save()
                return redirect("UserProfile", request.user.username)
            else:
                message = "Logged in User and Updated by field should be same"

    Dict = {
        "detail": detail,
        "company_form": company_form,
        "message": message
    }
    return render(request, "update_company_details.html", Dict)


def NewPost(request):
    if request.method == "POST":
        form = UserBlog_Form(request.POST)
        if form.is_valid():
            data = form.save(commit = False)
            data.usr = request.user
            data.save()
            print("Blog Submitted...@")
    return redirect("UserProfile", request.user.username)


def Like_By_Me(request, b_id, Username):
    if not request.user.is_authenticated:
        return redirect("login")

    blog = Blogs_Model.objects.get(id=b_id)
    BlogLikes.objects.create(usr=request.user, blog=blog)
    user = User.objects.get(username=blog.usr.username)
    ud = UserDataBase.objects.get(usr=user)
    name = ud.name.split()[0]
    number = ud.number
    email = ud.email
    n_likes = len(BlogLikes.objects.filter(blog=blog))
    msg = "Hi, {name}! You got new Like for blog - *{title}*. " \
          "And total likes for this Blog is {likes}.".format(name=name, title=blog.title, likes=n_likes)
    # SendSms(number, msg)
    SendEmailOld(email, msg)
    return redirect("UserProfile", Username)


def Manage_Followers(request, action, u_id):
    if not request.user.is_authenticated:
        return redirect("login")


    # Following = who send the Follow request
    # Follower = Who receive the Follow request

    if action == "Following":
        senderUser = User.objects.get(username=request.user.username)
        sender = UserDataBase.objects.get(usr=senderUser)
        receiver = UserDataBase.objects.get(id=u_id)
        User_Follow.objects.create(following=sender, followers=receiver)
        return redirect("professional_html", "all")

    if action == "Follower":
        ReceiverUser = User.objects.get(username=request.user.username)
        receiver = UserDataBase.objects.get(usr=ReceiverUser)
        sender = UserDataBase.objects.get(id=u_id)
        User_Follow.objects.create(following=sender, followers=receiver)
        return redirect("professional_html", "all")



def Company_Followers(request, c_id):
    if not request.user.is_authenticated:
        return redirect("login")
    print("entered")
    # Following = who send the Follow request

    senderUser = User.objects.get(username=request.user.username)
    sender = UserDataBase.objects.get(usr=senderUser)
    receiver = Company_Model.objects.get(id=c_id)
    Follow_Company.objects.create(user=sender, company=receiver)

    return redirect("company_details", c_id)




def Contact_Us(request):
    if request.method == "POST":
        email = request.POST['email']
        msg = request.POST['msg']
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        Queries.objects.create(email=email, first_name=first_name, last_name=last_name, query=msg)
        msg_for_u = "Thank you {} for contacting us. Our Team will Contact You within 24 hrs.".format(first_name)
        SendEmailOld(email, msg_for_u)
    return render(request, "index.html")

def Contact_Company(request, comp_id):
    if request.method == "POST":
        c= Company_Model.objects.get(id=comp_id)
        email = request.POST['email']
        msg = request.POST['message']
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        con = request.POST['country']
        Company_Queries.objects.create(comp=c, email=email, first_name=first_name, last_name=last_name, query=msg, country=con)
        msg_for_u = "Thank you {} for contacting us. Our Team will Contact You within 24 hrs.".format(first_name)
        SendEmailOld(email, msg_for_u)
    return redirect("company_details", comp_id)

