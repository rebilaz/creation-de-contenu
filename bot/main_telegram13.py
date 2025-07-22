import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import prompts
import api_clients

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Fonction utilitaire pour découper et envoyer de longs messages

def send_long_message(bot, chat_id, text, header=None):
    max_length = 4096
    if header:
        bot.send_message(chat_id=chat_id, text=header)
    for i in range(0, len(text), max_length):
        bot.send_message(chat_id=chat_id, text=text[i:i+max_length])

# Workflow principal (synchrone)
def run_full_analysis_workflow(sujet, chat_id, bot, user_data):
    try:
        bot.send_message(chat_id=chat_id, text="✅ Reçu. Lancement de l'analyse sur le sujet : '{}'...".format(sujet))
        # Phase 1: Recherche Initiale avec Gemini
        bot.send_message(chat_id=chat_id, text="Phase 1/4 : Recherche initiale en cours avec Gemini...")
        prompt_v1 = prompts.PROMPT_RECHERCHE_INITIALE.format(sujet=sujet)
        analyse_v1 = api_clients.call_gemini(prompt_v1)
        if callable(analyse_v1):
            analyse_v1 = analyse_v1()
        # Phase 2: Challenge Critique avec ChatGPT
        bot.send_message(chat_id=chat_id, text="Phase 2/4 : Challenge de l'analyse avec ChatGPT...")
        prompt_v2 = prompts.PROMPT_CRITIQUE.format(sujet=sujet, analyse_initiale=analyse_v1)
        critique_v1 = api_clients.call_chatgpt(prompt_v2)
        if callable(critique_v1):
            critique_v1 = critique_v1()
        # Phase 3: Synthèse Finale avec Gemini
        bot.send_message(chat_id=chat_id, text="Phase 3/4 : Synthèse finale en cours...")
        prompt_v3 = prompts.PROMPT_SYNTHESE_FINALE.format(sujet=sujet, analyse_initiale=analyse_v1, critique=critique_v1)
        texte_final = api_clients.call_gemini(prompt_v3)
        if callable(texte_final):
            texte_final = texte_final()
        # Phase 4: Création des livrables
        bot.send_message(chat_id=chat_id, text="Phase 4/4 : Création des livrables...")
        prompt_video = prompts.PROMPT_STRUCTURE_VIDEO.format(texte_final=texte_final)
        structure_video = api_clients.call_gemini(prompt_video)
        if callable(structure_video):
            structure_video = structure_video()
        prompt_miro = prompts.PROMPT_PLAN_MIRO.format(texte_final=texte_final)
        plan_miro = api_clients.call_gemini(prompt_miro)
        if callable(plan_miro):
            plan_miro = plan_miro()
        # Livraison du rapport final (découpé)
        send_long_message(bot, chat_id, texte_final, header="--- SYNTHÈSE FINALE ---")
        send_long_message(bot, chat_id, structure_video, header="--- STRUCTURE VIDÉO ---")
        send_long_message(bot, chat_id, plan_miro, header="--- PLAN MIRO ---")
    except Exception as e:
        bot.send_message(chat_id=chat_id, text="❌ Une erreur est survenue dans le workflow : {}".format(str(e)))

# Gestionnaires Telegram

def start_command(update, context):
    update.message.reply_text("Bonjour ! Envoyez-moi un sujet d'analyse, ou tapez 'trouve' pour que je cherche un sujet pour vous.")

def handle_message(update, context):
    chat_id = update.message.chat_id
    message_text = update.message.text.lower().strip()
    user_data = context.user_data
    if message_text == 'trouve':
        ideation_response = api_clients.call_gemini(prompts.PROMPT_IDEATION)
        if callable(ideation_response):
            ideation_response = ideation_response()
        sujets = []
        for line in ideation_response.splitlines():
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                sujet = line.split(" ", 1)[-1].strip(":-. ")
                sujets.append(sujet)
        if len(sujets) < 3:
            sujets = [s.strip() for s in ideation_response.split("\n") if s.strip()][:3]
        keyboard = [
            [InlineKeyboardButton("Sujet {}".format(i+1), callback_data="sujet_{}".format(i))]
            for i in range(len(sujets))
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        user_data['sujets_trouves'] = sujets
        update.message.reply_text(
            "Voici des sujets proposés. Choisissez-en un pour lancer l'analyse :",
            reply_markup=reply_markup
        )
    else:
        sujet = update.message.text
        run_full_analysis_workflow(sujet, chat_id, context.bot, user_data)

def button_callback_handler(update, context):
    query = update.callback_query
    data = query.data
    user_data = context.user_data
    if data.startswith("sujet_"):
        idx = int(data.split("_")[1])
        sujets = user_data.get('sujets_trouves', [])
        if 0 <= idx < len(sujets):
            sujet_choisi = sujets[idx]
            query.edit_message_text("Vous avez choisi : {}\n\nLancement de l'analyse...".format(sujet_choisi))
            run_full_analysis_workflow(sujet_choisi, query.message.chat_id, context.bot, user_data)
        else:
            query.edit_message_text("❌ Sujet non trouvé. Veuillez réessayer.")

def main():
    print("Lancement du bot...")
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button_callback_handler))
    print("Polling...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
