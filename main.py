"""
Ce projet a pour but de creer un assistant vocal pour transcrire des taches en utilisant python pour un project scolaire.
"""
from neuralintents import GenericAssistant
import speech_recognition as sr
import pyttsx3 as tts
import sys

recognizer = sr.Recognizer()

speaker = tts.init()
speaker.setProperty('rate',150)
speaker.setProperty('volume',0.9) 

todo_list = ["Faire les courses","Nettoyer la chambre"]

def create_noto():
    """
    Cette fonction creer une nouvelle tache, ouvre le micro et attend un ordre. Des que l'utilisateur finit d'enumerer ses ordres, la fonction lui demande le nom d'enregistrement de son fichier avec l'extension.
    """
    global recognizer
    
    speaker.say("Qu'est-ce que vous voulez noter?")
    speaker.runAndWait()
    
    done = False
    
    while not done:
        try:            
            with sr.Microphone() as mic:
                
                recognizer.adjust_for_ambient_noise(mic,duration=1)
                audio = recognizer.listen(mic)
                
                note = recognizer.recognize_google(audio,language="fr-FR")
                note = note.lower()
                
                speaker.say("Choisissez un nom fichier")
                speaker.runAndWait()
                
                recognizer.adjust_for_ambient_noise(mic, duration=1)
                audio = recognizer.listen(mic)
                filename = recognizer.recognize_google(audio,language="fr-FR")
                filename = filename.lower()
                
            with open(filename,'w') as f:
                f.write(note)
                done = True
                speaker.say(f"La note a ete cree avec succes {filename}")
                speaker.runAndWait()
                
        except sr.UnknownValueError:   
            recognizer = sr.Recognizer()
            speaker.say("Je n'ai pas compris, repetez")
            speaker.runAndWait()
            
def add_todo():
    """
    Cette fonction perment d'ajouter une tache.
    """
    global recognizer
    speaker.say("Qu'est-ce que vous voulez ajouter?")
    speaker.runAndWait()
    
    done = False
    
    while not done:
        try:
            with sr.Microphone() as mic:
                
                recognizer.adjust_for_ambient_noise(mic,duration=1)
                audio = recognizer.listen(mic)
                
                item = recognizer.recognize_google(audio,language="fr-FR")
                item = item.lower()
                
                todo_list.append(item)
                done = True
                
                speaker.say(f"J'ai ajouter{item} a la todo-list")
                speaker.runAndWait()
                
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("Je n'ai pas compris, repetez")
            speaker.runAndWait()
            
def show_todos():
    """
    Cette fonction permet d'énoncer toutes les taches enregistrées.
    """
    speaker.say("Voici votre liste des choses a faire:")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def hello():
    
    speaker.say("Bonjour, que puis-je faire pour vous?")
    speaker.runAndWait()



def bye():
    speaker.say("Au revoir!")
    speaker.runAndWait()
    os.exit(0)

    
mapping = {
    "salutations": hello(),
    "creation_note": create_noto(),
    "add_note": add_todo(),
    "show_todos": show_todos(),
    "exit": bye(),
    }


assistant = GenericAssistant('intents.json', intent_methods=mapping)
assistant.train_model()
assistant.save_model()

while True:
    
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            audio = recognizer.listen(mic)            
            message = recognizer.recognize_google(audio,language="fr-FR")
            message = message.lower()

        assistant.request(message)
        
    except:
        recognizer = sr.Recognizer()