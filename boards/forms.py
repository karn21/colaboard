from django import forms
from .models import Board, BoardList, ListCard
from django.forms import modelformset_factory
from django.conf import settings


class BoardCreationForm(forms.ModelForm):

    class Meta:
        model = Board
        fields = ['title', 'board_type']


ListModelFormset = modelformset_factory(
    BoardList,
    fields=('title', ),
    extra=1,
    widgets={'title': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your List Name'
    })
    }
)


class CardCreationForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Card name'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Card description'}))
    due_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'Card name', 'type': 'date'}))

    class Meta:
        model = ListCard
        fields = ['title', 'description', 'due_date', 'attachment']
