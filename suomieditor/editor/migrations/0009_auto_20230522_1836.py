# Generated by Django 4.2.1 on 2023-05-22 18:36

import datetime
import json
from django.db import migrations
import os

FORM_MAPPING = {
    "nimento": "NOMINATIVE".lower(),
    "kohdanto": "ACCUSATIVE".lower(),
    "omanto": "GENITIVE".lower(),
    "olento": "ESSIVE".lower(),
    "osanto": "PARTITIVE".lower(),
    "tulento": "TRANSLATIVE".lower(),
    "sisaolento": "INESSIVE".lower(),
    "sisaeronto": "ELATIVE".lower(),
    "sisatulento": "ILLATIVE".lower(),
    "ulkoolento": "ADESSIVE".lower(),
    "ulkoeronto": "ABLATIVE".lower(),
    "ulkotulento": "ALLATIVE".lower(),
    "vajanto": "ABESSIVE".lower(),
    "keinonto": "INSTRUCTIVE".lower(),
    "seuranto": "COMITATIVE".lower(),
}


def process_file(f, filename, apps):
    """Process a file of wordforms"""
    # line looks like this:
    # {"av": "_", "tn": 44, "word": "kevät", "BOOKWORD": "keväällä", "BASEFORM": "kevät", "CLASS": "nimisana",
    #  "NUMBER": "singular", "SIJAMUOTO": "ulkoolento", }
    # get the date from the filename, filename is {epoch time}.jsonl or output.jsonl
    # We can't import the BaseForm model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    BaseForm = apps.get_model("editor", "BaseForm")
    WordForm = apps.get_model("editor", "WordForm")
    # if output.jsonl, use Febraury 1st 2023
    if filename == "output.jsonl":
        timestamp = 1675324800
    else:
        timestamp = int(filename.split(".")[0])

    # turn timestamp into datetime
    timestamp = datetime.datetime.fromtimestamp(timestamp)
    # add UTC timezone
    timestamp = timestamp.replace(tzinfo=datetime.timezone.utc)

    # run line by line
    for line in f:
        linejson = json.loads(line)

        # check that all the fields are there
        # if not, just continue
        if (
            "BASEFORM" not in linejson
            or "NUMBER" not in linejson
            or "SIJAMUOTO" not in linejson
        ):
            continue
        baseform = linejson["BASEFORM"]
        # find the baseform from the database
        try:
            baseform = BaseForm.objects.get(word=baseform)
        except BaseForm.DoesNotExist:
            continue
        except BaseForm.MultipleObjectsReturned:
            # if multiple objects returned, use the first one
            baseform = BaseForm.objects.filter(word=baseform).first()
            # print("Multiple objects returned for {}".format(baseform.word))

        form_number = 1 if linejson["NUMBER"] == "singular" else 2

        form_case = FORM_MAPPING[linejson["SIJAMUOTO"]]

        # skip nimento singular
        if form_case == "nominative" and form_number == 1:
            continue

        # check if the wordform already exists
        # if it does, skip it
        if (
            WordForm.objects.filter(baseform=baseform)
            .filter(wordform=linejson["BOOKWORD"])
            .filter(number=form_number)
            .filter(case=form_case)
            .exists()
        ):
            continue

        word, created = WordForm.objects.update_or_create(
            baseform=baseform,
            wordform=linejson["BOOKWORD"],
            number=form_number,
            source="collector",
            case=form_case,
            timestamp=timestamp,
        )
        if created:
            word.save()


def download_wordfroms_from_object_storage(apps, schema_editor):
    # first make sure downloads directory exists
    if not os.path.exists("downloads"):
        os.mkdir("downloads")

    # corfirm that environment variable for bucket name is set
    bucket_name = os.environ.get("BUCKET_NAME")
    if not bucket_name:
        raise Exception("Environment variable BUCKET_NAME is not set")

    # then download the wordforms
    # use gsutil to download the wordforms
    os.system("gsutil -m cp -r gs://{}/*.jsonl downloads/".format(bucket_name))

    # iterate over the files in the downloads directory
    for filename in os.listdir("downloads"):
        # if not a jsonl file, skip it
        if not filename.endswith(".jsonl"):
            continue
        # proess the file
        with open("downloads/{}".format(filename), "r") as f:
            process_file(f, filename, apps)


class Migration(migrations.Migration):
    dependencies = [
        ("editor", "0008_wordform_source"),
    ]

    operations = [migrations.RunPython(download_wordfroms_from_object_storage)]
