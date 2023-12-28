# importing libraries
from tkinter import *
from tkinter import Text, Scrollbar, BOTH, RIGHT, Y
from tkinter.ttk import *
from tkinter import font,colorchooser,filedialog,messagebox
import os

# defining a function responsible for toggling the visibility of the toolbar and text area based on the value of show_toolbar

def ToolBarFunc():
    if show_toolbar.get()==False:
        tool_bar.pack_forget()
    if show_toolbar.get()==True:
        textarea.pack_forget()
        tool_bar.pack(fill=X)
        textarea.pack(fill=BOTH,expand=1)

# defining StatusBarFunc

def StatusBarFunc():
    if show_statusbar.get()==False :
        status_bar.pack_forget()
    else:
        status_bar.pack()

# defining change_theme, it configures the background and foreground colors of a textarea
def change_theme(bg_color,fg_color):
    textarea.config(bg=bg_color,fg=fg_color)

# defining the find option of edit menu, responsible in finding a word and replacing a word or character

def find():
    textarea.tag_remove('match', 1.0, END)
    def find_words():
        start_pos = '1.0'
        word = findentryfield.get()
        if word:
            while True:
                start_pos = textarea.search(word, start_pos, stopindex=END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                textarea.tag_add('match', start_pos, end_pos)
                textarea.tag_config('match', foreground='red', background='yellow')
                start_pos = end_pos
    def replace_text():
        word = findentryfield.get()
        replaceword = replaceentryfield.get()
        content = textarea.get(1.0, END)
        new_content = content.replace(word, replaceword)
        textarea.delete(1.0, END)
        textarea.insert(1.0, new_content)
    root1 = Toplevel()
    root1.title('Find')
    root1.geometry('450x250+500+200')
    root1.resizable(0, 0)
    labelFrame = LabelFrame(root1,text='Find/Replace')
    labelFrame.pack(pady=50)

    findLabel = Label(labelFrame, text='Find')
    findLabel.grid(row=0, column=0, padx=5, pady=5)
    findentryfield = Entry(labelFrame)
    findentryfield.grid(row=0, column=1, padx=5, pady=5)

    replaceLabel = Label(labelFrame, text='Replace')
    replaceLabel.grid(row=1, column=0, padx=5, pady=5)
    replaceentryfield = Entry(labelFrame)
    replaceentryfield.grid(row=1, column=1, padx=5, pady=5)

    findButton = Button(labelFrame, text='FIND',command=find_words)
    findButton.grid(row=2, column=0, padx=10, pady=10)

    replaceButton = Button(labelFrame, text='REPLACE',command=replace_text)
    replaceButton.grid(row=2, column=1, padx=10, pady=10)

    def doSomething():
        textarea.tag_remove('match',1.0,END)
        root1.destroy()
    root1.protocol('WM_DELETE_WINDOW',doSomething)

    root1.mainloop()



fontSize=12
fontStyle='Arial'

# defining font_style function which helps in changing the style of the font

def font_style(event):
    global fontStyle
    fontStyle=font_family_variable.get()
    textarea.config(font=(fontStyle,fontSize))

# defining font_size function which helps in modifying the size of the font
def font_size(event):
    global fontSize
    fontSize=size_variable.get()
    textarea.config(font=(fontStyle,fontSize))

# bold_text function is used in changing the weight from normal to bold and bold to normal

def bold_text():
    text_property=font.Font(font=textarea['font']).actual()
    if text_property['weight']=='normal':
        textarea.config(font=(fontStyle,fontSize,'bold'))
    if text_property['weight']=='bold':
        textarea.config(font=(fontStyle,fontSize,'normal'))

# italic_next is a function used in changing the slant of the text

def italic_text():
    text_property=font.Font(font=textarea['font']).actual()
    if text_property['slant']=='roman':
        textarea.config(font=(fontStyle,fontSize,'italic'))
    if text_property['slant']=='italic':
        textarea.config(font=(fontStyle,fontSize,'roman'))

# helpful in underlining the text and to make normal when it's underlined

def underline_text():
    text_property=font.Font(font=textarea['font']).actual()
    if text_property['underline']==0:
        textarea.config(font=(fontStyle,fontSize,'underline'))
    if text_property['underline']==1:
        textarea.config(font=(fontStyle,fontSize,))

# used in customizing the appearance of text in the textarea

def colour_select():
    color=colorchooser.askcolor()
    textarea.config(fg=color[1])

# funtion defined for right aligning the text
def right_align():
    data=textarea.get(0.0,END)
    textarea.tag_config('right',justify=RIGHT)
    textarea.delete(0.0,END)
    textarea.insert(INSERT,data,'right')

# funtion defined for left aligning the text

def left_align():
    data=textarea.get(0.0,END)
    textarea.tag_config('left',justify=LEFT)
    textarea.delete(0.0,END)
    textarea.insert(INSERT,data,'left')

# used to center align the text

def center_align():
    data=textarea.get(0.0,END)
    textarea.tag_config('center',justify=CENTER)
    textarea.delete(0.0,END)
    textarea.insert(INSERT,data,'center')
url=''
# new_file,open_file,save_file,saveas_file,iexit are defined to help in getting a new file, opening a file, saving a file and to exit from the window

def new_file():
    global url
    url=''
    textarea.delete(0.0,END)

def open_file():
    global url
    url=filedialog.askopenfilename(initialdir=os.getcwd,title='Select File',filetypes=(('Text File','txt'),('All Types','*.*')))
    if url!='':
        with open(url, 'r') as file:
            textarea.delete(1.0, END)
            textarea.insert(1.0, file.read())
            root.title(os.path.basename(url))

def save_file():
    if url=='':
        save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','.txt'),('All Files','*.*')))
        content=textarea.get(0.0,END)
        save_url.write(content)
        save_url.close()
    else:
        content=textarea.get(0.0,END)
        file=open(url,'w')
        file.write(content)

def saveas_file():
    save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt',
                                        filetypes=(('Text Type', '.txt'), ('All Files', '*.*')))
    content = textarea.get(0.0, END)
    save_url.write(content)
    save_url.close()
    if url!='':
        os.remove(url)

