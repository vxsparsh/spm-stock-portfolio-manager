from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User

    ticker = models.CharField(max_length=10)
    shares = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchase_date = models.DateField(default=date(2023, 9, 1))
    symbol = models.CharField(max_length=10, default="N/A")
    companyName = models.CharField(max_length=255, default="N/A")
    previousClose = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.00)
    marketCap = models.DecimalField(max_digits=20, decimal_places=2, null=True, default=0.00)
    returnYTD = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.00)
    peRatio = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.00)
    week52High = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.00)
    week52Low = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.00)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.00)

    def clean(self):
        self.ticker = self.ticker.upper()

    def __str__(self):
        return self.ticker


