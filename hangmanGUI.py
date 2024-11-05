from tkinter import *
from PIL import ImageTk, Image  

def initGUI():
    root = Tk()
    root.title("Hangman")
    root.geometry("300x50")
    return root

def clickLetter(i, letter):
    def func():
        if (buttons[i].cget("text")=="_"):
            buttons[i].config(text = letter)
        elif (buttons[i].cget("text")==letter):
            buttons[i].config(text = "_")
    return func
def clickDone(letter):
    def func():
        global positions
        positions = []
        for i in range(len(buttons)-1):
            if (buttons[i].cget("text") == letter):
                positions.append(i)
        buttons[-1].config(state = DISABLED)
        root.quit()
    return func
def guessing(word, letter, number, numMistakes, wordRV):
    root.geometry(str(len(word)*50+50)+"x600")
    textFrame = Frame(root)
    textFrame.grid(row = 0, column = 0)
    letterAsked = Label(textFrame, text = str(number) + ". Is " + letter + " in your word?")
    letterAsked.grid(row = 0, column = 0)
    inputFrame = Frame(root)
    inputFrame.grid(row=1, column = 0)
    global buttons 
    buttons = [Button(inputFrame, text = word[i], command = clickLetter(i, letter)) for i in range(len(word))]
    buttons.append(Button(inputFrame, text = "Done", command = clickDone(letter)))

    for i in range(len(buttons)):
        buttons[i].grid(row=0,column = i)
    
    textFrame2 = Frame(root)
    textFrame2.grid(row=2, column=0)
    text = Label(textFrame2, text="Most Likely Words:\n"+wordRV.topString(10))
    text.grid(row = 0, column=0)
     
    imageFrame = Frame(root)
    imageFrame.grid(row = 3, column = 0)
    image = ImageTk.PhotoImage(Image.open("images/"+str(numMistakes)+".jpg"))
    label = Label(imageFrame, image=image)
    label.grid(row = 0, column = 0)

    root.mainloop()

def destroy(root):
    for frame in root.winfo_children():
        frame.destroy()

# really scuffed, there has to be a better way to do this
def globalizeRoot(r):
    global root
    root = r
def guessCall(root, word, letter, number, numMistakes, wordRV):
    destroy(root)
    globalizeRoot(root)
    guessing(word, letter, number, numMistakes, wordRV)
    ret = ["_"]*len(word)
    for i in range(len(ret)):
        if i in positions:
            ret[i] = letter
    return ''.join(ret)
def finishCall(root, text):
    destroy(root)
    lbl = Label(root, text = text)
    lbl.grid(row = 0, column = 0)
    root.mainloop()

def startCall(root):
    entrylbl = Label(root, text = "How many letters?")
    entrylbl.grid(row = 0, column = 0)
    entry = Entry(root)
    entry.grid(row = 1, column = 0)
    entryButton = Button(root, text = "Done", command = lambda: root.quit())
    entryButton.grid(row = 1, column = 1)
    root.mainloop()
    return entry.get()
