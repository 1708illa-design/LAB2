from django import forms
from .models import Review, Newsletter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    # Жорстко перебиваємо дефолтну логіку Django, щоб було рівно 5 зірок
    rating = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        widget=forms.RadioSelect(),
        label='Оцінка'
    )

    class Meta:
        model = Review
        fields = ['author', 'text', 'rating']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Ваше ім'я"}),
            'text': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Напишіть ваш відгук...', 'rows': 4}),
        }
        labels = {
            'author': "Ваше ім'я",
            'text': 'Відгук',
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'newsletter-input', 'placeholder': 'Ваш email...'}),
        }
        labels = {
            'email': '',
        }

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        label="Ім'я",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Ваше ім'я"})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-input')

class OrderForm(forms.Form):
    city = forms.CharField(
        max_length=100,
        label="Місто",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введіть місто...',
            'id': 'city-input',
            'autocomplete': 'off',
        })
    )
    warehouse = forms.CharField(
        max_length=200,
        label="Відділення Нової Пошти",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Оберіть відділення...',
            'id': 'warehouse-input',
            'autocomplete': 'off',
        })
    )