from django.db import models


class Todo(models.Model):
    id = models.BigAutoField(primary_key=True)
    add_date = models.DateTimeField()
    content = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.content[:50]}"
