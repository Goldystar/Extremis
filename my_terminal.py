#<_io.TextIOWrapper name='C:/Users/admin/Desktop/26 2.txt' mode='w' encoding='cp1252'>
# Serial COM Port terminal program
# 22/5/2020, Girish Waghela
# I wrote 2 modules for this program: terminal.py and serial_rx_tx.py.
#
import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext
from tkinter import *
from tkinter import filedialog
import serial_rx_tx
import _thread
import time
import webbrowser
from tkinter import messagebox
from tkinter.font import Font
import xlsxwriter

# globals
serialPort = serial_rx_tx.SerialPort()
logFile = None

root = tk.Tk() # create a Tk root window
root.title( "IG - Serial Data Terminal " )
# set up the window size and position
root.geometry("800x500")
root.minsize(1000,500)

#to set font type
myfont = Font(family="Berlin Sans FB Demi",size=16)

#for bottom status bar-IG
statusvar = StringVar()
statusvar.set('Ready')
sbar = Label(root,font=myfont,textvariable=statusvar,relief=GROOVE,anchor ="w",fg="red")
sbar.pack(side=BOTTOM,fill = X)


#Auto-scroll
def on_off():
    if button_autoscroll.cget("text") == 'Auto Scroll ON':
        # print("on")
        button_autoscroll.config(text='Auto Scroll OFF',fg="red1")

    elif button_autoscroll.cget("text") == 'Auto Scroll OFF':
         print("off")
         button_autoscroll.config(text='Auto Scroll ON',fg="black")

#check scroll button
def check():
    if button_autoscroll.cget("text") == 'Auto Scroll ON':
       textbox.see(tk.END)
    #    print("on")

    elif button_autoscroll.cget("text") == 'Auto Scroll OFF':
        return None
        #  print("off")      

screen_height = root.winfo_screenheight()
print(screen_height)

# scrolled text box used to display the serial data
frame = tk.Frame(root, bg='steelblue1')
frame.pack(side="bottom", fill='both', expand='yes')
textbox = tkscrolledtext.ScrolledText(master=frame, wrap='word', width=180, height=14) #width=characters, height=lines
textbox.pack(side='bottom', fill='both', expand=True, padx=0, pady=0)
textbox.config(font="bold")

# scrolled text box used to display the serial data
frame2 = tk.Frame(root, bg='steelblue1')
frame2.pack(side="top", fill='both', expand='no')
textbox2 = tkscrolledtext.ScrolledText(master=frame2, wrap='word', width=180, height=5) #width=characters, height=lines
textbox2.pack(side='top', fill='y', expand=True, padx=0, pady=0)
textbox2.config(font=myfont)

#COM Port label
label_comport = Label(root,width=9,height=2,text="COM Port :")
label_comport.place(x=10,y=10)
label_comport.config(font=myfont,bg="white")

#COM Port entry box
comport_edit = Entry(root,width=10)
comport_edit.place(x=125,y=20)
comport_edit.config(font=myfont,relief=GROOVE)
comport_edit.insert(END,"COM3")

# serial data callback function
def OnReceiveSerialData(message):
    str_message = message.decode("utf-8")
    textbox.insert(INSERT, str_message)# IG most important for new text up an doWN FROM last one
    name = []
    name.append(str_message)
    print(name)
    check()
    return
    # #textbox.insert('1.0', str_message)#to latest on 1st line
    # textbox.see(tk.END)# to autoscroll to bottom


#save as
def save_as():
    serialPort.Close()
    button_openclose.config(text='Open COM Port')
    sbar.update()
    statusvar.set("COM Port Closed")
    f = filedialog.asksaveasfile(mode="w", defaultextension=".xlsx" )
    txt = str(f)
    x = txt.replace("<_io.TextIOWrapper name=","")
    x = x.replace(" mode='w' encoding='cp1252'>","")
    # x = x.replace(".txt","")
    print(x)
    workbook = xlsxwriter.Workbook(x)
    worksheet = workbook.add_worksheet()

    for row_num, data in enumerate(name):
         worksheet.write(row_num, 0, data)

    workbook.close()

    if f is None:
        return
    text2save = textbox.get(1.0,END)  
    f.write(text2save)  
    f.close()


# Register the callback above with the serial port object
serialPort.RegisterReceiveCallback(OnReceiveSerialData)


def sdterm_main():
    root.after(200, sdterm_main)  # run the main loop once each 200 ms

#
#  commands associated with button presses
# 
def OpenCommand():
    if button_openclose.cget("text") == 'Open COM Port':
        comport = comport_edit.get()
        baudrate = baudrate_edit.get()
        serialPort.Open(comport,baudrate)
        button_openclose.config(text='Close COM Port')
        sbar.update()
        statusvar.set("communication started")#### 

    elif button_openclose.cget("text") == 'Close COM Port':
        # if button_replaylog.cget('text') == 'Stop Replay Log':
        #     sbar.update()
        #     statusvar.set("Stop Log Replay first")
        # else:
            serialPort.Close()
            button_openclose.config(text='Open COM Port')
            sbar.update()
            statusvar.set("COM Port Closed")
           # textbox.insert('1.0',"COM Port here Closed\r\n")

def ClearDataCommand():
    textbox.delete('1.0',END)
    # textbox.

