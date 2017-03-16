from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory
from django.contrib.auth.models import User

from .models import *


class QuestionForm(forms.Form):

    question_title = forms.CharField(help_text="Give your question a title")
    question_content = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 10}), help_text="Write your question here: ")

    class Meta:
        model = Question
        fields = ('question_title', 'question_content')


class AnswerForm(forms.Form):

    answer_text = forms.CharField(help_text="Write in an answer to this question")

    class Meta:
        model = Question
        fields = 'answer_text'



class QuestionVotesForm(forms.ModelForm):
    voteOn = forms.BooleanField(widget=forms.CheckboxInput())

    class Meta:
        model = QuestionVotes
        fields = ()

# la stå
# class CommentVotesForm(models.ModelForm):
#    voteOn = forms.BooleanField(widget=forms.CheckboxInput(default=False))
#
#    class Meta:
#        model=CommentVotes


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