def iexit():
    if textarea.edit_modified():
        result=messagebox.askyesnocancel('Warning','Do you want to save the file')
        if result is True:
            if url!='':
                content=textarea.get(0.0,END)
                file=open(url,'w')
                file.write(content)
                root.destroy()
            else:
                content = textarea.get(0.0, END)
                save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt',filetypes=(('Text Type', '.txt'), ('All Files', '*.*')))
                save_url.write(content)
                save_url.close()
                root.destroy()
        elif result is False:
            root.destroy()
        else:
            pass
    else:
        root.destroy()

# helpful in identifying the number of words and characters entered in the text area

def statusbar(event):
    if textarea.edit_modified():
        words=len(textarea.get(0.0,END).split())
        chars=len(textarea.get(0.0,('end-1c')).replace(" ",""))
        status_bar.config(text=f"characters:{chars} words:{words}")
    textarea.edit_modified((False))


def clear_text(event=None):
    textarea.delete(1.0, END)

# creating a window and giving title,geometry
root=Tk()
root.title("Text Editor")
root.geometry('1500x750+10+10')
root.resizable(False,False)

# creating a menu bar and a file menu with new, open, save, saveas ,exit commands in it and adding images to each command

menubar=Menu(root)
root.config(menu=menubar)
filemenu = Menu(menubar,tearoff=False)
menubar.add_cascade(label='File', menu=filemenu)
newImage = PhotoImage(file='new.png')
openImage = PhotoImage(file='open.png')
saveImage = PhotoImage(file='save.png')
save_asImage = PhotoImage(file='save_as.png')
exitImage = PhotoImage(file='exit.png')
filemenu.add_command(label='New', accelerator='Ctrl+N', image=newImage, compound=LEFT,command=new_file)
filemenu.add_command(label='Open', accelerator='Ctrl+O',image=openImage, compound=LEFT,command=open_file)
filemenu.add_command(label='Save', accelerator='Ctrl+S',image=saveImage, compound=LEFT,command=save_file)
filemenu.add_command(label='Save As', accelerator='Ctrl+Alt+S',image=save_asImage, compound=LEFT,command=saveas_file)
filemenu.add_separator()
filemenu.add_command(label='Exit', accelerator='Ctrl+Q',image=exitImage, compound=LEFT,command=iexit)
root.bind('<Control-n>', lambda event: new_file())
root.bind('<Control-o>', lambda event: open_file())
root.bind('<Control-s>', lambda event: save_file())
root.bind('<Control-Alt-s>', lambda event: saveas_file())
root.bind('<Control-q>', lambda event: iexit())

# font size and font color combobox is created

tool_bar=Label(root)
tool_bar.pack(side=TOP,fill=X)
font_families=font.families()
font_family_variable=StringVar()
size_variable=IntVar()
fontfamily_combobox=Combobox(tool_bar,width=30,values=font_families,state='readonly',textvariable=font_family_variable)
fontfamily_combobox.current(font_families.index('Arial'))
fontfamily_combobox.grid(row=0,column=0,padx=4)
font_size_combobox=Combobox(tool_bar,width=14,state='readonly',textvariable=size_variable,values=tuple(range(8,80)))
font_size_combobox.grid(row=0,column=1,padx=4)
font_size_combobox.current(4)

fontfamily_combobox.bind('<<ComboboxSelected>>',font_style)
font_size_combobox.bind('<<ComboboxSelected>>',font_size)

# bold button

boldimage=PhotoImage(file='bold.png')
boldButton=Button(tool_bar,image=boldimage,command=bold_text)
boldButton.grid(row=0,column=2,padx=4)

# italic Button is added to change the slant of the text i.e from roman to slant and slant to roman

