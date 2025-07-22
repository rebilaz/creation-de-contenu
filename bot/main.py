import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import prompts
import api_clients

# Charger les variables d'environnement
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# --- Fonctions du Workflow ---

async def run_full_analysis_workflow(sujet: str, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    """
    Orchestre le workflow complet : recherche, critique, synthèse et livraison.
    """
    # Informer l'utilisateur que le processus commence
    await context.bot.send_message(chat_id=chat_id, text=f"✅ Reçu. Lancement de l'analyse sur le sujet : '{sujet}'...")

    # Phase 1: Recherche Initiale avec Gemini
    await context.bot.send_message(chat_id=chat_id, text="Phase 1/4 : Recherche initiale en cours avec Gemini...")
    prompt_v1 = prompts.PROMPT_RECHERCHE_INITIALE.format(sujet=sujet)
    analyse_v1 = api_clients.call_gemini(prompt_v1)

    # Phase 2: Challenge Critique avec ChatGPT
    await context.bot.send_message(chat_id=chat_id, text="Phase 2/4 : Challenge de l'analyse avec ChatGPT...")
    prompt_v2 = prompts.PROMPT_CRITIQUE.format(sujet=sujet, analyse_initiale=analyse_v1)
    critique_v1 = api_clients.call_chatgpt(prompt_v2)

    # Phase 3: Synthèse Finale avec Gemini
    await context.bot.send_message(chat_id=chat_id, text="Phase 3/4 : Synthèse finale en cours...")
    prompt_v3 = prompts.PROMPT_SYNTHESE_FINALE.format(sujet=sujet, analyse_initiale=analyse_v1, critique=critique_v1)
    texte_final = api_clients.call_gemini(prompt_v3)

    # Phase 4: Création des livrables
    await context.bot.send_message(chat_id=chat_id, text="Phase 4/4 : Création des livrables...")
    prompt_video = prompts.PROMPT_STRUCTURE_VIDEO.format(texte_final=texte_final)
    structure_video = api_clients.call_gemini(prompt_video)

    prompt_miro = prompts.PROMPT_PLAN_MIRO.format(texte_final=texte_final)
    plan_miro = api_clients.call_gemini(prompt_miro)
    
    # Livraison du rapport final
    final_report = f"--- RAPPORT D'ANALYSE FINAL ---\n\n{texte_final}\n\n--- STRUCTURE VIDÉO ---\n\n{structure_video}\n\n--- PLAN MIRO ---\n\n{plan_miro}"
    await context.bot.send_message(chat_id=chat_id, text=final_report)


# --- Gestionnaires de Commandes Telegram ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /start."""
    await update.message.reply_text("Bonjour ! Envoyez-moi un sujet d'analyse, ou tapez 'trouve' pour que je cherche un sujet pour vous.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les messages texte."""
    chat_id = update.message.chat_id
    message_text = update.message.text.lower().strip()

    if message_text == 'trouve':
        # GitHub Copilot : Implémente la logique pour la commande "trouve"
        # 1. Appeler l'IA avec prompts.PROMPT_IDEATION pour obtenir 3 sujets
        # 2. Envoyer les sujets à l'utilisateur (ou choisir le premier)
        # 3. Lancer run_full_analysis_workflow avec le sujet choisi
        await update.message.reply_text("Fonction 'trouve' en cours de développement...")

    else:
        # Le message est considéré comme un sujet manuel
        sujet = update.message.text
        await run_full_analysis_workflow(sujet, chat_id, context)

def main():
    """Fonction principale pour lancer le bot."""
    print("Lancement du bot...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Ajout des gestionnaires
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Lancement du bot
    print("Polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
