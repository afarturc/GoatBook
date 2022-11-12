from django import forms
#POST
class PostForm(forms.Form):
    caption = forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={
            "class": "form-control", 
            "placeholder": "Caption", 
            "id": "caption", 
            "name": "caption",
            "row": "3",
    }))
    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            "class": "form-control",
            "id": "image",
            "name": "image",
    }))


class EditPostForm(forms.Form):
    post_id = forms.IntegerField(widget=forms.HiddenInput(
        attrs={
            "id": "post_id",
            "name": "post_id",
    }))
    caption = forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={
            "class": "form-control", 
            "placeholder": "Caption", 
            "id": "caption", 
            "name": "caption",
            "row": "3",
    }))
    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            "class": "form-control",
            "id": "image",
            "name": "image",
    }))

#COMMENT
class CommentForm(forms.Form):
    comment = forms.CharField(max_length=256 ,widget=forms.TextInput(
        attrs={
            "class" :"input w-full", 
            "placeholder": "Comment", 
            "id": "comment", 
            "name": "comment",
            "row": "3",
    }))


#Like
class LikeForm(forms.Form):
    #disabled button
    like= forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={
            "class" :"btn btn-primary",
            "type": "submit",
            "value": "Like",
            "id": "like",
            "name": "like",
    }))
    

class LikeFormDelete(forms.Form):
    #active button
    Unlike = forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={
            "class" :"btn btn-primary",
            "type": "submit",
            "value": "Unlike",
            "id": "Unlike",
            "name": "Unlike",
    }))


class ImageForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            "class": "form-control",
            "id": "image",
            "name": "image",
    }))

class PasswordForm(forms.Form):
    old_password = forms.CharField(max_length=256, widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "Atual Password",
            "id": "old_password",
            "name": "old_password",
    }))

    new_password = forms.CharField(max_length=256, widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "Nova Password",
            "id": "new_password",
            "name": "new_password",
    }))

    password_confirm = forms.CharField(max_length=256, widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "Confirmar Password",
            "id": "password_confirm",
            "name": "password_confirm",
    }))

class BioForm(forms.Form):
    bio = forms.CharField(max_length=256, widget=forms.Textarea(
        attrs={
            "class": "form-control w-full",
            "placeholder": "Bio",
            "id": "bio",
            "name": "bio",
    }))







