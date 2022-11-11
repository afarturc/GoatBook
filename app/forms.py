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
    comment = forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={
            "class" :"input w-full", 
            "placeholder": "Comment", 
            "id": "comment", 
            "name": "comment",
            "row": "3",
    }))


class LikeForm(forms.Form):
    like = forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={
            "class": "form-control", 
            "placeholder": "Like", 
            "id": "like", 
            "name": "like",
            "row": "3",
    }))


    