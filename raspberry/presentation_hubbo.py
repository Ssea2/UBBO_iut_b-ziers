import pyttsx3

moteur= pyttsx3.init()

def parler(texte):

        moteur.setProperty('rate', 110)
    
        voix = moteur.getProperty('voices')
        print(len(voix))
        moteur.setProperty('voice', voix[26].id)
    
        moteur.say(texte)
        moteur.runAndWait()
        
        

#easter_egg = "I am a Darlek, prepare to die"
texte_a_dire="Bonjour à tous, je suis UBBO, un robot conçu dans le cadre d'un projet de la filière Robotique et Intelligence Artificielle, ou ROBIA. Les étudiants m'ont crée afin de résoudre des problèmes complexes, d'automatiser des tâches, et de créer des systèmes intelligents qui interagissent avec leur environnement" 
parler(texte_a_dire)