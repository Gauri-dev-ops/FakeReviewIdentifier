from transformers import pipeline

# Public model for fake review detection
MODEL_NAME = "debojit01/fake-review-detector"
classifier = pipeline("text-classification", model=MODEL_NAME, truncation=True)

def predict_review(text: str):
    out = classifier(text, truncation=True)[0]
    label = out.get("label", "LABEL")
    confidence = round(float(out.get("score", 0.0)) * 100, 2)
    return label, confidence, out
