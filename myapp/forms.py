from django import forms
from .models import MyModel

class MyModelForm(forms.ModelForm):
    name = forms.CharField(
        label='Псевдоним канала:',
        initial='reuters',  # Текстовая строка с заданным текстом
        widget=forms.TextInput(attrs={'placeholder': 'Введите текст здесь'}),
        max_length=100
    )

    # Закомментированный код теперь не имеет лишних отступов
    
    CHOICES = [
        (1, 'Раз в 1 минуту'),
        (5, 'Раз в 5 минут'),
        (15, 'Раз в 15 минут'),
        (30, 'Раз в 30 минут'),
        (60, 'Раз в 1 час'),
        (120, 'Раз в 2 часа'),
    ]

    interval = forms.ChoiceField(
        choices=CHOICES,
        label="Частота проверки:",
        required=False
    )
    

    class Meta:
        model = MyModel
        #fields = ['text_string_1', 'dropdown_field']
        fields = ['name', 'interval']

    def __init__(self, *args, **kwargs):
        super(MyModelForm, self).__init__(*args, **kwargs)
        # Устанавливаем значение по умолчанию для interval, если оно не передано
        if not self.instance.pk:
            self.fields['interval'].initial = 1  # Если объект не существует (новая форма), устанавливаем значение по умолчанию