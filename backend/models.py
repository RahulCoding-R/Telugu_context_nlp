
from pathlib import Path

import torch
import torch.nn as nn
from transformers import (
    AutoConfig,
    AutoModel,
    AutoModelForSequenceClassification,
    AutoTokenizer
)

ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT / "models"

MULTITASK_DIR = MODEL_DIR / "multitask_model"
CONTEXT_DIR = MODEL_DIR / "context_model"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

TONE_LABELS = ["angry", "fear", "happy", "no", "sad"]


class TeluguToneModel(nn.Module):
    def __init__(self, config):
        super().__init__()

        self.encoder = AutoModel.from_config(config)
        hidden = self.encoder.config.hidden_size

        self.dropout = nn.Dropout(0.2)
        self.tone_head = nn.Linear(hidden, 5)

    def forward(self, input_ids, attention_mask, token_type_ids=None):
        encoder_inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask
        }

        if token_type_ids is not None:
            encoder_inputs["token_type_ids"] = token_type_ids

        output = self.encoder(**encoder_inputs)

        pooled = output.last_hidden_state[:, 0]
        pooled = self.dropout(pooled)

        return self.tone_head(pooled)


def load_models():
    print("Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        str(CONTEXT_DIR),
        local_files_only=True
    )

    print("Loading tone model...")

    config = AutoConfig.from_pretrained(
        str(CONTEXT_DIR),
        local_files_only=True
    )

    tone_model = TeluguToneModel(config)

    weights = torch.load(
        MULTITASK_DIR / "model.pt",
        map_location="cpu",
        weights_only=True
    )

    result = tone_model.load_state_dict(weights, strict=False)

    del weights

    if result.missing_keys or set(result.unexpected_keys) != {
        "sarcasm_head.weight",
        "sarcasm_head.bias"
    }:
        raise RuntimeError(
            f"Unexpected checkpoint mismatch: "
            f"missing={result.missing_keys}, "
            f"unexpected={result.unexpected_keys}"
        )

    print("Original tone weights loaded successfully.")

    print("Loading context model...")

    context_model = AutoModelForSequenceClassification.from_pretrained(
        str(CONTEXT_DIR),
        local_files_only=True
    )

    tone_model.to(DEVICE).eval()
    context_model.to(DEVICE).eval()

    print("Tone and context models loaded successfully.")
    print("Device:", DEVICE)

    return tokenizer, tone_model, context_model


def analyze_text(text, tokenizer, model):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )

    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.inference_mode():
        tone_logits = model(**inputs)
        tone_probs = torch.softmax(tone_logits, dim=1)[0]

    tone_id = tone_probs.argmax().item()

    return {
        "tone": TONE_LABELS[tone_id],
        "tone_confidence": round(
            tone_probs[tone_id].item() * 100, 2
        )
    }


def analyze_context(context, reply, tokenizer, model):
    inputs = tokenizer(
        context,
        reply,
        return_tensors="pt",
        truncation=True,
        max_length=256
    )

    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.inference_mode():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=1)[0]

    prediction = probs.argmax().item()

    return {
        "prediction_id": prediction,
        "pair_class": ["negative_pair", "positive_pair"][prediction],
        "confidence": round(probs[prediction].item() * 100, 2)
    }
