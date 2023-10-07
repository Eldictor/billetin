import speech_recognition as sr
import subprocess as sub
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, colors, os
from tkinter import *
from pygame import mixer
from PIL import Image, ImageTk
import threading as tr
import database
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import utc

main_window=Tk()
main_window.title("Billetin AI")
main_window.geometry("300x300")
main_window.resizable(0,0)
main_window.configure(bg='#000000')

def conversar(rec):
    chat=ChatBot("Billetin",database_uri=None)
    trainer=ListTrainer(chat)
    trainer.train(database.get_question_answers())
    talk("Vamos a conversar...")
    while True:
        try:
            request = listen("")
        except UnboundLocalError:
            print("No te entendí, intenta de nuevo")
            continue    
        print("Tu"+request)
        answer=chat.get_response(request)
        print("Billetin"+answer)
        talk(answer)
        if 'chao' in request:
            break


label_title= Label(main_window, text="Billetin IA", bg="#6DD5FA",fg="#2c3e50",
                   font=('Arial', 30, "bold"))
label_title.pack(pady=10)  

def mexican_voice():
    change_voice(1)
    pass
def english_voice():
    change_voice(0)
    pass
def spain_voice():
    change_voice(2)
    pass
def change_voice(id):
    engine.setProperty('voice',voices[id].id)
    engine.setProperty('rate',145)
    talk("Hola soy billetin   ")

name="Billetin"
listener=sr.Recognizer()
engine=pyttsx3.init()

voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate',145)

def give_me_name():
    talk("Hola,¿cómo te llamas?")
    name=listen("Te escucho")
    name=name.strip()
    talk(f"Bienvenido {name}")

    try:
        with open("name.txt", 'w') as f:
            f.write(name)
    except FileNotFoundError:
            file=open("name.txt",'w')
            file.write(name)

def say_hello():
    if os.path.exists("name.txt") :
        with open("name.txt") as f:
            for name in f:
                talk(f"Hola, bienvenido {name}")
    else:
        give_me_name()

def thread_hello():
    t=tr.Thread(target=say_hello)
    t.start
    thread_hello()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen(phrase=None):
    listener = sr.Recognizer()     
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        talk(phrase)
        pc = listener.listen(source)

    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError:
        print("No te entendí, intenta de nuevo")
        if name in rec:
            rec = rec.replace(name, '')
    return rec

def run_billetin():
    while True:
        try:
            rec = listen("Te escucho")
        except UnboundLocalError:
            print("No te entendí, intenta de nuevo")
            continue     
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search=rec.replace('busca','')
            wikipedia.set_lang('es')
            wiki=wikipedia.summary(search, 1)
            print(search +":"+wiki)
            talk(wiki)
            break
        elif 'alarma' in rec:
            num=rec.replace('alarma','')
            num=num.strip()
            talk("Alarma activada a las "+num+"horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M')==num:
                    print("DESPIERTA!!!")
                    mixer.init()
                    mixer.music.load("turururu.mp3")
                    mixer.music.play()
                    if keyboard.read_key()=="s":
                        mixer.music.stop()
                        break
        elif 'colores' in rec:
            talk("Enseguida")
            colors.capture()
        elif 'termina' in rec:
            talk("Adios")
            break
        
button_voice_mx=Button(main_window,text="Español \nMéxico", fg="gray", bg="#bdc3c7",
                       font=("Arial",10,"bold"), command=mexican_voice)
button_voice_mx.place(x=170,y=180)

button_voice_es=Button(main_window,text="Español \nEspaña", fg="gray", bg="#bdc3c7",
                       font=("Arial",10,"bold"), command=spain_voice)
button_voice_es.place(x=100,y=180)

button_voice_us=Button(main_window,text="Ingles", fg="gray", bg="#bdc3c7",
                       font=("Arial",10,"bold"), command=english_voice)
button_voice_us.place(x=170,y=250)

button_prin=Button(main_window,text="Escuchar", fg="gray", bg="#bdc3c7",
                       font=("Arial",10,"bold"),command=run_billetin)

button_prin.place(x=100,y=250)

ImagenBilleton = ImageTk.PhotoImage(Image.open("ImagenBilleton.jpg"))

window_photo=Label(main_window, image=ImagenBilleton)
window_photo.pack(pady=5)

main_window.mainloop()