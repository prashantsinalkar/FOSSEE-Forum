from django import forms
from django.contrib.auth import login, logout, authenticate
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator, MinValueValidator, \
RegexValidator, URLValidator
from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField

from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator, MinValueValidator, \
RegexValidator, URLValidator
from django.template.defaultfilters import filesizeformat
from website.models import Profile


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        print username
        password = cleaned_data.get('password')
        print password
        if username is None or password is None:
            raise forms.ValidationError("Invalid username or password")
        user = authenticate(username=username, password=password)
        
        if not user:
            raise forms.ValidationError("Invalid username or password")
        if not user.is_active:
            raise forms.ValidationError("User is blocked")
        cleaned_data['user'] = user
        return cleaned_data
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'confirmation_code']
    first_name = forms.CharField(widget=forms.TextInput(),
                        required = True,
                        error_messages = {'required':'First name field required.'})
    last_name = forms.CharField(widget=forms.TextInput(),
                        required = True,
                        error_messages = {'required':'Last name field required.'})

    phone = forms.CharField(max_length = 12, widget=forms.TextInput(),required=False, validators = [RegexValidator(regex = '^[0-9-_+.]*$')])

  #   def clean_phone(self):
  #   	phone = self.cleaned_data['phone']
  #   	temp = str(phone)
  #   	if not temp.isdigit():
  #   		raise forms.ValidationError("Enter valid contact number.")
		# return phone

    def clean_last_name(self):

		last_name = self.cleaned_data['last_name']
		temp = last_name.replace(" ",'')

		for e in str(temp):
			if not e.isalnum():
				raise forms.ValidationError("Only Alphanuemaric")

		return last_name

    def clean_first_name(self):

    	first_name = self.cleaned_data['first_name']
        temp = first_name.replace(" ",'')

        for e in str(temp):
			if not e.isalnum():
				raise forms.ValidationError("Only Alphanuemaric")

        return first_name
	

    def __init__(self, user, *args, **kwargs):

        initial = ''
        if 'instance' in kwargs:
            initial = kwargs["instance"]
			
        if 'user' in kwargs:
            user = kwargs["user"]
            del kwargs["user"]
            
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
          
     
class RegisterForm(forms.Form):
	username = forms.CharField(
		label = _("Username"),
		max_length = 30,
		widget = forms.TextInput(),
		required = True,
		validators = [
		RegexValidator(
			regex = '^[a-zA-Z0-9-_+.]*$',
			message = 'Username required. 30 characters or fewer. \
			Letters, digits and @/./+/-/_ only.',
			code = 'invalid_username'
		),
		]
	)
	password = forms.CharField(
		label = _("Password"),
		widget = forms.PasswordInput(render_value = False),
		min_length = 8,
	)
	
	password_confirm = forms.CharField(
		label = _("Password (again)"),
		widget = forms.PasswordInput(render_value = False),
		min_length = 8,
	)
	email = forms.EmailField(
		label = _("Email"),
		widget = forms.TextInput(),
		required=True
	)
	
	def clean_username(self):
		try:
			User.objects.get(username=self.cleaned_data['username'])
			raise forms.ValidationError("This username has already existed.")
		except User.DoesNotExist:
			pass
			
			
	def clean_email(self):
		try:
			User.objects.get(email=self.cleaned_data['email'])
			raise forms.ValidationError("This email is already taken.")
		except User.DoesNotExist:
			pass	
			
	def clean_password_confirm(self):
		password = self.cleaned_data.get('password')
		password_confirm = self.cleaned_data.get('password_confirm')
		if password and password_confirm != password :
			raise forms.ValidationError('Passwords do not match')
		return self.cleaned_data