from django import forms
from .models import *

class AddUser_Form(forms.ModelForm):
    class Meta:
        model = UserDataBase
        exclude = ("usr", "degree", "dob", "location", "experience", "website",
                   "facebook_ac", "instagram_ac", "linkedin_ac", "google_ac", "whatshapp_ac")
        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control", }),
            "email":forms.EmailInput(attrs={"class":"form-control", }),
            "number":forms.NumberInput(attrs={"class":"form-control", }),
            "image":forms.FileInput(attrs={"class":"form-control","onchange":"loadFile(event)" }),
            "about":forms.Textarea(attrs={"class":"form-control", "rows":"5"}),
        }



class Edit_User_Details(forms.ModelForm):
    class Meta:
        model = UserDataBase
        exclude = ("usr",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", }),
            "company": forms.TextInput(attrs={"class": "form-control", }),
            "email": forms.EmailInput(attrs={"class": "form-control", }),
            "number": forms.NumberInput(attrs={"class": "form-control", }),
            "about": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            "location": forms.TextInput(attrs={"class": "form-control", }),
            "degree": forms.TextInput(attrs={"class": "form-control", }),
            "website": forms.TextInput(attrs={"class": "form-control", }),
            "experience": forms.TextInput(attrs={"class": "form-control", }),
            "image": forms.FileInput(attrs={"class":"form-control", "onchange": "loadFile(event)"}),
            "user_title": forms.TextInput(attrs={"class": "form-control", }),
            "facebook_ac": forms.TextInput(attrs={"class": "form-control", }),
            "instagram_ac": forms.TextInput(attrs={"class": "form-control", }),
            "linkedin_ac": forms.TextInput(attrs={"class": "form-control", }),
            "google_ac": forms.TextInput(attrs={"class": "form-control", }),
            "whatshapp_ac": forms.NumberInput(attrs={"class": "form-control", }),
            "dob": forms.DateInput(attrs={"class": "form-control", })
        }


class Add_Company_Details(forms.ModelForm):
    class Meta:
        model = Company_Model
        exclude = ("usr",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": "required"}),
            "category": forms.TextInput(attrs={"class": "form-control", "required": "required", "value": "Information Technology"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "required": "required"}),
            "number": forms.NumberInput(attrs={"class": "form-control", "required": "required"}),
            "about": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            "location": forms.TextInput(attrs={"class": "form-control", }),
            "degree": forms.TextInput(attrs={"class": "form-control", }),
            "logo": forms.FileInput(attrs={"class": "form-control", "required": "required", "onchange": "loadFile(event)"}),
            "website": forms.TextInput(attrs={"class": "form-control", "required": "required"}),
            "company_title": forms.TextInput(attrs={"class": "form-control", }),
            "linkedin_ac": forms.TextInput(attrs={"class": "form-control", }),
            "start_date": forms.DateInput(attrs={"class": "form-control", })
        }


class Update_Company_Detail(forms.ModelForm):
    class Meta:
        model = Company_Model
        exclude = ("usr",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", }),
            "category": forms.TextInput(attrs={"class": "form-control",}),
            "email": forms.EmailInput(attrs={"class": "form-control", }),
            "number": forms.NumberInput(attrs={"class": "form-control", }),
            "about": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            "map": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            "location": forms.TextInput(attrs={"class": "form-control", }),
            "company_title": forms.TextInput(attrs={"class": "form-control", }),
            "website": forms.TextInput(attrs={"class": "form-control", }),
            "logo": forms.FileInput(attrs={"class": "form-control", "onchange": "loadFile(event)"}),
            "linkedin_ac": forms.TextInput(attrs={"class": "form-control", }),
            "is_verified": forms.Select(attrs={"class": "form-control", }),
        }

class UserBlog_Form(forms.ModelForm):
    class Meta:
        model = Blogs_Model
        exclude = ("usr",)
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", }),
            "youtube_video": forms.Textarea(attrs={"class": "form-control", }),
            "blog": forms.Textarea(attrs={"class": "form-control", })
        }

