from django.db import models

# Create your models here.


class ExampleCache(models.Model):
    declension = models.IntegerField(default=0)
    gradation = models.CharField(max_length=1, default="")
    size = models.IntegerField(default=0)
    examples = models.TextField(default="")

    class Meta:
        unique_together = ["declension", "gradation"]

    # TODO: maybe migrate to ids instead of words?
    def example_baseforms(self):
        for example in self.examples.split(", "):
            yield BaseForm.objects.get(
                word=example, declension=self.declension, gradation=self.gradation
            )

    def __str__(self):
        return f"{self.declension}, {self.gradation} ({self.size}): {self.examples}"


class BaseForm(models.Model):
    word = models.CharField(max_length=100, default="")
    declension = models.IntegerField(default=0)
    gradation = models.CharField(max_length=1, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["word", "declension", "gradation"]

    def __str__(self):
        return f"{self.word} ({self.declension}, {self.gradation})"


class WordForm(models.Model):
    class Number(models.IntegerChoices):
        SINGULAR = 1
        PLURAL = 2

    class Case(models.TextChoices):
        NOMINATIVE = "nominative"
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
        ACCUSATIVE = "accusative"

        # foreignkey to BaseForm

    class Source(models.TextChoices):
        KOTUS = "kotus"
        COLLECTOR = "collector"
        EDITOR = "editor"

    baseform = models.ForeignKey(BaseForm, on_delete=models.CASCADE)
    wordform = models.CharField(max_length=100, default="")
    number = models.IntegerField(choices=Number.choices)
    case = models.CharField(max_length=20, choices=Case.choices)
    source = models.CharField(max_length=20, choices=Source.choices, default="kotus")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["baseform", "wordform", "number", "case"]

    def __str__(self):
        number_pretty = "singular" if self.number == 1 else "plural"
        return f"{self.wordform} ({number_pretty}, {self.case} of {self.baseform.word})"

    def url(self):
        return f"/editor/{self.baseform.id}/"
