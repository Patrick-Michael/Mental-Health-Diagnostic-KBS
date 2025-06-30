# Mental-Health-Diagnostic-KBS
This is my project for the Knowledge-Based Systems module SS2025 THD.

The project aims to utilise an ontology of three major groups of disorders, MDD, BPD and anxiety disorder, to "diagnose patients" via assigning specific episodes from given symptoms.

It utilises an RDF ontology, a symptom map generated from the ontology, a streamlit GUI app with fuzzy matching as a feature, and a diagnostic pipeline using Python and HermiT.


Getting started: 

1. Download the project files into a known directory
2. Install dependencies: pip install -r requirements.txt
3. Run the program: streamlit run app_gui.py
   
The app will open in your browser at http://localhost:8501.

Note: Make sure PatrickMentalHealthOntologyPython.rdf is present in the project root folder.

How to use: 

Write symptoms in the text box and select from the menu. With fuzzy matching, it can approximate typos and show possible alternative names for symptoms. 


Example picture: 

Use the "Diagnose" button and wait for inferred symptoms, episodes, and disorders.
