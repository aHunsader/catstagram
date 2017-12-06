from django import forms
from .models import Picture, Profile
from django.core.files import File
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput
from django.core.files.base import ContentFile
import io
from PIL import Image
from django.core.files.storage import default_storage as storage




class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="", widget=TextInput(attrs={'autofocus': "true", 'class': "login well well-sm",'placeholder': "username"}))
    password = forms.CharField(label="", widget=PasswordInput(attrs={'class': "login well well-sm", 'placeholder':"password"}))

class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(label="", widget=TextInput(attrs={'class': "login well well-sm",'placeholder': "username"}))
    password1 = forms.CharField(label="", widget=PasswordInput(attrs={'class': "login well well-sm", 'placeholder':"password"}))
    password2 = forms.CharField(label="", widget=PasswordInput(attrs={'class': "login well well-sm", 'placeholder':"re-enter password"}))

class BioForm(forms.Form):
	bio_text = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Tell other users about yourself...', 'class': "bio well"}))


class PictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PictureForm, self).__init__(*args, **kwargs)

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    picFilter = forms.IntegerField(widget=forms.HiddenInput())
    caption = forms.CharField(label="", required=False, 
        widget=forms.Textarea(attrs={'placeholder': 'Add a caption', 'class': "caption-form well"}))
    image = forms.FileField(label="")
    



    class Meta:
        model = Picture
        fields = ('caption', 'image', 'x', 'y', 'width', 'height', 'picFilter', )

    def save(self):
        photo = super(PictureForm, self).save(commit=False)
        picFilter = self.cleaned_data.get('picFilter')
        current_user = self.user.profile
        photo.profile = current_user
        photo.save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        file = Image.open(photo.image)
        fh = storage.open(photo.image.name, "w")
        file = file if not picFilter else file.convert('L')
        cropped_image = file.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400, 400), Image.ANTIALIAS)
        resized_image.save(fh, 'png')
        fh.close()

        return photo



class ProfilePicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfilePicForm, self).__init__(*args, **kwargs)


    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    profile_pic = forms.FileField(label="Add a profile picture:")

    class Meta:
        model = Profile
        fields = ('profile_pic', 'x', 'y', 'width', 'height', )

    def save(self):
        current_user = self.user.profile
        current_user.profile_pic = self.cleaned_data.get('profile_pic')
        current_user.default = False
        current_user.save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        file = Image.open(current_user.profile_pic)
        fh = storage.open(current_user.profile_pic.name, "w")
        cropped_image = file.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400, 400), Image.ANTIALIAS)
        resized_image.save(fh, 'png')
        fh.close()

        return current_user
