from .models import WordForm


EXAMPLE_NOUN_FORMS = {
    "nimento": ["nominatiivi", "nimentö", "mikä? kuka?", "monikossa -t"],
    "kohdanto": ["akkusatiivi", "kohdanto", "kenet?", ""],
    "omanto": [
        "genetiivi",
        "omanto",
        "minkä? kenen?",
        "-n, -en, -in, -den, -ten, -tten",
    ],
    "olento": ["essiivi", "olento", "minä? millaisena? kenenä?", "-na, -nä"],
    "osanto": [
        "partitiivi",
        "osanto, eronto",
        "mitä? ketä?",
        "-a, -ä, -ta, -tä",
    ],
    "tulento": [
        "translatiivi",
        "tulento",
        "miksi? millaiseksi? keneksi?",
        "-ksi -kse (omistusliitteen yhteydessä)",
    ],
    "sisaolento": ["inessiivi", "sisäolento", "missä? kenessä?", "-ssa, -ssä"],
    "sisaeronto": ["elatiivi", "sisäeronto", "mistä? kenestä?", "-sta, -stä"],
    "sisatulento": [
        "illatiivi",
        "sisätulento",
        "mihin? keneen?",
        "-loppuvokaalin pidentymä + n  -han, hen, hin, hon, hun, hyn, hän, hön  -seen, -siin",
    ],
    "ulkoolento": ["adessiivi", "ulko-olento", "millä? kenellä?", "-lla, -llä"],
    "ulkoeronto": ["ablatiivi", "ulkoeronto", "miltä? keneltä)", "-lta, -ltä"],
    "ulkotulento": ["allatiivi", "ulkotulento", "mille? kenelle?", "-lle"],
    "vajanto": ["abessiivi", "vajanto", "mitä ilman?", "-tta, -ttä"],
    "keinonto": ["instruktiivi", "keinonto", "miten (keinoa, välinettä)", "-n"],
    "seuranto": ["komitatiivi", "seuranto", "minkä kanssa", "-in, -ine-"],
}

GRADATIONS = {
    "A": {"k": "kk", "kk": "k"},
    "B": {"p": "pp", "pp": "p"},
    "C": {"t": "tt", "tt": "t"},
    "D": {"k": "-", "-": "k"},
    "E": {"p": "v", "v": "p"},
    "F": {"t": "d", "d": "t"},
    "G": {"nk": "ng", "ng": "nk"},
    "H": {"mp": "mm", "mm": "mp"},
    "I": {"lt": "ll", "ll": "lt"},
    "J": {"nt": "nn", "nn": "nt"},
    "K": {"rt": "rr", "rr": "rt"},
    "L": {"l": "k", "k": "l"},
    "M": {"k": "v"},
    "_": {"_": "_"},
}

FORM_MAPPING = {
    "nimento": WordForm.Case.NOMINATIVE,
    "kohdanto": WordForm.Case.ACCUSATIVE,
    "omanto": WordForm.Case.GENITIVE,
    "olento": WordForm.Case.ESSIVE,
    "osanto": WordForm.Case.PARTITIVE,
    "tulento": WordForm.Case.TRANSLATIVE,
    "sisaolento": WordForm.Case.INESSIVE,
    "sisaeronto": WordForm.Case.ELATIVE,
    "sisatulento": WordForm.Case.ILLATIVE,
    "ulkoolento": WordForm.Case.ADESSIVE,
    "ulkoeronto": WordForm.Case.ABLATIVE,
    "ulkotulento": WordForm.Case.ALLATIVE,
    "vajanto": WordForm.Case.ABESSIVE,
    "keinonto": WordForm.Case.INSTRUCTIVE,
    "seuranto": WordForm.Case.COMITATIVE,
}
