from django import forms

class updateTrainsForm(forms.Form):
    id = forms.CharField(max_length=5)
    trainname = forms.CharField(max_length=100)
    source = forms.CharField(max_length=100)
    destination = forms.CharField(max_length=100)
    starttime = forms.DateTimeField()
    endtime = forms.DateTimeField()
    totalseats = forms.IntegerField()
    filled = forms.IntegerField()
    status = forms.CharField(max_length=20)