from django.db import models
# from django.contrib.postgres.fields import ArrayField


class Variety(models.Model):
    name = models.CharField(max_length=50)
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE)


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
    is_priority = models.BooleanField(default=False)

    age_min = models.IntegerField()
    age_max = models.IntegerField()

    in_males = models.BooleanField(default=True)
    in_females = models.BooleanField(default=True)

    conditions = models.ManyToManyField(Condition)

    group = models.ForeignKey('Emergency_Group', on_delete=models.CASCADE,
                              null=True)

    name = models.CharField(max_length=50)
