from django.db import models

# Create your models here.


class BaseForm(models.Model):
    word = models.CharField(max_length=100, default="")
    declension = models.IntegerField(default=0)
    gradation = models.CharField(max_length=1, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.word} ({self.declension}, {self.gradation})"


class WordForm(models.Model):
    class Number(models.IntegerChoices):
        SINGULAR = 1
        PLURAL = 2

    class Case(models.TextChoices):
        NOMINATIVE = "nominative"
        ACCUSATIVE = "accusative"
        GENITIVE = "genitive"
        PARTITIVE = "partitive"
        INESSIVE = "inessive"
        ELATIVE = "elative"
        ILLATIVE = "illative"
        ADESSIVE = "adessive"
        ABLATIVE = "ablative"
        ALLATIVE = "allative"
        ESSIVE = "essive"
        TRANSLATIVE = "translative"
        ABESSIVE = "abessive"
        INSTRUCTIVE = "instructive"
        COMITATIVE = "comitative"

        # foreignkey to BaseForm

    baseform = models.ForeignKey(BaseForm, on_delete=models.CASCADE)
    wordform = models.CharField(max_length=100, default="")
    number = models.IntegerField(choices=Number.choices)
    case = models.CharField(max_length=20, choices=Case.choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        number_pretty = "singular" if self.number == 1 else "plural"
        return f"{self.wordform} ({number_pretty}, {self.case} of {self.baseform.word})"