def SendDataCommand():
    message = senddata_edit.get()
    if serialPort.IsOpen():
        message += '\r\n'
        serialPort.Send(message)
        textbox.insert(END,message)
    else:
        sbar.update()
        statusvar.set("Not sent - Open COM Port is open or not connected")
        # textbox.insert('1.0',"COM Port Closed\r\n")

def ReplayLogFile():
    try:
      if logFile != None:
        readline = logFile.readline()
        global serialPort
        serialPort.Send(readline)
    except:
      print("Exception in ReplayLogFile()")

def ReplayLogThread():
    while True:
        time.sleep(1.0)
        global logFile
        if serialPort.IsOpen():
            if logFile != None:
                ReplayLogFile()

def OpenLogFile():
    if not serialPort.IsOpen():
        sbar.update()
        statusvar.set("Open COM port first")
    else:
        if button_replaylog.cget('text') == 'Replay Log':
            try:
                root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                           filetypes=(("log files", "*.log"), ("all files", "*.*")))
                global logFile
                logFile = open(root.filename,'r')
                _thread.start_new_thread(ReplayLogThread, ())
                button_replaylog.config(text='Stop Log Replay')
                sbar.update()
                statusvar.set("Sending to open COM port from: " + root.filename)
                #textbox.insert('1.0', "Sending to open COM port from: " + root.filename + "\r\n")
            except:
                sbar.update()
                statusvar.set("Could not open log file")
               # textbox.insert('1.0', "Could not open log file\r\n")
        else:
            button_replaylog.config(text='Replay Log')
            sbar.update()
            statusvar.set("Stopped sending messages to open COM port")
           # textbox.insert('1.0', "Stopped sending messages to open COM port\r\n")
            logFile = None

def DisplayAbout():
    tk.messagebox.showinfo(
    "About",
    "Program Written by Girish Waghela \r\n\r\n" 
    "Handling of serial COM port data as follows:\r\n\r\n" 
    "1 - Getting messages from a COM port via a callback function\r\n" 
    "2 - Sending messages from a file to the COM port, one at a time\r\n" 
    "3 - Sending log file messages and receiving messages at the same time\r\n\r\n")

def TutorialsWebPage():
    webbrowser.open("https://www.youtube.com",
                    new=1, autoraise=True)

# COM Port open/close button
button_openclose = Button(root,text="Open COM Port",width=15,command=OpenCommand)
button_openclose.config(font=myfont,bg='gray90',borderwidth=4)
button_openclose.place(x=270,y=6)

#Clear Rx Data button
button_cleardata = Button(root,text="Clear Data",width=10,command=ClearDataCommand)
button_cleardata.config(font=myfont,bg='gray90',borderwidth=4)
button_cleardata.place(x=560,y=6)

#Send Message button
sfont = Font(family="Berlin Sans FB Demi",size=16)
button_senddata = Button(root,text="Send",width=10,command=SendDataCommand)
button_senddata.config(font=sfont,bg='gray90',borderwidth=4)
button_senddata.place(x=730,y=60)

#Save button
button_save = Button(root,text="Save",width=5,command=save_as)
button_save.config(font=myfont,bg='gray90',borderwidth=4)
button_save.place(x=475,y=6)

#Auto scroll button
button_autoscroll = Button(root,text="Auto Scroll ON",width=13,command=on_off)
button_autoscroll.config(font=myfont,bg='gray90',borderwidth=4,fg="black")
button_autoscroll.place(x=705,y=6)

#  #Replay Log button
# button_replaylog = Button(root,text="Replay Log",width=6,command=OpenLogFile)
# button_replaylog.config(font=myfont,bg='gray90',borderwidth=4)
# button_replaylog.place(x=475,y=6)

#About button
# button_about = Button(root,text="About",width=16,command=DisplayAbout)
# button_about.config(font=myfont,bg='gray90',borderwidth=4)
# button_about.place(x=620,y=25)

#Tutorials
# button_tutorials = Button(root,text="Tutorials",width=16,command=TutorialsWebPage)
# button_tutorials.config(font=myfont,bg='gray90',borderwidth=4)
# button_tutorials.place(x=789,y=25)

#
# data entry labels and entry boxes
#

#Send Data entry box
senddata_edit = Entry(root,width=34)
senddata_edit.place(x=270,y=70)
senddata_edit.config(font=myfont)
senddata_edit.insert(END,"Message")

#Baud Rate label
label_baud = Label(root,width=9,height=2,text="Baud Rate :")
label_baud.place(x=10,y=60)
label_baud.config(font=myfont,bg="white")

#Baud Rate entry box
baudrate_edit = Entry(root,width=10)
baudrate_edit.place(x=125,y=70)
baudrate_edit.config(font=myfont)
baudrate_edit.insert(END,"9600")

#
# The main loop
#
root.after(200, sdterm_main)


#for upper menu bar
mainmenu = Menu(root)
# file
m1 = Menu(mainmenu,tearoff=0)
m1.add_command(label="Save",command=save_as)
m1.add_command(label="Replaylog",command=OpenLogFile)
# m1.add_command(label="Exit",command=quit)
root.config(menu=mainmenu)
mainmenu.add_cascade(label="File",menu=m1)
# edit
m2 = Menu(mainmenu,tearoff=0)
m2.add_command(label="About",command=DisplayAbout)
m2.add_command(label="Tutorial",command=TutorialsWebPage)
root.config(menu=mainmenu)
mainmenu.add_cascade(label="Help",menu=m2)

root.mainloop()
#


