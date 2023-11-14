from django.db import models


class KafkaData(models.Model):
    latitude = models.DecimalField(max_digits=50, decimal_places=10)
    longitude = models.DecimalField(max_digits=50,decimal_places=10)
    id = models.CharField(max_length=20,primary_key=True)

    def __str__(self):
        return f'Sent: {self.latitude}, Received: {self.longitude}, Id : {self.id}'

