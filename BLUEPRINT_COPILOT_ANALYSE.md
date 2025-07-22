# Blueprint du Copilot d'Analyse Stratégique

## Mission Générale
Transformer un sujet d'investissement en une analyse complète, nuancée et multi-formats (texte de fond, structure vidéo, plan visuel), en utilisant une méthode de recherche et de critique croisée entre plusieurs IA.

---

## Déclencheur
- **Réception d'un sujet** (ex : "Thèse sur la tokenisation RWA") sur Telegram → SUJET = ce message.
- **Réception de la commande "trouve"** sur Telegram → SUJET = résultat du [Prompt d'Idéation].

---

## Phase 1 : Initialisation et Recherche Primaire

1. **Détermination de la variable SUJET**
   - Si message ≠ "trouve" → SUJET = message reçu.
   - Si message = "trouve" → SUJET = résultat du [Prompt d'Idéation].

2. **Appel API n°1 (Gemini)**
   - Prompt : [Prompt de Recherche Initiale]
   - Input : SUJET
   - Output : Analyse_V1

---

## Phase 2 : Challenge et Point de Vue Alternatif

1. **Appel API n°2 (ChatGPT)**
   - Prompt : [Prompt de Critique]
   - Inputs : SUJET, Analyse_V1
   - Output : Critique_V1

---

## Phase 3 : Synthèse Pédagogique et Création des Livrables

1. **Appel API n°1 (Gemini)**
   - Prompt : [Prompt de Synthèse Finale]
   - Inputs : SUJET, Analyse_V1, Critique_V1
   - Output : Texte_Final

2. **Appel API (Gemini ou ChatGPT)**
   - Prompt : [Prompt de Structure Vidéo]
   - Input : Texte_Final
   - Output : Structure_Video

3. **Appel API (Gemini ou ChatGPT)**
   - Prompt : [Prompt de Plan Miro]
   - Input : Texte_Final
   - Output : Plan_Miro

---

## Phase 4 : Livraison

1. **Formatage**
   - Assembler Texte_Final, Structure_Video, Plan_Miro dans un message clair et structuré.

2. **Envoi**
   - Renvoyer le message final à l'utilisateur via Telegram.

---

# Boîte à Outils du Copilot (Prompts à Copier-Coller)

## [Prompt d'Idéation (pour la commande "trouve")]
Agis comme un analyste stratégique qui doit identifier une tendance émergente ou un angle mort pour une vidéo d'analyse financière pointue (date : juillet 2025). Le sujet doit être à l'intersection d'au moins un de ces trois thèmes : 1) Infrastructure Financière & Stablecoins, 2) Convergence TradFi & DeFi, 3) Géopolitique des Monnaies Numériques. Propose 3 sujets d'actualité sous forme de questions précises et percutantes.

## [Prompt de Recherche Initiale]
Agis comme un analyste financier. Construis une thèse d'investissement complète et sourcée sur le sujet suivant : "[SUJET]". L'analyse doit inclure : 1) Le problème résolu, 2) Le modèle économique et les métriques clés, 3) Les avantages concurrentiels et le paysage concurrentiel, 4) Les risques et le cas baissier, 5) Les implications macro-économiques ou géopolitiques.

## [Prompt de Critique]
Agis comme un analyste "red teamer" et un expert critique. Voici une première analyse sur le sujet de "[SUJET]". Ta mission est de la challenger.
1. Identifie les points faibles, les simplifications excessives ou les angles morts de cette analyse.
2. Propose un point de vue opposé ou une thèse alternative (un "bear case" si l'analyse est "bullish", et vice versa).
3. Souligne les questions importantes qui restent sans réponse.
Ne te contente pas de résumer, apporte une réelle critique constructive et argumentée.
Voici l'analyse à critiquer :
[coller le contenu de la variable Analyse_V1]

## [Prompt de Synthèse Finale]
Agis comme un expert pédagogue qui doit créer le document final le plus complet possible pour m'apprendre un sujet.
- Le Document 1 est une analyse initiale sur "[SUJET]".
- Le Document 2 est une critique de cette première analyse, apportant un point de vue différent.
Ta mission est de fusionner ces deux documents en un seul texte final. Ce texte doit :
a) Présenter la thèse principale de manière claire.
b) Intégrer les contre-arguments et les risques soulevés dans la critique pour offrir une vision équilibrée et nuancée.
c) Être structuré de manière logique et didactique pour maîtriser le sujet de A à Z.
Voici le Document 1 :
[coller le contenu de la variable Analyse_V1]
Voici le Document 2 :
[coller le contenu de la variable Critique_V1]

## [Prompt de Structure Vidéo]
En te basant sur le texte final suivant, propose une structure de scénario détaillée pour une vidéo YouTube. Découpe le contenu en 4 à 5 parties logiques avec des titres clairs et des points clés pour chaque partie.
Voici le texte :
[coller le contenu de la variable Texte_Final]

## [Prompt de Plan Miro]
En te basant sur le texte final suivant, propose un plan détaillé pour un tableau Miro. Le plan doit inclure un nœud central, des branches principales pour chaque grande idée, et des feuilles pour les détails spécifiques, les exemples, et les arguments "pour" et "contre".
Voici le texte :
[coller le contenu de la variable Texte_Final]
