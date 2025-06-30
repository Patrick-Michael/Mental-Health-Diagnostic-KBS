import streamlit as st
from diagnostic_pipeline import diagnose_patient
from owlready2 import get_ontology
from pathlib import Path
from symptom_map import symptom_map

st.set_page_config(page_title="Mental Health Diagnostic Tool", layout="centered")
st.title("🧠 Mental Health Diagnostic Tool")
st.markdown(
    "Select symptoms from the dropdown. "
    "The system will infer your likely mental health episode(s) and condition(s)."
)

# --- DROPDOWN SELECTION ---
st.subheader("📋 Select Known Symptoms")

# Build labeled dropdown: "Fatigue (tired, exhausted)" → "Fatigue1"
dropdown_labels = {
    f"{item['display']} ({', '.join(item['variants'])})": item["individual"]
    for item in symptom_map
}
dropdown_display_names = list(dropdown_labels.keys())

selected_labels = st.multiselect("🔍 Select your symptoms from the list:", options=dropdown_display_names)
selected_dropdown = [dropdown_labels[label] for label in selected_labels]

# --- DIAGNOSIS ---
if st.button("🧠 Diagnose"):
    if not selected_dropdown:
        st.warning("⚠️ Please select at least one symptom.")
    else:
        with st.spinner("📚 Loading ontology and running diagnosis..."):
            onto_path = Path(__file__).parent / "PatrickMentalHealthOntologyPython.rdf"
            onto = get_ontology(str(onto_path)).load()
            result = diagnose_patient(selected_dropdown)

        if not result or "symptom_info" not in result:
            st.error("❌ No results were returned from the diagnostic engine.")
        else:
            st.subheader("🧾 Selected Symptoms")
            for s in result["symptom_info"]:
                st.write(f"- {s}")

            if result.get("episodes"):
                st.subheader("📘 Inferred Episode(s)")
                for ep in result["episodes"]:
                    st.success(f"🧩 {ep}")

            if result.get("disorders"):
                st.subheader("🏥 Inferred Disorder(s)")
                for dis in result["disorders"]:
                    st.success(f"⚠️ {dis}")
