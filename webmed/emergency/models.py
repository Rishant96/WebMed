from django.db import models
# from django.contrib.postgres.fields import ArrayField


class Variety(models.Model):
    name = models.CharField(max_length=50)
    condition = models.ForeignKey('Condition',
                                  on_delete=models.CASCADE,
                                  related_name='varieties')

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Emergency_Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Create your models here.
class Emergency(models.Model):

    group = models.ForeignKey('Emergency_Group',
                              on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

    is_priority = models.BooleanField(default=False)

    conditions = models.ManyToManyField(Condition,
        through='Presenting_Complaint',
        through_fields=('emergency', 'condition'))

    age_min = models.IntegerField(default=12)
    age_max = models.IntegerField(default=60)

    MALE = 'M'
    FEMALE = 'F'
    BOTH = 'MF'

    GENDER_CHOICES = [
        (BOTH, 'Both'),
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    genders_affected = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default=BOTH,
    )


class Presenting_Complaint(models.Model):
    emergency = models.ForeignKey(Emergency, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE,
        limit_choices_to={'condition': condition})
