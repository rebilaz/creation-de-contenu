# Fichier pour stocker tous les modèles de prompts pour les IA

SUJET_DE_TEST = "La tokenisation des actifs du monde réel (RWA) et son impact sur la finance traditionnelle."

PROMPT_IDEATION = """
Agis comme un analyste stratégique qui doit identifier une tendance émergente ou un angle mort pour une vidéo d'analyse financière pointue (date : juillet 2025). Le sujet doit être à l'intersection d'au moins un de ces trois thèmes : 1) Infrastructure Financière & Stablecoins, 2) Convergence TradFi & DeFi, 3) Géopolitique des Monnaies Numériques. Propose 3 sujets d'actualité sous forme de questions précises et percutantes.
"""

PROMPT_RECHERCHE_INITIALE = """
Agis comme un analyste financier. Construis une thèse d'investissement complète et sourcée sur le sujet suivant : "{sujet}". L'analyse doit inclure : 1) Le problème résolu, 2) Le modèle économique et les métriques clés, 3) Les avantages concurrentiels et le paysage concurrentiel, 4) Les risques et le cas baissier, 5) Les implications macro-économiques ou géopolitiques.
"""

PROMPT_CRITIQUE = """
Agis comme un analyste "red teamer" et un expert critique. Voici une première analyse sur le sujet de "{sujet}". Ta mission est de la challenger.
1. Identifie les points faibles, les simplifications excessives ou les angles morts de cette analyse.
2. Propose un point de vue opposé ou une thèse alternative (un "bear case" si l'analyse est "bullish", et vice versa).
3. Souligne les questions importantes qui restent sans réponse.
Ne te contente pas de résumer, apporte une réelle critique constructive et argumentée.
Voici l'analyse à critiquer :
{analyse_initiale}
"""

PROMPT_SYNTHESE_FINALE = """
Agis comme un expert pédagogue qui doit créer le document final le plus complet possible pour m'apprendre un sujet.
- Le Document 1 est une analyse initiale sur "{sujet}".
- Le Document 2 est une critique de cette première analyse, apportant un point de vue différent.
Ta mission est de fusionner ces deux documents en un seul texte final. Ce texte doit :
a) Présenter la thèse principale de manière claire.
b) Intégrer les contre-arguments et les risques soulevés dans la critique pour offrir une vision équilibrée et nuancée.
c) Être structuré de manière logique et didactique pour maîtriser le sujet de A à Z.
Voici le Document 1 :
{analyse_initiale}
Voici le Document 2 :
{critique}
"""

PROMPT_STRUCTURE_VIDEO = """
En te basant sur le texte final suivant, propose une structure de scénario détaillée pour une vidéo YouTube. Découpe le contenu en 4 à 5 parties logiques avec des titres clairs et des points clés pour chaque partie.
Voici le texte :
{texte_final}
"""

PROMPT_PLAN_MIRO = """
En te basant sur le texte final suivant, propose un plan détaillé pour un tableau Miro. Le plan doit inclure un nœud central, des branches principales pour chaque grande idée, et des feuilles pour les détails spécifiques, les exemples, et les arguments "pour" et "contre".
Voici le texte :
{texte_final}
"""
