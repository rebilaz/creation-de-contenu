from google.cloud import aiplatform
from vertexai.preview.language_models import GenerativeModel
import vertexai

def interroger_gemini(prompt_text: str) -> str:
    """
    Interroge le modèle Gemini 1.5 Pro sur Vertex AI avec gestion d'erreur.
    Nécessite l'authentification IAM fédérée (pas de clé API dans le code).
    """
    try:
        # Initialisation du contexte Vertex AI
        vertexai.init(project='starlit-verve-458814-u9', location='us-central1')
        # Instanciation du modèle Gemini
        model = GenerativeModel("gemini-1.5-pro-001")
        # Appel du modèle avec le prompt
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        print(f"Erreur lors de l'appel à Gemini : {e}")
        return f"❌ Erreur lors de l'appel à Gemini : {e}"

# Exemple d'utilisation
if __name__ == "__main__":
    prompt = "Explique en 3 points l'impact de la tokenisation des actifs sur la finance traditionnelle."
    resultat = interroger_gemini(prompt)
    print("Réponse Gemini :\n", resultat)
