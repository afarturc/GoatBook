from django import forms

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

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=256 ,widget=forms.TextInput(
        attrs={
            "class" :"input w-full", 
            "placeholder": "Comment", 
            "id": "comment", 
            "name": "comment",
            "row": "3",
    }))


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


    