#ChatBot+Speaker
import json
from difflib import get_close_matches

import speech_recognition as sr
import pyttsx3

#inicializar reconocedor de voz
r=sr.Recognizer()



def record_text():
    while(1):
        try: #es para intetnar de nuevo si no se entiende lo que se dijo/no se pudo convertir
            with sr.Microphone() as source2: #usar el microfono como fuente de audio
                

                audio2=r.listen(source2)

                MyText=r.recognize_google(audio2, language="es-MX")  # Español México es-MX es-ES para España es-US Español Estados Unidos

                return MyText
            
        except sr.RequestError as e: #si hay un error con la solicitud a la API de Google
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError: #si no se pudo entender el audio
            print("Unable to recognize speech")
    return 

def speak_text(command):
    
    engine=pyttsx3.init() #inicializar el motor de texto a voz
    engine.setProperty('rate', 150) #velocidad de habla
    """for voice in engine.getProperty('voices'):
            print(voice)"""
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0')
    engine.say(command) #decir el comando
    engine.runAndWait() #esperar a que termine de hablar

    return

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict =json.load(file) #data variable tipo diccionario
    return data

def save_knowledge_base(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as file: #w es write mode
        json.dump(data, file, indent=4) #indent=4 para formato legible


def find_best_match(user_question: str, questions: list[str]) -> str| None:
    matches: list=get_close_matches(user_question, questions, n=1, cutoff=0.6) #n=1 para obtener solo la mejor coincidencia, cutoff=0.6 para establecer un umbral de similitud
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str| None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q['answer']
        
def chat_bot():
    knowledge_base: dict=load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str=record_text() #obtener el texto del audio
        print("You said: {}".format(user_input)) #imprimir el texto reconocido

        if user_input.lower() == 'quit':
            print("ChatBot: Adiós!")
            break
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]]) #buscar mejor match en json

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'ChatBot: {answer}')
            speak_text(answer) #hacer que el chatbot hable la respuesta
        else:
            answer: str= 'No sé la respuesta a eso. ¿Puedes enseñarme?'
            print('ChatBot: No sé la respuesta a eso. ¿Puedes enseñarme?')
            speak_text(answer)
            new_answer: str=input("Escribe la respuesta o skip para omitir: ")

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({'question': user_input, 'answer': new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('ChatBot: Gracias por enseñarme!')
                speak_text('Gracias por enseñarme!')

if __name__ == "__main__": 
    with sr.Microphone() as source2:
        r.adjust_for_ambient_noise(source2) #ajustar el reconocedor para el ruido ambiental

while True:
    chat_bot()