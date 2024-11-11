from django import forms
from .models import MyModel
#from .models import MyForm

class MyModelForm(forms.ModelForm):
    """
    text_string_0 = forms.CharField(
        label='Статический текст:',
        #initial='Это просто текст',
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    forms.CharField(
    label='Создать задачу на запись всех стримов с YouTube'
    )
    """
    text_string_1 = forms.CharField(
        label='Псевдоним канала:',
        initial='reuters',  # Текстовая строка с заданным текстом
        widget=forms.TextInput(attrs={'placeholder': 'Введите текст здесь'}),
        max_length=100
    )
    """
    button_1 = forms.CharField(
    widget=forms.HiddenInput(),  # Скрытый input для кнопки
    initial='Кнопка 1'
    )
    """
    """
    text_area = forms.CharField(
        label='Описание:',
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40})  # Текстовое поле
    )
    """
    dropdown_field = forms.ChoiceField(
        label='Частота проверки:',
        choices=[
            ('option1', 'Раз в 15 минут'),
            ('option2', 'Раз в 30 минут'),
            ('option3', 'Раз в 1 час'),
            ('option4', 'Раз в 2 часа'),
            #('option5', 'Option 5'),
        ]
    )
    """
    button_2 = forms.CharField(
    widget=forms.HiddenInput(),  # Скрытый input для кнопки
    initial='Кнопка 2'
    )
    """
    class Meta:
        model = MyModel
        #fields = ['text_string', 'text_area', 'dropdown_field']
        fields = ['text_string_1', 'dropdown_field']