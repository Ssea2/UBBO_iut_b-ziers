import pyttsx3

moteur= pyttsx3.init()

def parler(texte):

        moteur.setProperty('rate', 110)
    
        voix = moteur.getProperty('voices')
        print(len(voix))
        moteur.setProperty('voice', voix[26].id)
    
        moteur.say(texte)
        moteur.runAndWait()


easter_egg = "I am a Darlek, prepare to die" 
truc_a_adire = [
        "Le programme sur les trois années de formation inclut des modules sur l'IT (Python, IA, Traitement d'image...) et OT (Automatisme, Instrumentation, Robotique...). Chaque année, les étudiants développent leurs compétences à travers des cours théoriques et des applications concrètes",
        "Les prérequis incluent une bonne maîtrise des mathématiques, des connaissances en programmation et un intérêt pour les technologies innovantes. Un diplôme de niveau Bac est nécessaire pour l'admission.",
        "Les diplômés peuvent travailler dans des domaines tels que la robotique industrielle, l'intelligence artificielle, Automaticien",
        "Oui, il est possible de suivre la formation en alternance à partir de la 2eme année, permettant aux étudiants de combiner théorie et pratique dans un environnement professionnel",
        "Les évaluations incluent des projets de groupe, et des contrôles continus sur la base des compétences acquises au cours des modules.",
]

def f_rep_qestion(question_n):
        parler(truc_a_adire[question_n-1])
