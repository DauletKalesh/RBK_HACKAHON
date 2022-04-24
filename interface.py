from customs import EntryWithPlaceholder,TkinterCustomButton
from russian_filter import filtration
import json 
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import pickle
from tkinter import * 

with open("patterns (1).json", encoding='utf-8') as file:
    data = json.load(file)
model = keras.models.load_model('chat_model')

# load tokenizer object
with open('tokenizer.pickle', 'rb') as token:
    tokenizer = pickle.load(token)

# load label encoder object
with open('label_encoder.pickle', 'rb') as encode:
    lbl_encoder = pickle.load(encode)

y_axis = 0


def response():
    global y_axis
    message = entry.get()
    entry.delete(0, 'end')
    max_len = 20
    y_axis += const//2
    if 'оператор' in message:
        answer = 'Связываю вас с оператором'
    Label(
        canvas, bg="light grey", text=message, wraplength=200, justify=RIGHT
    ).place(x=160, y=const+10+y_axis)
    result = model.predict(
        keras.preprocessing.sequence.pad_sequences(
            tokenizer.texts_to_sequences([filtration(message)]),
        truncating='post', maxlen=max_len)
    )
    tag = lbl_encoder.inverse_transform([np.argmax(result)])
    for i in data['patterns']:
            if i['key'] == tag and answer!='Связываю вас с оператором':
                answer = i['answers']
                break
    y_axis += len(message)//2
    Label(
        canvas, bg="light grey", text=answer, wraplength=200, justify=LEFT
    ).place(x=5, y=const*2+y_axis)
    y_axis += len(answer)+len(message)*2


root = Tk()
root.geometry('350x500')
root.configure(background='darkgrey')
root.title('Виртуальный помощник')
root.resizable(width=False, height=False)

frame = Frame(root,width=330,height=450)
frame.place(x=3, y=3)
# frame.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)
canvas = Canvas(frame, bg='#FFFFFF',width=330,height=450,scrollregion=(0,0,1000,1000))

vbar = Scrollbar(root, orient=VERTICAL)
# vbar.pack(side=RIGHT,fill=Y)
vbar.place(x=330, y=0, height=450)

canvas.configure(yscrollcommand=vbar.set,width=330,height=450)
vbar.configure(command = canvas.yview)
# canvas.pack(side=LEFT,expand=True,fill=BOTH)
canvas.place(x=0, y=0)


entry = EntryWithPlaceholder(root, placeholder='Напишите вопрос')
entry.config(font=('calibri',14))

button = TkinterCustomButton(
    master=root, text="Отправить", fg_color='turquoise', hover_color='blue',
    width=100, height=30, text_font=('arial bold', 13), command=response
)

text = Label(frame, bg="light grey", text="Здравствуйте, я ваш виртуальный помощник \N{smiling face with smiling eyes}! Чем могу помочь?", wraplength=200, justify=LEFT)
const = len(text['text'])-10

button.place(x=230, y=464)
entry.place(x=5, y=465, width=220)
text.place(x=5, y=5)
root.mainloop()

