from models import load_models, analyze_text, analyze_context

print("\nINITIALIZING MODELS...\n")

tokenizer, multitask, context = load_models()

print("\nTEST 1: TONE AND SARCASM")
result = analyze_text(
    "Nuvvu chala goppodivi!",
    tokenizer,
    multitask
)
print(result)

print("\nTEST 2: CONTEXT ANALYSIS")
result = analyze_context(
    "Nuvvu chala goppodivi!",
    "Avunu, nenu chaala goppodini!",
    tokenizer,
    context
)
print(result)

print("\nALL TESTS COMPLETED")
