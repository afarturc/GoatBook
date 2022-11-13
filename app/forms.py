from django import forms

class EditPostForm(forms.Form):
    caption = forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Caption", 
            "id": "caption", 
            "name": "caption",
    }))
    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            "class": "file-input file-input-bordered file-input-primary w-full",
            "id": "image",
            "name": "image",
    }))

#COMMENT
class CommentForm(forms.Form):
    comment = forms.CharField(max_length=256 ,widget=forms.TextInput(
        attrs={
            "class": "input input-bordered w-full",  
            "placeholder": "Comment", 
            "id": "comment", 
            "name": "comment",
    }))

class ImageForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            "class": "file-input file-input-bordered file-input-primary w-full",
            "id": "image",
            "name": "image",
    }))

class PasswordForm(forms.Form):
    old_password = forms.CharField(max_length=256, widget=forms.PasswordInput(
        attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Old Password",
            "id": "old_password",
            "name": "old_password",
    }))

    new_password = forms.CharField(max_length=256, widget=forms.PasswordInput(
        attrs={
            "class": "input input-bordered w-full",
            "placeholder": "New Password",
            "id": "new_password",
            "name": "new_password",
    }))

    password_confirm = forms.CharField(max_length=256, widget=forms.PasswordInput(
        attrs={
            "class": "input input-bordered w-full", 
            "placeholder": "Confirm New Password",
            "id": "password_confirm",
            "name": "password_confirm",
    }))

class BioForm(forms.Form):
    bio = forms.CharField(max_length=256, widget=forms.Textarea(
        attrs={
            "class": "input input-bordered w-full", 
            "placeholder": "Bio",
            "id": "bio",
            "name": "bio",
    }))







