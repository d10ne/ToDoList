from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание', max_length=255)
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return ', '.join([self.title, self.description, str(self.user_id)])

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['created']
