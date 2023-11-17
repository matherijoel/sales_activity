from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Record, Profile
from django import forms
from django.forms.widgets import PasswordInput, TextInput

# - Register/Create a user
title_choices = (
    ('', 'your job title'),  # Initial option
    ('DSF', 'DIRECT SALES FORCE'),
    ('UM', 'UNIT MANAGER'),
    ('BDE - M', 'BDE - MEDICAL'),
    ('BDE - GI', 'BDE - GENERAL'),
    ('BM', 'BRANCH MANAGER'),
    ('MB', 'MANAGER BRANCHES'),
    ('HM', 'HEAD OF MEDICAL'),
    ('HC', 'HEAD OF COMMERCIAL'),
    ('OTHER', 'OTHER'),
)

branch_choices = (
    ('', 'Select a branch'),  # Initial option
    ('HQ', 'HEAD OFFICE'),
    ('NAKURU', 'NAKURU'),
    ('CBD', 'NAIROBI CBD'),
    ('MERU', 'MERU'),
    ('MOMBASA', 'MOMBASA'),
    ('THIKA', 'THIKA'),
    ('KISUMU', 'KISUMU'),
    ('ELDORET', 'ELDORET'),
)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    job_title = forms.TypedChoiceField(label="", coerce=str, widget=forms.Select(attrs={'placeholder': 'your job title'}), choices=title_choices)
    branch_name = forms.TypedChoiceField(label="", coerce=str, widget=forms.Select(attrs={'placeholder': 'Select a branch'}), choices=branch_choices)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'job_title', 'branch_name', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

# Update User
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    job_title = forms.TypedChoiceField(label="", widget=forms.Select(attrs={'placeholder': 'your job title'}), choices=title_choices)
    branch_name = forms.TypedChoiceField(label="", widget=forms.Select(attrs={'placeholder': 'Select a branch'}), choices=branch_choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'job_title', 'branch_name']

# Update User Profile
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']

# - Login a user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

# - Create a record
class CreateRecordForm(forms.ModelForm):
    created_by = forms.ModelChoiceField(label="", queryset=User.objects.all(), widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Created By'}),)
    class Meta:
        model = Record
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'county', 'nearest_town', 'current_insurer', 
                  'intermediary_name', 'engagement_date', 'anticipated_closure_date', 'business_class', 
                  'expected_premium', 'chances_of_closure', 'current_stage', 'additional_remarks','created_by']
        widgets = {
            'engagement_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date', 'placeholder': 'DD/MM/YYYY'}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateRecordForm, self).__init__(*args, **kwargs)
        if user:
            self.initial['created_by'] = user

    def save(self, commit=True):
        record = super(CreateRecordForm, self).save(commit=False)
        record.created_by = self.cleaned_data['created_by']
        if commit:
            record.save()
            return record

# - Update a record
class UpdateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'county', 'nearest_town', 'current_insurer', 
                  'intermediary_name', 'engagement_date', 'anticipated_closure_date', 'business_class', 
                  'expected_premium', 'chances_of_closure', 'current_stage', 'additional_remarks']
        widgets = {
            'engagement_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date', 'placeholder': 'DD/MM/YYYY'}),
        }
