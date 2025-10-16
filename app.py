import streamlit as st
from model import predict_review
import re

st.set_page_config(page_title="Fake Review Identifier", page_icon="🕵️‍♀️", layout="wide")

def heuristic_flags(text):
    flags = []
    if text.count("!") > 3:
        flags.append("Many exclamation marks")
    if len(text.split()) < 15 and any(w in text.lower() for w in ["best", "amazing", "must buy", "perfect"]):
        flags.append("Short promotional phrasing")
    words = re.findall(r"\w+", text.lower())
    if any(words.count(w) > 4 for w in set(words)):
        flags.append("Lots of repeated words")
    return flags

def highlight_suspicious(text):
    suspicious = ["amazing","best","perfect","must buy","five stars","highly recommend","guarantee"]
    for w in suspicious:
        text = re.sub(fr"(?i)\b{w}\b", f"**{w}**", text)
    return text

st.title("🕵️‍♀️ Fake Review Identifier")
st.markdown("Paste a product review and the AI will predict whether it's likely **FAKE** or **REAL** — with a confidence score and quick explanations.")

with st.sidebar:
    st.header("Options")
    show_debug = st.checkbox("Show model debug output", value=False)
    show_flags = st.checkbox("Show heuristic flags", value=True)
    st.markdown("---")
    st.write("Try example reviews:")
    if st.button("Example — Likely Fake"):
        st.session_state.review_text = "This product is AMAZING!!! Best purchase ever, five stars, must buy! Loved it!!!"
    if st.button("Example — Likely Real"):
        st.session_state.review_text = "Battery lasts about two days with moderate use. Delivery was late by 2 days but overall satisfied with the build quality."

if "review_text" not in st.session_state:
    st.session_state.review_text = ""

review = st.text_area("Enter review text here:", value=st.session_state.review_text, height=200)

col1, col2 = st.columns([2,1])
with col2:
    if st.button("Analyze"):
        if not review.strip():
            st.warning("Please enter a review.")
        else:
            with st.spinner("Analyzing..."):
                label, confidence, raw = predict_review(review)
            label_upper = label.upper()
            if any(k in label_upper for k in ["FAKE","FALSE","DECEPTIVE"]):
                st.error(f"🚨 Prediction: **{label}** — {confidence}% confidence")
            else:
                st.success(f"✅ Prediction: **{label}** — {confidence}% confidence")

            if show_flags:
                flags = heuristic_flags(review)
                if flags:
                    st.info("Heuristic flags: " + ", ".join(flags))
                else:
                    st.info("No strong heuristic flags detected.")

            st.markdown("**Suspicious words (highlighted):**")
            st.markdown(highlight_suspicious(review))

            if show_debug:
                st.write("Model output (debug):")
                st.json(raw)
    else:
        st.write("Click **Analyze** to check the review.")

