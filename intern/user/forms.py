from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class SendEmailForm(forms.Form):
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Subject')}))
    message = forms.CharField(widget=forms.Textarea)
    users = forms.ModelMultipleChoiceField(label="To",
                                           queryset=User.objects.all(),
                                           widget=forms.SelectMultiple())