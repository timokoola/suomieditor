from .models import WordForm


EXAMPLE_NOUN_FORMS = {
    WordForm.Case.NOMINATIVE: ["nominatiivi", "nimentö", "mikä? kuka?", "monikossa -t"],
    WordForm.Case.ACCUSATIVE: ["akkusatiivi", "kohdanto", "kenet?", ""],
    WordForm.Case.GENITIVE: [
        "genetiivi",
        "omanto",
        "minkä? kenen?",
        "-n, -en, -in, -den, -ten, -tten",
    ],
    WordForm.Case.ESSIVE: [
        "essiivi",
        "olento",
        "minä? millaisena? kenenä?",
        "-na, -nä",
    ],
    WordForm.Case.PARTITIVE: [
        "partitiivi",
        "osanto, eronto",
        "mitä? ketä?",
        "-a, -ä, -ta, -tä",
    ],
    WordForm.Case.TRANSLATIVE: [
        "translatiivi",
        "tulento",
        "miksi? millaiseksi? keneksi?",
        "-ksi -kse (omistusliitteen yhteydessä)",
    ],
    WordForm.Case.INESSIVE: [
        "inessiivi",
        "sisäolento",
        "missä? kenessä?",
        "-ssa, -ssä",
    ],
    WordForm.Case.ELATIVE: ["elatiivi", "sisäeronto", "mistä? kenestä?", "-sta, -stä"],
    WordForm.Case.ILLATIVE: [
        "illatiivi",
        "sisätulento",
        "mihin? keneen?",
        "-loppuvokaalin pidentymä + n  -han, hen, hin, hon, hun, hyn, hän, hön  -seen, -siin",
    ],
    WordForm.Case.ADESSIVE: [
        "adessiivi",
        "ulko-olento",
        "millä? kenellä?",
        "-lla, -llä",
    ],
    WordForm.Case.ABLATIVE: [
        "ablatiivi",
        "ulkoeronto",
        "miltä? keneltä)",
        "-lta, -ltä",
    ],
    WordForm.Case.ALLATIVE: ["allatiivi", "ulkotulento", "mille? kenelle?", "-lle"],
    WordForm.Case.ABESSIVE: ["abessiivi", "vajanto", "mitä ilman?", "-tta, -ttä"],
    WordForm.Case.INSTRUCTIVE: [
        "instruktiivi",
        "keinonto",
        "miten (keinoa, välinettä)",
        "-n",
    ],
    WordForm.Case.COMITATIVE: ["komitatiivi", "seuranto", "minkä kanssa", "-in, -ine-"],
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