italicimage=PhotoImage(file='italic.png')
italicButton=Button(tool_bar,image=italicimage,command=italic_text)
italicButton.grid(row=0,column=3,padx=4)

# underline button

underlineimage=PhotoImage(file='underline.png')
underlineButton=Button(tool_bar,image=underlineimage,command=underline_text)
underlineButton.grid(row=0,column=4,padx=4)

# font colour button is created to change the color of the text and given a function as colour_select()

fontcolorimage=PhotoImage(file='font_color.png')
fontcolorButton=Button(tool_bar,image=fontcolorimage,command=colour_select)
fontcolorButton.grid(row=0,column=5,padx=4)

# left align button is created

leftalignimage=PhotoImage(file='left.png')
leftalignButton=Button(tool_bar,image=leftalignimage,command=left_align)
leftalignButton.grid(row=0,column=6,padx=4)

#right align button

rightalignimage=PhotoImage(file='right.png')
rightalignButton=Button(tool_bar,image=rightalignimage,command=right_align)
rightalignButton.grid(row=0,column=7,padx=4)

# center align button

centeralignimage=PhotoImage(file='center.png')
centeralignButton=Button(tool_bar,image=centeralignimage,command=center_align)
centeralignButton.grid(row=0,column=8,padx=4)

# adding scrollbar

scrollbar=Scrollbar(root)
scrollbar.pack(side="right",fill=Y)
textarea=Text(root,yscrollcommand=scrollbar.set)
textarea.pack(fill=BOTH,expand=True)
scrollbar.config(command=textarea.yview)


status_bar=Label(root,text='status bar')
status_bar.pack(side=BOTTOM)
textarea.bind('<<Modified>>',statusbar)

# creating an edit menu and adding commands like cut,copy,paste,clear,find to it and adding images to each command

editmenu=Menu(menubar,tearoff=False)
cutimage=PhotoImage(file='cut.png')
copyimage=PhotoImage(file='copy.png')
pasteimage=PhotoImage(file='paste.png')
clearimage=PhotoImage(file='clear_all.png')
findimage=PhotoImage(file='find.png')
editmenu.add_command(label='Cut', accelerator='Ctrl+X', image=cutimage, compound=LEFT,command=lambda:textarea.event_generate('<Control-x>'))
editmenu.add_command(label='Copy', accelerator='Ctrl+C', image=copyimage, compound=LEFT,command=lambda:textarea.event_generate('<Control-c>'))
editmenu.add_command(label='Paste', accelerator='Ctrl+V', image=pasteimage, compound=LEFT,command=lambda:textarea.event_generate('<Control-v>'))
editmenu.add_command(label='Clear', accelerator='Ctrl+N', image=clearimage, compound=LEFT,command=clear_text)
editmenu.add_command(label='Find', accelerator='Ctrl+Alt+X', image=findimage, compound=LEFT,command=find)
root.bind('<Control-n>', lambda event: clear_text())
menubar.add_cascade(label='Edit', menu=editmenu)
show_toolbar=BooleanVar()
show_statusbar=BooleanVar()
viewmenu=Menu(menubar,tearoff=False)
toolimage=PhotoImage(file='tool_bar.png')
statusimage=PhotoImage(file='status_bar.png')
viewmenu.add_checkbutton(label='Tool Bar',variable=show_toolbar,onvalue=True,offvalue=False,image=toolimage,compound=LEFT,command=ToolBarFunc)
show_toolbar.set(True)
viewmenu.add_checkbutton(label='Status Bar',variable=show_statusbar, onvalue=True,offvalue=False,image=statusimage,compound=LEFT,command=StatusBarFunc)
show_statusbar.set(True)
menubar.add_cascade(label='View', menu=viewmenu)

# creating themes menu and adding radio buttons for different colors

themesmenu=Menu(menubar,tearoff=False)
theme_choice1=StringVar()
theme_choice2=StringVar()
theme_choice3=StringVar()
theme_choice4=StringVar()
lightimage=PhotoImage(file='light_default.png')
darkimage=PhotoImage(file='dark.png')
redimage=PhotoImage(file='red.png')
monokaiimage=PhotoImage(file='monokai.png')
menubar.add_cascade(label='Themes', menu=themesmenu)
themesmenu.add_radiobutton(label='Light Default', variable=theme_choice1, image=lightimage, compound=LEFT,command=lambda : change_theme('white','black'))
themesmenu.add_radiobutton(label='Dark', variable=theme_choice2, image=darkimage, compound=LEFT,command=lambda : change_theme('gray20','white'))
themesmenu.add_radiobutton(label='Pink', variable=theme_choice3, image=redimage, compound=LEFT,command=lambda : change_theme('pink','blue'))
themesmenu.add_radiobutton(label='Monokai', variable=theme_choice4, image=monokaiimage, compound=LEFT,command=lambda : change_theme('orange','white'))

root.mainloop()





