import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from IndicTransToolkit.processor import IndicProcessor

MODEL_NAME = "ai4bharat/indictrans2-indic-en-dist-200M"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = None
model = None
processor = None


def load_translation_model():
    global tokenizer, model, processor

    print("Loading IndicTrans2 tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True
    )

    print("Loading IndicTrans2 model...")
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True
    )

    model.to(DEVICE)
    model.eval()

    processor = IndicProcessor(inference=True)

    print("IndicTrans2 ready on", DEVICE)


def translate_text(text):
    batch = processor.preprocess_batch(
        [text],
        src_lang="tel_Telu",
        tgt_lang="eng_Latn"
    )

    inputs = tokenizer(
        batch,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=256
    )

    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            num_beams=5,
            max_length=256
        )

    decoded = tokenizer.batch_decode(
        outputs,
        skip_special_tokens=True
    )

    return processor.postprocess_batch(
        decoded,
        lang="eng_Latn"
    )[0]
