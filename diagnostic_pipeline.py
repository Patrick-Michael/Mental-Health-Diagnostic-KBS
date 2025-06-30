from owlready2 import get_ontology, sync_reasoner, OwlReadyInconsistentOntologyError, ThingClass
from pathlib import Path
import uuid
import tempfile

def diagnose_patient(symptom_names):
    try:
        ONTOLOGY_FILENAME = "PatrickMentalHealthOntologyPython.rdf"
        onto_path = Path(__file__).parent / ONTOLOGY_FILENAME
        onto = get_ontology(str(onto_path)).load()

        with onto:
            # Create a unique patient individual
            patient_id = f"Patient_{uuid.uuid4().hex[:6]}"
            patient = onto.PatientProfile(patient_id)

            for symptom_name in symptom_names:
                symptom = getattr(onto, symptom_name, None)
                if symptom:
                    patient.hasSymptom.append(symptom)
                else:
                    return None

            # First reasoning pass (episodes)
            sync_reasoner()
            inferred_episodes = [
                cls for cls in patient.is_a
                if isinstance(cls, ThingClass) and "Episode" in cls.name
            ]

            if not inferred_episodes:
                return {"error": "❌ No episode could be inferred."}

            # Create episode individuals and link to patient
            for cls in inferred_episodes:
                episode_instance = cls(f"{cls.name}From_{patient_id}")
                patient.hasEpisode.append(episode_instance)

            # Save modified ontology
            tmp_rdf_path = Path(tempfile.gettempdir()) / f"mental_health_{uuid.uuid4().hex[:4]}.rdf"
            onto.save(file=str(tmp_rdf_path), format="rdfxml")

        # Reload for second inference (disorders)
        onto2 = get_ontology(f"file://{tmp_rdf_path.as_posix()}").load()
        with onto2:
            sync_reasoner()

        reloaded_patient = onto2.search_one(iri="*" + patient_id)
        if not reloaded_patient:
            return {"error": "❌ Patient not found in reloaded ontology."}

        inferred_disorders = [
            cls for cls in reloaded_patient.is_a
            if isinstance(cls, ThingClass) and "Disorder" in cls.name
        ]

        return {
            "symptom_info": [s.name for s in reloaded_patient.hasSymptom],
            "episodes": [e.name for e in reloaded_patient.hasEpisode],
            "disorders": [d.name for d in inferred_disorders],
        }

    except OwlReadyInconsistentOntologyError:
        return {"error": "❌ Ontology became inconsistent."}
    except Exception as e:
        return {"error": f"❌ Unexpected error: {str(e)}"}
