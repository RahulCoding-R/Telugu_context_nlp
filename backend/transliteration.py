import torch
from ai4bharat.transliteration import XlitEngine

old_load = torch.load

torch.load = lambda *args, **kwargs: old_load(
    *args, **{**kwargs, "weights_only": False}
)

engine = XlitEngine("te", beam_width=10, rescore=True)

torch.load = old_load


def transliterate(text):
    return engine.translit_sentence(text, lang_code="te")
