from django.db import models
from django.utils.translation import gettext as _
from decimal import Decimal

class housing_type(models.Model):
    # Assumption
    # Housing_type contains at least Landed, Condominium, HDB but is non-exhaustive
    housing_type = models.CharField(max_length = 50)

    def __str__(self):
        return self.housing_type


class Household(models.Model):
    housing_type = models.ForeignKey(housing_type, 
                                     on_delete = models.CASCADE, 
                                     blank=True, 
                                     null=True)


class household_individual(models.Model):
    householdID = models.ForeignKey(Household, 
                                    related_name='family_members', 
                                    on_delete=models.CASCADE, 
                                    blank=True, 
                                    null=True)

    name = models.CharField(max_length=100)
    gender = models.IntegerField(choices=((1, _("Male")), 
                                          (2, _("Female"))), default=1)
    marital_status = models.IntegerField(choices=((1, _("Single")), 
                                                  (2, _("Married")),
                                                  (3, _("Widowed")), 
                                                  (4, _("Separated")),
                                                  (5, _("Divorced")), 
                                                  (6, _("Not reported"))), default=1)
    spouse = models.CharField(max_length=100,
                              blank=True, 
                              default = "")
    occupation_type = models.IntegerField(choices=((1, _("Unemployed")), 
                                                   (2, _("Student")),
                                                   (3, _("Employed"))), default=1)

    annual_income = models.DecimalField(max_digits=10, 
                                        decimal_places=2,
                                        default = Decimal('0.00'))

    DOB = models.DateField()

    class Meta:
        unique_together = ['householdID', 'name']
        ordering = ['name']

    def __str__(self):
        return self.name