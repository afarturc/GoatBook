from django import forms

class FormSingup(forms.Form):
    username = forms.CharField( widget=forms.TextInput(
        attrs={'class': 'input input-bordered w-full',
                'placeholder': 'Username',
                'id': 'username',
                'name': 'username',}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input input-bordered w-full',
                'placeholder': 'Password',
                'id': 'password',
                'name': 'password',}))

    email = forms.EmailField( widget=forms.EmailInput(
        attrs={'class': 'input input-bordered w-full',
                'placeholder': 'Email',
                'id': 'email',
                'name': 'email',}))

    confirmation = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input input-bordered w-full',
                'placeholder': 'Confirm Password',
                'id': 'password2',
                'name': 'confirmation',}))
    
    photo = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'file-input file-input-bordered file-input-primary w-full',
                'placeholder': 'Photo',
                'id': 'photo',
                'name': 'photo',}))




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







