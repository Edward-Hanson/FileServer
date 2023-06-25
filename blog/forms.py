from django import forms

class EmailForm(forms.Form):
    recipient_email = forms.EmailField(label='Recipient Email')
