import pyttsx3

moteur= pyttsx3.init()

def parler(texte):

        moteur.setProperty('rate', 75)
    
        voix = moteur.getProperty('voices')
        print(len(voix))
        moteur.setProperty('voice', voix[68].id)
    
        moteur.say(texte)
        moteur.runAndWait()

easter_egg = "I am a Darlek, prepare to die"
texte_a_dire="Be-en-vénu ah le E-U-Té de Bézié" 
parler(easter_egg)