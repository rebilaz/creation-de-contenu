import os
import google.generativeai as genai
import openai
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# --- Configuration des clients API ---
# GitHub Copilot : Configure les clients pour Gemini et OpenAI ici en utilisant les clés d'API du .env

import asyncio

async def call_gemini(prompt_text: str) -> str:
    """
    Appel asynchrone à l'API Gemini (ex: gemini-1.5-pro).
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = await model.generate_content_async(
            prompt_text,
            generation_config={"temperature": 0.7, "max_output_tokens": 2048}
        )
        if hasattr(response, "text"):
            return response.text
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return "❌ Réponse inattendue de Gemini."
    except Exception as e:
        return f"❌ Erreur lors de l'appel à Gemini : {str(e)}"

async def call_chatgpt(prompt_text: str) -> str:
    """
    Appel asynchrone à l'API OpenAI (ex: gpt-4o).
    """
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.7,
            max_tokens=2048,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erreur lors de l'appel à ChatGPT : {str(e)}"
