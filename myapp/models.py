from django.db import models

# Create your models here.

class MyModel(models.Model):
    OPTION_CHOICES = [
            ('option1', 'Раз в 15 минут'),
            ('option2', 'Раз в 30 минут'),
            ('option3', 'Раз в 1 час'),
            ('option4', 'Раз в 2 часа'),
            #('option5', 'Option 5'),
        ]

    text_field = models.CharField(max_length=100)  # Текстовое поле
    dropdown_field = models.CharField(max_length=10, choices=OPTION_CHOICES)  # Выпадающий список

    def __str__(self):
        return self.text_field

class TaskChannel(models.Model):
    handle = models.CharField("Псевдоним", max_length=30)
    name = models.CharField("Имя", max_length=60)
    i_d = models.CharField("ID", max_length=24)
    checking_frequency = {
                    'option1': 'Раз в 15 минут',
                    'option2': 'Раз в 30 минут',
                    'option3': 'Раз в 1 час',
                    'option4': 'Раз в 2 часа',
                    }
    active = {
        0: 'False',
        1: 'True',
        }
    status = {
        1: 'Waiting for stream',
        2: 'Recordering',
        3: 'Error',
        }
    
    def __str__(self):
        return self.name
    
class Stream(models.Model):
    i_d = models.CharField("Stream ID", max_length=11)
    taskchannel_id = models.CharField("Channel ID", max_length=24)
    name = models.CharField("Имя", max_length=100)
    date = models.DateField("Дата")
    path = models.CharField("Путь к стриму", max_length=100)
    url = models.CharField("Ссылка на стрим", max_length=50)
    status = {
        1: 'On air',
        2: 'Ended'
        }
    
    def __str__(self):
        return self.name
    

class TaskModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)