from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Newsletter, Profile


# --- ФОРМА ВІДГУКУ ---
class ReviewForm(forms.ModelForm):
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


# --- ФОРМА ПІДПИСКИ НА РОЗСИЛКУ ---
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'newsletter-input',
                'placeholder': 'Ваш email...',
                'required': True
            }),
        }


# --- ФОРМА РЕЄСТРАЦІЇ ---
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, required=True, label="Ім'я",
        widget=forms.TextInput(attrs={'placeholder': "Ваше ім'я"})
    )
    email = forms.EmailField(
        required=True, label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'email@example.com'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        labels = {'username': 'Логін'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Додаємо всім полям клас для красивого відображення
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-input')

        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Підтвердження"
        self.fields['password1'].help_text = "Мінімум 8 символів."

    def save(self, commit=True):
        # 1. Зберігаємо базового користувача
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']

        if commit:
            # 2. Зберігаємо користувача в базу
            user.save()
            # 3. НАДІЙНО створюємо профіль (кешбек-рахунок)
            Profile.objects.get_or_create(user=user)

        return user


# --- ФОРМА ЗАМОВЛЕННЯ ---
class OrderForm(forms.Form):
    last_name = forms.CharField(label="Прізвище",
                                widget=forms.TextInput(attrs={'placeholder': 'Ваше прізвище', 'class': 'modern-input'}))
    first_name = forms.CharField(label="Ім'я",
                                 widget=forms.TextInput(attrs={'placeholder': "Ваше ім'я", 'class': 'modern-input'}))
    middle_name = forms.CharField(label="По батькові", required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'По батькові', 'class': 'modern-input'}))
    phone = forms.CharField(label="Телефон", widget=forms.TextInput(
        attrs={'placeholder': '+380...', 'class': 'modern-input phone-mask'}))

    city = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'id': 'city-input', 'autocomplete': 'off', 'class': 'modern-input'}))
    region = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'id': 'region-input', 'readonly': 'readonly', 'class': 'modern-input'}))
    warehouse = forms.CharField(required=False,
                                widget=forms.Select(attrs={'id': 'warehouse-select', 'class': 'modern-input'}))

    use_bonuses = forms.BooleanField(required=False, label="Списати бонуси для знижки")


# --- ФОРМА ПРОФІЛЮ (ДЛЯ ОСОБИСТОГО КАБІНЕТУ) ---
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['last_name', 'first_name', 'middle_name', 'phone', 'city', 'warehouse', 'index']
        labels = {
            'last_name': 'Прізвище',
            'first_name': "Ім'я",
            'middle_name': 'По батькові',
            'phone': 'Телефон',
            'city': 'Місто',
            'index': 'Індекс',
        }
        widgets = {
            'last_name': forms.TextInput(attrs={'placeholder': 'Ваше прізвище'}),
            'first_name': forms.TextInput(attrs={'placeholder': "Ваше ім'я"}),
            'middle_name': forms.TextInput(attrs={'placeholder': 'По батькові (необов\'язково)'}),
            'phone': forms.TextInput(attrs={'placeholder': '+380... (ваш номер)'}),
            'city': forms.TextInput(
                attrs={'id': 'city-input', 'autocomplete': 'off', 'placeholder': 'Почніть вводити назву міста...'}),
            'warehouse': forms.HiddenInput(attrs={'id': 'warehouse-final'}),
            'index': forms.TextInput(attrs={'placeholder': 'Поштовий індекс'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Автоматично додаємо клас 'modern-input' всім видимим полям
        for field in self.fields.values():
            if not isinstance(field.widget, forms.HiddenInput):
                field.widget.attrs.setdefault('class', 'modern-input')