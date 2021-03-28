from .models import Tour, Announcements
from django import forms

class AddDate_Form(forms.ModelForm):
    city = forms.CharField(label='City', max_length=255)
    venue = forms.CharField(label='Venue', max_length=255)
    show_date = forms.DateInput()
    price = forms.DecimalField(label='Price', decimal_places=2)
    tickets = forms.URLField(label='Ticket Link', required=False)
    details = forms.CharField(label='Details', max_length=255, widget=forms.Textarea)

    class Meta:
        model = Tour
        fields = '__all__'

class AddAnn_Form(forms.ModelForm):
    post = forms.CharField(label='', max_length=255, widget=forms.TextInput(attrs={'class' : 'testcss'}))

    class Meta:
        model = Announcements
        fields = '__all__'