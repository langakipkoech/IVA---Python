from email import message
from email.mime import audio
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import nltk
nltk.download('all')
#build a recognition

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['Go shopping','Clean room', 'Record Video']

#train model that will recognize intents and map them
def create_note():
    global recognizer

    #say something, what do you want to actually add to your note
    speaker.say('What do you want to write onto your note?')
    speaker.runAndWait()

    #wait for the user input and we gonna implement loop to ensure the program does not terminate
    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

            #extract text from audio

                note = recognizer.recognize_google(audio)
                note = note.lower()

            #chose a file name

                speaker.say('Choose a filename')
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f'I successfuly created the note {filename}')
                speaker.runAndWait()
#instance of an error
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say('I did not understand you. Please try again')
            speaker.runAndWait()

#to do list function
def add_todo():
    global recognizer

    speaker.say('what todo you want to add?')
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say(f" i added {item} to the todo list")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say('I did not understand you. Please try again')
            speaker.runAndWait()

def show_todos():

    speaker.say('The items on the to do list are the following')

    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def hello():
    speaker.say('hello what i can do for you')
    speaker.runAndWait()

def quit():
    speaker.say('Bye')
    speaker.runAndWait
    sys.exit(0)

#create a mapping dictionary
mappings = {
    "greetings": hello,
    "create_note": create_note,
    "add_todo":add_todo,
    "show_todos": show_todos,
    "exit": quit

}

assistant = GenericAssistant('intent.json', intent_methods=mappings )
assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            message = recognizer.recognize_google(audio)
            message = message.lower()
        assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()







