from django.forms import ModelForm
from .models import User, Tickets, Feedbacks
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from products.models import Cities, Categories, Shops

class RegisterForm(forms.Form):

    username = forms.CharField(min_length=4, max_length=150, label="نام کاربری",
                               widget=forms.TextInput(attrs={"id": "username-input", "class": "textbox-based"}))
    email = forms.EmailField(label="ایمیل",widget=forms.EmailInput(attrs={"id":"email-input", "class": "textbox-based"}))
    password = forms.CharField(min_length=8, max_length=100, label="گذرواژه",
                               widget=forms.PasswordInput(attrs={"id":"password-input", "class":"textbox-based"}))
    confirm_password = forms.CharField(min_length=8, max_length=100, label="تایید گذرواژه",
                                       widget=forms.PasswordInput(attrs={"id": "confitm-password-input", "class": "textbox-based"}))


    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("شخص دیگری با این ایمیل ثبت نام کرده است")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("شخص دیگری با این نام کاربری ثبت نام کرده است")
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if password and confirm_password and password == confirm_password:
            return confirm_password
        else:
            raise ValidationError("گذرواژه و تایید گذرواژه باهم تطابق ندارند")


class LoginForm(forms.Form):

    username = forms.CharField(label="نام کاربری", min_length=4, max_length=150,
                               widget=forms.TextInput(attrs={"id":"username-input", "class":"textbox-based"}))
    password = forms.CharField(label="گذرواژه", min_length=8, max_length=100,
                               widget=forms.PasswordInput(attrs={"id": "password-input", "class": "textbox-based"}))

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            return password
        raise ValidationError("نام کاربری یا گذرواژه نادرست است")



class FilterProductMainPageForm(forms.Form):
    ranks = (
        (None, "-----"),
        ("a", "A"),
        ("b", "B"),
        ("c", "C"),
        ("d", "D"),
        ("e", "E"),
        ("f", "F"),
        ("o", "Out of range")
    )
    city_items = [(city.name, city.name) for city in Cities.objects.all()]
    city_items.insert(0, (None, "-----"))
    category_items = [(category.name, category.name) for category in Categories.objects.all()]
    category_items.insert(0, (None, "-----"),)
    shop_name_items = [(shop.name, shop.name) for shop in Shops.objects.published()]
    shop_name_items.insert(0, (None, "-----"),)
    city = forms.ChoiceField(required=False, label="شهر",
                             choices=city_items,
                             widget=forms.Select(attrs={"class": "input-section-based", "id": "city-selector"}))
    shop_name = forms.ChoiceField(required=False,
                                    choices=shop_name_items,
                                label="نام فروشگاه",
                                widget=forms.Select(attrs={"class": "input-section-based",
                                                              "id": "shop-name"}))
    category = forms.ChoiceField(required=False, label="دسته بندی",
                                 choices=category_items,
                                 widget=forms.Select(attrs={"class": "input-section-based",
                                                            "id": "rank-shop-selector"}))

class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        widgets = {
            "username": forms.TextInput(attrs={"class": "textbox-based textbox-normal-size",
                                                             "id": "username-box"}),
            "email": forms.EmailInput(attrs={"class": "textbox-based textbox-normal-size",
                                                                          "id": "email-box"}),
            "first_name": forms.TextInput(attrs={"class": "textbox-based textbox-normal-size",
                                                               "id": "first-name-box"}),
            "last_name": forms.TextInput(attrs={"class": "textbox-based textbox-normal-size", "id": "last-name-box"})
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        is_same = self.user.email == email
        if user:
            if is_same:
                return email
            raise ValidationError("شخص دیگری با این ایمیل ثبت نام کرده است")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(username=username).exists()
        is_same = self.user.username == username
        if user:
            if is_same:
                return username
            raise ValidationError("شخص دیگری با این نام کاربری ثبت نام کرده است")
        return username


class UserChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

    password = forms.CharField(min_length=8, max_length=100, label="گذرواژه کنونی",
                               widget=forms.PasswordInput(attrs={"class": "textbox-based textbox-normal-size", "id": "username-box"}))
    new_password = forms.CharField(min_length=8, max_length=100, label="گذرواژه جدید",
                               widget=forms.PasswordInput(attrs={"class": "textbox-based textbox-normal-size", "id": "email-box"}))
    confirm_new_password = forms.CharField(min_length=8, max_length=100, label="تکرار گذرواژه جدید",
                               widget=forms.PasswordInput(attrs={"class": "textbox-based textbox-normal-size", "id": "first-name-box"}))

    def clean_password(self):
        password = self.cleaned_data.get("password")
        user = User.objects.get(id=self.user.id)
        valid = self.user.check_password(password)
        if not valid:
            raise ValidationError("گذرواژه وارد شده نادرست است")
        else:
            return password

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")

        if new_password and confirm_new_password and new_password == confirm_new_password:
            return confirm_new_password
        else:
            raise ValidationError("گذرواژه ها با یکدیگر تطابق ندارند")


class TicketUserMessageForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ("user_text_message", )
        widgets = {
            "user_text_message": forms.Textarea(attrs={"id": "text-message-user"}),
        }


class TickeAdminMessageForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ("admin_text_message", )
        widgets = {
            "admin_text_message": forms.Textarea(attrs={"id": "text-message-user"}),
        }

        labels = {
            "admin_text_message": "متن بازخورد تیکت",
        }


class ContractUsForm(forms.ModelForm):
    class Meta:
        model = Feedbacks
        fields = ("name", "description")
        widgets = {
            "name": forms.TextInput(attrs={"id": "id-name", "class": "textbox-based"}),
            "description": forms.Textarea(attrs={"id": "description-id", "class": "textarea-descrption"}),
        }

