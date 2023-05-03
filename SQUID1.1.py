
from tkinter import *
from tkinter import ttk
import json
from telnetlib import Telnet
import time
import subprocess
from functools import partial
import os
import threading
decodersList = []
encodersList = []
newroomname = ''
newroomnumber = ''

class Decoder:
    def __init__(self,ip,name):
        self.ip = ip
        self.name = name
class Encoder:
    def __init__(self,ip,multicast,name):
        self.ip = ip
        self.multicast = multicast
        self.name = name
def RoomSelected(args):
    selectedRoom = Combo.get()
    ComboDesRoom.set(selectedRoom)
    ComboSourRoom.set(selectedRoom)
    DesRoomSelected(args)#good?
    SourRoomSelected(args)
def DesRoomSelected(args):
    selectedRoom = ComboDesRoom.get()
    selectedRoom,RoomNumber = selectedRoom.split('-')
    comboDesList = []
    decodersList.clear()
    filename = 'db.json'
    with open(filename,"r") as file:
            data = json.load(file)
    for room in data['rooms']:
        if room['number'] == RoomNumber:
            for dec in room['decoders']:
               decodersList.append(Decoder(dec['ip'],dec['name']))
               comboDesList.append(dec['name'])
    ComboDes.configure(value=comboDesList)

    ComboDes.set("בחר יעד")
    #print(RoomNumber)
    #ComboDes.event_generate('<Down>')
    
    #switch(True)
    #if list.get(0)=='לא נבחר חמ"ל':
    #if is_onflag:
    #    print('a')
    #    list.delete(0,END)
    #    x=getdecoders()
    #    for each_item in range(len(x)):
    #            list.insert(END, x[each_item])
    #is_on=False
    if selectedRoom=='בחר חמ"ל':
        on_button.place_forget()
    else:
        on_button.place(relx = 0.95, rely = 0.27, anchor = CENTER)

    #x=getdecoders()  
    #for each_item in range(len(x)):
    #      
    #    list.insert(END, x[each_item])
    if not is_on:
        #print('a')
        on_button.invoke()
        on_button.invoke()
def SourRoomSelected(args):
    selectedRoom = ComboSourRoom.get()
    selectedRoom,RoomNumber = selectedRoom.split('-')
    comboSourList = []
    encodersList.clear()
    filename = 'db.json'
    with open(filename,"r") as file:
            data = json.load(file)
    for room in data['rooms']:
        if room['number'] == RoomNumber:
            for enc in room['encoders']:
               encodersList.append(Encoder(enc['ip'],enc['multicast'],enc['name']))
               comboSourList.append(enc['name'])
    ComboSour.configure(value=comboSourList)

    ComboSour.set("בחר מקור")
    #print(RoomNumber)
def DesSelected(args):
    statdes.configure(bg='white')
def SourSelected(args):
    statsour.configure(bg='white')
def ping(ip):
    ping_test = subprocess.call('ping %s -n 1' % ip) #one time
    return ping_test == 0  
def ping2(ip): #slow 4 times
    res=os.popen(f"ping {ip}").read()
    return "Received = 4" in res
def Do():
    
    tempdecip = 0#check later
    tempenip = 0

    selectedRoom = ComboDes.get()
    if selectedRoom != "בחר יעד":
        #print(decodersList)
        for dec in decodersList:
            if dec.name == selectedRoom:
                #print(dec.ip)
                decip = dec #for execute
                tempdecip = 1
    selectedRoom = ComboSour.get()
    if selectedRoom != "בחר מקור":
        #print(decodersList)
        for enc in encodersList:
            if enc.name == selectedRoom:
                #print(enc.ip)
                encip = enc#for execute
                tempenip = 1
    if tempdecip != 0 and tempenip != 0:
        Execute(decip,encip)
        #print(decip.ip," streaming ",encip.ip)
def Do2():
    selectedecoders=[]
    listcur=list.curselection()
    for i in listcur:
        op=list.get(i)
        selectedecoders.append(op)

    tempdecip = 0#check later
    tempenip = 0
    decsclas=[]
    for dec in decodersList:
         if dec.name in selectedecoders:
                 decsclas.append(dec)
    selectedRoom = ComboSour.get()
    if selectedRoom != "בחר מקור":
        for enc in encodersList:
            if enc.name == selectedRoom:
                encip = enc#for execute
                tempenip = 1
    if len(selectedecoders)!= 0 and tempenip != 0:
        for decip in decsclas:
            #Execute(decip,encip)
            threads=[]#
            t=threading.Thread(target=Execute,args=[decip,encip])  
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()#

def Execute(decip,encip):        
    #classes and not ip!!!!!
    if ping(decip.ip):
    #try:                    
        uid = "root"
        tn = Telnet(decip.ip,'24')
        print(tn.read_until(('login: ').encode('ascii')))
        tn.write(uid.encode('ascii') + " \n".encode('ascii'))
        print(tn.read_until(('/ #').encode('ascii')))
        time.sleep(0.5)
        tn.write(('gbparam s hd_stream_ip ').encode('ascii') + encip.multicast.encode('ascii') + " \n".encode('ascii'))
        time.sleep(0.5)
        tn.write(('gbparam s hd_stream port 12345').encode('ascii') + " \n".encode('ascii'))
        time.sleep(0.5)
        tn.write(('e e_reconnect').encode('ascii') + " \n".encode('ascii'))
        time.sleep(0.5)
        tn.close()
        print("{} is streaming {}".format(decip.ip,encip.ip))
    else:
    #except:
        print("no connection...")                              #Else, it's not reachable
def reboot(ip):
     if ping(ip):
        uid = "root"
        tn = Telnet(ip,'24')
        print(tn.read_until(('login: ').encode('ascii')))
        tn.write(uid.encode('ascii') + " \n".encode('ascii'))
        print(tn.read_until(('/ #').encode('ascii')))
        time.sleep(0.5)
        tn.write(('reboot').encode('ascii') + " \n".encode('ascii'))
        time.sleep(0.5)
        tn.close()
        print("reboot {}".format(ip))
     else:
        print("no connection...")                              #Else, it's not reachable

def blue1_enter(e):
   addroom.config(background='#3D59AB', foreground= "white")

def blue1_leave(e):
   addroom.config(background= '#6495ED', foreground= 'white')

def gray1_enter(e):
   delroom.config(background='#CD2626', foreground= "white")

def gray1_leave(e):
   delroom.config(background= '#212121', foreground= 'white')

def blue2_enter(e):
   adddes.config(background='#3D59AB', foreground= "white")

def blue2_leave(e):
   adddes.config(background= '#6495ED', foreground= 'white')

def gray2_enter(e):
   remdes.config(background='#CD2626', foreground= "white")

def gray2_leave(e):
   remdes.config(background= '#212121', foreground= 'white')
def blue3_enter(e):
   addsour.config(background='#3D59AB', foreground= "white")

def blue3_leave(e):
   addsour.config(background= '#6495ED', foreground= 'white')

def gray3_enter(e):
   remsour.config(background='#CD2626', foreground= "white")

def gray3_leave(e):
   remsour.config(background= '#212121', foreground= 'white')
def blue4_enter(e):
   do.config(background='#3D59AB', foreground= "white")

def blue4_leave(e):
   do.config(background= '#6495ED', foreground= 'white')

def edit1_enter(e):
   editdes.config(background='#696969', foreground= "white")

def edit1_leave(e):
   editdes.config(background= '#B0B0B0', foreground= 'white')
def edit2_enter(e):
   editsour.config(background='#696969', foreground= "white")

def edit2_leave(e):
   editsour.config(background= '#B0B0B0', foreground= 'white')
def edit3_enter(e):
   editroom.config(background='#696969', foreground= "white")

def edit3_leave(e):
   editroom.config(background= '#B0B0B0', foreground= 'white')
def check_enter(e):
   checkroom.config(background='#CD8500', foreground= "white")

def check_leave(e):
   checkroom.config(background= '#E3A869', foreground= 'white')
def reb1_enter(e):
    rebdes.config(background='#FF3030', foreground= "white")

def reb1_leave(e):
    rebdes.config(background= '#FF7F50', foreground= 'white')
def reb2_enter(e):
    rebsour.config(background='#FF3030', foreground= "white")

def reb2_leave(e):
    rebsour.config(background= '#FF7F50', foreground= 'white')
#FF7F50
def Adddeswindow():
    print("AddDestinationWindow")
    global newdesWindow
    newdesWindow = Toplevel(root)
    newdesWindow.title("יעד חדש")
    newdesWindow.geometry("600x300")
    newdesWindow.resizable(0, 0)
    
    newdesWindow.iconphoto(False, image)
    newdesWindow.grid_rowconfigure(4, weight=1)
    newdesWindow.grid_columnconfigure(2, weight=1)
    all_frame = Frame(newdesWindow, bg='white',height=300,width=600)#minimum
    all_frame.grid(rowspan=4,columnspan=2,sticky="nsew")
    center_frame = Frame(newdesWindow, bg='#EEE9E9')#minimum
    center_frame.grid(row=1,rowspan=2 ,columnspan=2,sticky="nsew",padx=20)
    title = Label(newdesWindow,text="יעד חדש", font = ("Times New Roman",24),bg='white')
    namelabel = Label(newdesWindow,text=":שם", font = ("Times New Roman",20), bg='#EEE9E9')
    global desnameentry
    desnameentry = Entry(newdesWindow,width=40,justify='right')
    iplabel = Label(newdesWindow,text=":IP", font = ("Times New Roman",20), bg='#EEE9E9')
    global desipentry
    desipentry = Entry(newdesWindow,width=40,justify='right')
    
    global adddesbutton2
    adddesbutton2 = Button(newdesWindow,text="הוסף", font=(fon,17),fg='White', bg='#6495ED',relief='groove',width=10,command =partial(Addnewdes)) #לא מעביר
    cancelbutton = Button(newdesWindow,text="ביטול", font=(fon,17),fg='White', bg='#212121',relief='groove',width=10,command=newdesWindow.destroy)
    
    global deserrorlabel
    deserrorlabel =Label(newdesWindow,fg='red',bg='white', font=(fon,15))
    deserrorlabel.place(relx = 0.5,
                  rely = 0.85,
                  anchor ='center')
    
    title.grid(row=0, column=1, columnspan=2,sticky='e',padx=(0,25))
    namelabel.grid(row=1,column=1,sticky='e',padx=(0,25))
    desnameentry.grid(row=1,column=0,sticky='e',padx=(0,25))
    iplabel.grid(row=2,column=1,sticky='e',padx=(0,25))
    desipentry.grid(row=2,column=0,sticky='e',padx=(0,25))
    #addbutton2.grid(row=10,column=1)
    adddesbutton2.grid(row=3,column=1,sticky='e',padx=(0,25))
    cancelbutton.grid(row=3,column=0,sticky='w',padx=(25,0))

    desipentry.bind('<Return>',adddesinvoke)
def adddesinvoke(args):
    adddesbutton2.invoke()
def Editsourwindow():
    if ComboSour.get()!='בחר מקור':
        print("EditSourceWindow")
        global editsourWindow
        editsourWindow = Toplevel(root)
        editsourWindow.title("ערוך מקור")
        editsourWindow.geometry("600x300")
        editsourWindow.resizable(0, 0)
        
        editsourWindow.iconphoto(False, image)
        editsourWindow.grid_rowconfigure(5, weight=1)
        editsourWindow.grid_columnconfigure(2, weight=1)
        all_frame = Frame(editsourWindow, bg='white',height=300,width=600)#minimum
        all_frame.grid(rowspan=5,columnspan=2,sticky="nsew")
        center_frame = Frame(editsourWindow, bg='#EEE9E9')#minimum
        center_frame.grid(row=1,rowspan=3 ,columnspan=2,sticky="nsew",padx=20)
        title = Label(editsourWindow,text="ערוך מקור", font = ("Times New Roman",24),bg='white')
        namelabel = Label(editsourWindow,text=":שם", font = ("Times New Roman",20), bg='#EEE9E9')
        global Esournameentry
        Esournameentry = Entry(editsourWindow,width=40,justify='right')
        iplabel = Label(editsourWindow,text=":IP", font = ("Times New Roman",20), bg='#EEE9E9')
        global Esouripentry
        Esouripentry = Entry(editsourWindow,width=40,justify='right')
        multilabel = Label(editsourWindow,text=":Multicast", font = ("Times New Roman",20), bg='#EEE9E9')
        global Esourmultientry
        Esourmultientry = Entry(editsourWindow,width=40,justify='right')
        global savesourbutton2
        savesourbutton2 = Button(editsourWindow,text="שמור", font=(fon,17),fg='White', bg='#6495ED',relief='groove',width=10,command =partial(Editsour)) #לא מעביר
        cancelbutton = Button(editsourWindow,text="ביטול", font=(fon,17),fg='White', bg='#212121',relief='groove',width=10,command=editsourWindow.destroy)
        
        global Esourerrorlabel
        Esourerrorlabel =Label(editsourWindow,fg='red',bg='white', font=(fon,15))
        Esourerrorlabel.place(relx = 0.5,
                      rely = 0.9,
                      anchor ='center')
        
        title.grid(row=0, column=1, columnspan=2,sticky='e',padx=(0,25))
        namelabel.grid(row=1,column=1,sticky='e',padx=(0,25))
        Esournameentry.grid(row=1,column=0,sticky='e',padx=(0,25))
        iplabel.grid(row=2,column=1,sticky='e',padx=(0,25))
        Esouripentry.grid(row=2,column=0,sticky='e',padx=(0,25))
        multilabel.grid(row=3,column=1,sticky='e',padx=(0,25))
        Esourmultientry.grid(row=3,column=0,sticky='e',padx=(0,25))
        #addbutton2.grid(row=10,column=1)
        savesourbutton2.grid(row=4,column=1,sticky='e',padx=(0,25))
        cancelbutton.grid(row=4,column=0,sticky='w',padx=(25,0))
        filename = 'db.json'
        with open(filename,"r") as file:
            data = json.load(file)
        selectedRoom = ComboSourRoom.get()
        selectedRoom,RoomNumber = selectedRoom.split('-')   
        for room in data['rooms']:
            if room['name'] == selectedRoom:    
                for dec in room['encoders']:
                    if dec['name']==ComboSour.get():
                       Esournameentry.insert(0,dec['name'])
                       Esouripentry.insert(0,dec['ip'])
                       Esourmultientry.insert(0,dec['multicast'])
        Esouripentry.bind('<Return>',Multiauto2)
        Esourmultientry.bind('<Return>',editsourinvoke)
        global firstsourname
        firstsourname = Esournameentry.get()
        global firstsourip
        firstsourip = Esouripentry.get()
        global firstsourmulti
        firstsourmulti = Esourmultientry.get()
def editsourinvoke(args):
    savesourbutton2.invoke()
def Editdeswindow():
    if ComboDes.get()!='בחר יעד':
        print("EditDestinationWindow")
        global editdesWindow
        editdesWindow = Toplevel(root)
        editdesWindow.title("ערוך יעד")
        editdesWindow.geometry("600x300")
        editdesWindow.resizable(0, 0)
        
        editdesWindow.iconphoto(False, image)
        editdesWindow.grid_rowconfigure(4, weight=1)
        editdesWindow.grid_columnconfigure(2, weight=1)
        all_frame = Frame(editdesWindow, bg='white',height=300,width=600)#minimum
        all_frame.grid(rowspan=4,columnspan=2,sticky="nsew")
        center_frame = Frame(editdesWindow, bg='#EEE9E9')#minimum
        center_frame.grid(row=1,rowspan=2 ,columnspan=2,sticky="nsew",padx=20)
        title = Label(editdesWindow,text="ערוך יעד", font = ("Times New Roman",24),bg='white')
        namelabel = Label(editdesWindow,text=":שם", font = ("Times New Roman",20), bg='#EEE9E9')
        global Edesnameentry
        Edesnameentry = Entry(editdesWindow,width=40,justify='right')
        iplabel = Label(editdesWindow,text=":IP", font = ("Times New Roman",20), bg='#EEE9E9')
        global Edesipentry
        Edesipentry = Entry(editdesWindow,width=40,justify='right')
        
        global savedesbutton2
        savedesbutton2 = Button(editdesWindow,text="שמור", font=(fon,17),fg='White', bg='#6495ED',relief='groove',width=10,command =partial(Editdes)) #לא מעביר
        cancelbutton = Button(editdesWindow,text="ביטול", font=(fon,17),fg='White', bg='#212121',relief='groove',width=10,command=editdesWindow.destroy)
        
        global Edeserrorlabel
        Edeserrorlabel =Label(editdesWindow,fg='red',bg='white', font=(fon,15))
        Edeserrorlabel.place(relx = 0.5,
                      rely = 0.85,
                      anchor ='center')
        
        title.grid(row=0, column=1, columnspan=2,sticky='e',padx=(0,25))
        namelabel.grid(row=1,column=1,sticky='e',padx=(0,25))
        Edesnameentry.grid(row=1,column=0,sticky='e',padx=(0,25))
        iplabel.grid(row=2,column=1,sticky='e',padx=(0,25))
        Edesipentry.grid(row=2,column=0,sticky='e',padx=(0,25))
        #addbutton2.grid(row=10,column=1)
        savedesbutton2.grid(row=3,column=1,sticky='e',padx=(0,25))
        cancelbutton.grid(row=3,column=0,sticky='w',padx=(25,0))
        filename = 'db.json'
        with open(filename,"r") as file:
            data = json.load(file)
        selectedRoom = ComboDesRoom.get()
        selectedRoom,RoomNumber = selectedRoom.split('-')   
        for room in data['rooms']:
            if room['name'] == selectedRoom:    
                for dec in room['decoders']:
                    if dec['name']==ComboDes.get():
                       Edesnameentry.insert(0,dec['name'])
                       Edesipentry.insert(0,dec['ip'])
        Edesipentry.bind('<Return>',editdesinvoke)

        global firstdesname
        firstdesname = Edesnameentry.get()
        global firstdesip
        firstdesip = Edesipentry.get()
def editdesinvoke(args):
    savedesbutton2.invoke()
def Editroomwindow():
    if Combo.get()!='בחר חמ"ל':
        print("EditRoomWindow")
        global editroomWindow
        editroomWindow = Toplevel(root)
        editroomWindow.title('ערוך חמ"ל')
        editroomWindow.geometry("600x300")
        editroomWindow.resizable(0, 0)
        
        editroomWindow.iconphoto(False, image)
        editroomWindow.grid_rowconfigure(4, weight=1)
        editroomWindow.grid_columnconfigure(2, weight=1)
        all_frame = Frame(editroomWindow, bg='white',height=300,width=600)#minimum
        all_frame.grid(rowspan=4,columnspan=2,sticky="nsew")
        center_frame = Frame(editroomWindow, bg='#EEE9E9')#minimum
        center_frame.grid(row=1,rowspan=2 ,columnspan=2,sticky="nsew",padx=20)
        title = Label(editroomWindow,text='ערוך חמ"ל', font = ("Times New Roman",24),bg='white')
        namelabel = Label(editroomWindow,text=":שם", font = ("Times New Roman",20), bg='#EEE9E9')
        global Eroomnameentry 
        Eroomnameentry = Entry(editroomWindow,width=40,justify='right')
        numberlabel = Label(editroomWindow,text=":מספר", font = ("Times New Roman",20), bg='#EEE9E9')
        global Eroomnumberentry
        Eroomnumberentry = Entry(editroomWindow,width=40,justify='right')
        
        global savebutton2
        savebutton2 = Button(editroomWindow,text="שמור", font=(fon,17),fg='White', bg='#6495ED',relief='groove',width=10,command =partial(Editroom,Combo.get())) #לא מעביר
        cancelbutton = Button(editroomWindow,text="ביטול", font=(fon,17),fg='White', bg='#212121',relief='groove',width=10,command=editroomWindow.destroy)
        
        global Eroomerrorlabel
        Eroomerrorlabel =Label(editroomWindow,fg='red',bg='white', font=(fon,15))
        Eroomerrorlabel.place(relx = 0.5,
                      rely = 0.85,
                      anchor ='center')
        
        title.grid(row=0, column=1, columnspan=2,sticky='e',padx=(0,25))
        namelabel.grid(row=1,column=1,sticky='e',padx=(0,25))
        Eroomnameentry.grid(row=1,column=0,sticky='e',padx=(0,25))
        numberlabel.grid(row=2,column=1,sticky='e',padx=(0,25))
        Eroomnumberentry.grid(row=2,column=0,sticky='e',padx=(0,25))
        #addbutton2.grid(row=10,column=1)
        savebutton2.grid(row=3,column=1,sticky='e',padx=(0,25))
        cancelbutton.grid(row=3,column=0,sticky='w',padx=(25,0))
        filename = 'db.json'
        with open(filename,"r") as file:
            data = json.load(file)
        selectedRoom = ComboDesRoom.get()
        selectedRoom,RoomNumber = selectedRoom.split('-')   
        for room in data['rooms']:
            if room['name'] == selectedRoom:                    
                   Eroomnameentry.insert(0,room['name'])
                   Eroomnumberentry.insert(0,room['number'])

        Eroomnumberentry.bind('<Return>',editroominvoke)

        global firstroomname
        firstroomname = Eroomnameentry.get()
        global firstroomnumber
        firstroomnumber = Eroomnumberentry.get()
def editroominvoke(args):
    savebutton2.invoke()
def Editroom(comboget):
    name = Eroomnameentry.get()
    number = Eroomnumberentry.get()
    #print(ip,name)
    flag =True #save
    if (name=='' or number==''):
        Eroomerrorlabel.configure(text='יש שדות ריקים*')
        flag =False
    elif firstroomname !=name: #old and new
        if ilegal(name):
            Eroomerrorlabel.configure(text='תו לא חוקי \ קיים כבר*')
            flag =False
    elif firstroomnumber !=number: #old and new
        if ilegal(number):
            Eroomerrorlabel.configure(text='תו לא חוקי \ קיים כבר*')
            flag =False
    #elif ilegal(name) or ilegal(number):
    #        Eroomerrorlabel.configure(text='תו לא חוקי \ קיים כבר*')
    if flag:
        filename = 'db.json'
        app = {
               "number": number,
               "name": name     
               }
        with open(filename,"r") as file:
            data = json.load(file)
        selectedRoom = comboget
        selectedRoom,RoomNumber = selectedRoom.split('-')   
        for room in data['rooms']:
            if room['number'] == RoomNumber:
                        room['number']=number
                        room['name']=name
        data['rooms'].sort(key=lambda x:
        x["number"])  

        with open(filename,"w") as file:
            json.dump(data,file)
            filename = 'db.json'
        with open(filename,"r") as file:
                data = json.load(file)
 
        vlist = []
        for room in data['rooms']:
            vlist.append('{}-{}'.format(room['name'], room['number']))

        RefreshAdd(vlist,name,number)

        editroomWindow.destroy()
    print('edit')
def Addsourwindow():
    print("AddSourceWindow")
    global newsourWindow
    newsourWindow = Toplevel(root)
    newsourWindow.title("מקור חדש")
    newsourWindow.geometry("600x300")
    newsourWindow.resizable(0, 0)
    
    newsourWindow.iconphoto(False, image)
    newsourWindow.grid_rowconfigure(5, weight=1)
    newsourWindow.grid_columnconfigure(2, weight=1)
    all_frame = Frame(newsourWindow, bg='white',height=300,width=600)#minimum
    all_frame.grid(rowspan=5,columnspan=2,sticky="nsew")
    center_frame = Frame(newsourWindow, bg='#EEE9E9')#minimum
    center_frame.grid(row=1,rowspan=3 ,columnspan=2,sticky="nsew",padx=20)
    title = Label(newsourWindow,text="מקור חדש", font = ("Times New Roman",24),bg='white')
    namelabel = Label(newsourWindow,text=":שם", font = ("Times New Roman",20), bg='#EEE9E9')
    global sournameentry
    sournameentry = Entry(newsourWindow,width=40,justify='right')
    iplabel = Label(newsourWindow,text=":IP", font = ("Times New Roman",20), bg='#EEE9E9')
    global souripentry
    souripentry = Entry(newsourWindow,width=40,justify='right')
    multilabel = Label(newsourWindow,text=":Multicast", font = ("Times New Roman",20), bg='#EEE9E9')
    global sourmultientry
    sourmultientry = Entry(newsourWindow,width=40,justify='right')
    global addsourbutton2
    addsourbutton2 = Button(newsourWindow,text="הוסף", font=(fon,17),fg='White', bg='#6495ED',relief='groove',width=10,command =partial(Addnewsour)) #לא מעביר
    cancelbutton = Button(newsourWindow,text="ביטול", font=(fon,17),fg='White', bg='#212121',relief='groove',width=10,command=newsourWindow.destroy)
    
    global sourerrorlabel
    sourerrorlabel =Label(newsourWindow,fg='red',bg='white', font=(fon,15))
    sourerrorlabel.place(relx = 0.5,
                  rely = 0.9,
                  anchor ='center')
    
    title.grid(row=0, column=1, columnspan=2,sticky='e',padx=(0,25))
    namelabel.grid(row=1,column=1,sticky='e',padx=(0,25))
    sournameentry.grid(row=1,column=0,sticky='e',padx=(0,25))
    iplabel.grid(row=2,column=1,sticky='e',padx=(0,25))
    souripentry.grid(row=2,column=0,sticky='e',padx=(0,25))
    #addbutton2.grid(row=10,column=1)
    multilabel.grid(row=3,column=1,sticky='e',padx=(0,25))
    sourmultientry.grid(row=3,column=0,sticky='e',padx=(0,25))
    addsourbutton2.grid(row=4,column=1,sticky='e',padx=(0,25))
    cancelbutton.grid(row=4,column=0,sticky='w',padx=(25,0))

    souripentry.bind('<Return>',Multiauto)
    sourmultientry.bind('<Return>',addsourinvoke)
def addsourinvoke(args):
    addsourbutton2.invoke()
def Multiauto2(args):
    if Esouripentry.get().count('.')==3:

        a,b,c,d=Esouripentry.get().split('.')
        if a=='30':
            a='230'
        elif a=='40':
            a='231'
        elif a=='50':
            a='225'
        multi=a+'.'+b+'.'+c+'.'+d
        Esourmultientry.delete(0, 'end')
        Esourmultientry.insert(0,multi)
def Multiauto(args):
    if souripentry.get().count('.')==3:

        a,b,c,d=souripentry.get().split('.')
        if a=='30':
            a='230'
        elif a=='40':
            a='231'
        elif a=='50':
            a='225'
        multi=a+'.'+b+'.'+c+'.'+d
        sourmultientry.delete(0, 'end')
        sourmultientry.insert(0,multi)
def Addroomwindow():
    print("Addroomwindow")
    global newWindow
    newWindow = Toplevel(root)
    newWindow.title("חמל חדש")
    newWindow.geometry("600x300")
    newWindow.resizable(0, 0)
    
    newWindow.iconphoto(False, image)
    newWindow.grid_rowconfigure(4, weight=1)
    newWindow.grid_columnconfigure(2, weight=1)
    text = Text(newWindow)
    all_frame = Frame(newWindow, bg='white',height=300,width=600)#minimum
    all_frame.grid(rowspan=4,columnspan=2,sticky="nsew")
    center_frame = Frame(newWindow, bg='#EEE9E9')#minimum
    center_frame.grid(row=1,rowspan=2 ,columnspan=2,sticky="nsew",padx=20)
    title = Label(newWindow,text="חמל חדש", font = ("Times New Roman",24),bg='white')
    namelabel = Label(newWindow,text=":שם", font = ("Times New Roman",20), bg='#EEE9E9')
    global nameentry
    nameentry = Entry(newWindow,width=40,justify='right')
    numberlabel = Label(newWindow,text=":מספר", font = ("Times New Roman",20), bg='#EEE9E9')
    global numberentry
    numberentry = Entry(newWindow,width=40,justify='right')
    
    global addroombutton2
    addroombutton2 = Button(newWindow,text="הוסף", font=(fon,17),fg='White', bg='#6495ED',relief='groove',width=10,command =partial(Addnewroom)) #לא מעביר
    cancelbutton = Button(newWindow,text="ביטול", font=(fon,17),fg='White', bg='#212121',relief='groove',width=10,command=newWindow.destroy)
    
    global errorlabel
    errorlabel =Label(newWindow,fg='red',bg='white', font=(fon,15))
    errorlabel.place(relx = 0.5,
                  rely = 0.85,
                  anchor ='center')
    
    title.grid(row=0, column=1, columnspan=2,sticky='e',padx=(0,25))
    namelabel.grid(row=1,column=1,sticky='e',padx=(0,25))
    nameentry.grid(row=1,column=0,sticky='e',padx=(0,25))
    numberlabel.grid(row=2,column=1,sticky='e',padx=(0,25))
    numberentry.grid(row=2,column=0,sticky='e',padx=(0,25))
    #addbutton2.grid(row=10,column=1)
    addroombutton2.grid(row=3,column=1,sticky='e',padx=(0,25))
    cancelbutton.grid(row=3,column=0,sticky='w',padx=(25,0))
    numberentry.bind('<Return>',addroominvoke)
def addroominvoke(args):
    addroombutton2.invoke()
def Deldeswindow():
    
    if (ComboDes.get() != 'בחר יעד'):
        global deldesWindow
        deldesWindow = Toplevel(root)
        deldesWindow.title("מחק יעד")
        deldesWindow.geometry("400x200")
        deldesWindow.resizable(0, 0)
        
        deldesWindow.iconphoto(False, image)
        deldesWindow.grid_rowconfigure(3, weight=1)
        deldesWindow.grid_columnconfigure(2, weight=1)
        all_frame = Frame(deldesWindow, bg='white',height=200,width=400)#minimum
        all_frame.grid(rowspan=4,columnspan=2,sticky="nsew")
        
        title = Label(deldesWindow,text="?האם אתה בטוח", font = ("Times New Roman",24),bg='white')
        
        yesbutton = Button(deldesWindow,text="כן", font=(fon,17),fg='White', bg='#6495ED',relief='groove',width=10,command =partial(Deldes))
        nobutton = Button(deldesWindow,text="לא", font=(fon,17),fg='White', bg='#212121',relief='groove',width=10,command=deldesWindow.destroy)
        
        title.grid(row=0, column=0, columnspan=2,sticky='e',padx=(0,25))
        
        yesbutton.grid(row=3,column=1,sticky='e',padx=(0,25))
        nobutton.grid(row=3,column=0,sticky='w',padx=(25,0))
def Delsourwindow():
    
    if (ComboSour.get() != 'בחר מקור'):
        global delsourWindow
        delsourWindow = Toplevel(root)
        delsourWindow.title("מחק מקור")
        delsourWindow.geometry("400x200")
        delsourWindow.resizable(0, 0)
        
        delsourWindow.iconphoto(False, image)
        delsourWindow.grid_rowconfigure(3, weight=1)
        delsourWindow.grid_columnconfigure(2, weight=1)
        all_frame = Frame(delsourWindow, bg='white',height=200,width=400)#minimum
        all_frame.grid(rowspan=4,columnspan=2,sticky="nsew")
        
        title = Label(delsourWindow,text="?האם אתה בטוח", font = ("Times New Roman",24),bg='white')
        
        yesbutton = Button(delsourWindow,text="כן", font=(fon,17),fg='White', bg='#6495ED',relief='groove',width=10,command =partial(Delsour))
        nobutton = Button(delsourWindow,text="לא", font=(fon,17),fg='White', bg='#212121',relief='groove',width=10,command=delsourWindow.destroy)
        
        title.grid(row=0, column=0, columnspan=2,sticky='e',padx=(0,25))
        
        yesbutton.grid(row=3,column=1,sticky='e',padx=(0,25))
        nobutton.grid(row=3,column=0,sticky='w',padx=(25,0))
def Delroomwindow():
    if (Combo.get() != 'בחר חמ"ל'):
        global delWindow
        delWindow = Toplevel(root)
        delWindow.title("מחק חמל")
        delWindow.geometry("400x200")
        delWindow.resizable(0, 0)
        
        delWindow.iconphoto(False, image)
        delWindow.grid_rowconfigure(3, weight=1)
        delWindow.grid_columnconfigure(2, weight=1)
        all_frame = Frame(delWindow, bg='white',height=200,width=400)#minimum
        all_frame.grid(rowspan=4,columnspan=2,sticky="nsew")
        
        title = Label(delWindow,text="?האם אתה בטוח", font = ("Times New Roman",24),bg='white')
        
        yesbutton = Button(delWindow,text="כן", font=(fon,17),fg='White', bg='#6495ED',relief='groove',width=10,command =partial(Delroom))
        nobutton = Button(delWindow,text="לא", font=(fon,17),fg='White', bg='#212121',relief='groove',width=10,command=delWindow.destroy)
        
        title.grid(row=0, column=0, columnspan=2,sticky='e',padx=(0,25))
        
        yesbutton.grid(row=3,column=1,sticky='e',padx=(0,25))
        nobutton.grid(row=3,column=0,sticky='w',padx=(25,0))
def Delroom():
    #print('del')
    #print(Combo.get())
    if (Combo.get() != 'בחר חמ"ל'):
        filename = 'db.json'
        with open(filename,"r") as file:
            data2 = json.load(file)
        
        #print('jj')
        selectedRoom = Combo.get()
        selectedRoom,RoomNumber = selectedRoom.split('-')   
        #print(selectedRoom)
        for room in data2['rooms']:
            if room['name'] == selectedRoom:
                data2['rooms'].remove(room)
        with open(filename,"w") as file:
            json.dump(data2,file)

        vlist = []
        f = open('db.json')
        data = json.load(f)
        for room in data['rooms']:
            vlist.append('{}-{}'.format(room['name'], room['number']))
        RefreshDel(vlist)
    delWindow.destroy()
def Deldes():
    if (ComboDes.get() != 'בחר יעד'):
        filename = 'db.json'
        with open(filename,"r") as file:
            data2 = json.load(file)       
        selectedRoom = ComboDesRoom.get()
        selectedRoom,RoomNumber = selectedRoom.split('-')   
        desname=ComboDes.get()
        for room in data2['rooms']:
            if room['name'] == selectedRoom:
                for dec in room['decoders']:
                    if dec['name']==desname:
                        room['decoders'].remove(dec)
        with open(filename,"w") as file:
            json.dump(data2,file)

        comboDesList = []
        decodersList.clear()
        for room in data2['rooms']:
            if room['number'] == RoomNumber:
                for dec in room['decoders']:
                   decodersList.append(Decoder(dec['ip'],dec['name']))
                   comboDesList.append(dec['name'])
        ComboDes.configure(value=comboDesList)
        ComboDes.set('')
        ComboDes.set('בחר יעד') 
    deldesWindow.destroy()
def Delsour():
    if (ComboSour.get() != 'בחר מקור'):
        filename = 'db.json'
        with open(filename,"r") as file:
            data2 = json.load(file)       
        selectedRoom = ComboSourRoom.get()
        selectedRoom,RoomNumber = selectedRoom.split('-')   
        sourname=ComboSour.get()
        for room in data2['rooms']:
            if room['name'] == selectedRoom:
                for enc in room['encoders']:
                    if enc['name']==sourname:
                        room['encoders'].remove(enc)
        with open(filename,"w") as file:
            json.dump(data2,file)

        comboSourList = []
        encodersList.clear()
        for room in data2['rooms']:
            if room['number'] == RoomNumber:
                for enc in room['encoders']:
                   encodersList.append(Encoder(enc['ip'],enc['multicast'],enc['name']))
                   comboSourList.append(enc['name'])
        ComboSour.configure(value=comboSourList)
        ComboSour.set('')
        ComboSour.set('בחר מקור') 
    delsourWindow.destroy()
def Addnewroom():
    name = nameentry.get()
    number = numberentry.get()
    #print(number,name)
    if (name=='' or number==''):
        errorlabel.configure(text='יש שדות ריקים*')
    elif ilegal(name) or ilegal(number):
        errorlabel.configure(text='תו לא חוקי \ קיים כבר*')
    else:
        filename = 'db.json'
        app = {
               "number": number,
               "name": name,
               "encoders": [],
               "decoders": []
               }
        with open(filename,"r") as file:
            data = json.load(file)
        data['rooms'].append(app)
        data['rooms'].sort(key=lambda x:
        x["number"])    #sort db by number

        with open(filename,"w") as file:
            json.dump(data,file)

        
        newWindow.destroy()
        vlist = []
        f = open('db.json')
        data = json.load(f)
        for room in data['rooms']:
            vlist.append('{}-{}'.format(room['name'], room['number']))
        RefreshAdd(vlist,name,number)
def Addnewdes():
    #if בחר
    if ComboDesRoom.get()!='בחר חמ"ל':
        name = desnameentry.get()
        ip = desipentry.get()
        #print(ip,name)
        if (name=='' or ip==''):
            deserrorlabel.configure(text='יש שדות ריקים*')
        elif ilegalonly(name) or ilegal(ip):
            deserrorlabel.configure(text='תו לא חוקי \ קיים כבר*')
            #print('empty')
        else:
            filename = 'db.json'
            app = {
                   "ip": ip,
                   "name": name     
                   }
            with open(filename,"r") as file:
                data = json.load(file)
            selectedRoom = ComboDesRoom.get()
            selectedRoom,RoomNumber = selectedRoom.split('-')   
            for room in data['rooms']:
                if room['name'] == selectedRoom:

                    #data[room].append(app)

                    room['decoders'].append(app)
                    room['decoders'].sort(key=lambda x:
                    x["ip"])  
            
            with open(filename,"w") as file:
                json.dump(data,file)
        
            
            comboDesList = []
            decodersList.clear()
            for room in data['rooms']:
                if room['number'] == RoomNumber:
                    for dec in room['decoders']:
                       decodersList.append(Decoder(dec['ip'],dec['name']))
                       comboDesList.append(dec['name'])
            ComboDes.configure(value=comboDesList)

            ComboDes.set(name)
            newdesWindow.destroy()
def Editsour():
    if ComboSourRoom.get()!='בחר חמ"ל':
        name = Esournameentry.get()
        ip = Esouripentry.get()
        multi= Esourmultientry.get()
        #print(ip,name)
        flag = True
        if (name=='' or ip=='' or multi==''):
            Esourerrorlabel.configure(text='יש שדות ריקים *')
        elif firstsourname !=name: #old and new
            if ilegalonly(name):
                Esourerrorlabel.configure(text='תו לא חוקי / קיים כבר*')
                flag =False
        elif firstsourip !=ip: #old and new
            if ilegal(ip):
                Esourerrorlabel.configure(text='תו לא חוקי / קיים כבר*')
                flag =False
        elif firstsourmulti !=multi: #old and new
            if ilegal(multi):
                Esourerrorlabel.configure(text='תו לא חוקי / קיים כבר*')
                flag =False
        #elif ilegal(name) or ilegal(ip) or ilegal(multi):
        #    Esourerrorlabel.configure(text='תו לא חוקי \ קיים כבר*')
        if flag:
            filename = 'db.json'
            app = {
                   "ip": ip,
                   "multicast": multi,
                   "name": name     
                   }
            with open(filename,"r") as file:
                data = json.load(file)
            selectedRoom = ComboSourRoom.get()
            selectedRoom,RoomNumber = selectedRoom.split('-')   

            for room in data['rooms']:
                if room['number'] == RoomNumber:
                    for enc in room['encoders']:
                        if enc['name']==ComboSour.get():
                            #room['encoders'].remove(enc)
                            #room['encoders'].append(app)
                            enc['ip']=ip
                            enc['multicast']=multi
                            enc['name']=name
                            room['encoders'].sort(key=lambda x:
                            x["ip"])  
                            encodersList.append(Encoder(enc['ip'],enc['multicast'],enc['name']))

                            with open(filename,"w") as file:
                                json.dump(data,file)
                            comboSourList = []
                            encodersList.clear()
                            filename = 'db.json'
                            with open(filename,"r") as file:
                                    data = json.load(file)
                            for room in data['rooms']:
                                if room['number'] == RoomNumber:
                                    for enc in room['encoders']:
                                       encodersList.append(Encoder(enc['ip'],enc['multicast'],enc['name']))
                                       comboSourList.append(enc['name'])
                            ComboSour.configure(value=comboSourList)
                            ComboSour.set("")                         
                            ComboSour.set(name)


            
            editsourWindow.destroy()
    print('edit')
def Editdes():
    if ComboDesRoom.get()!='בחר חמ"ל':
        name = Edesnameentry.get()
        ip = Edesipentry.get()
        #print(ip,name)
        flag =True #save
        if (name=='' or ip==''):
            Edeserrorlabel.configure(text='יש שדות ריקים*')
            flag =False
        elif firstdesname !=name: #old and new
            if ilegalonly(name):
                Edeserrorlabel.configure(text='תו לא חוקי \ קיים כבר*')
                flag =False
        elif firstdesip !=ip: #old and new
            if ilegal(ip):
                Edeserrorlabel.configure(text='תו לא חוקי \ קיים כבר*')
                flag =False
        #elif ilegal(name) or ilegal(ip):
        #    Edeserrorlabel.configure(text='תו לא חוקי \ קיים כבר*')
        #else:
        if flag:
            filename = 'db.json'
            app = {
                   "ip": ip,
                   "name": name     
                   }
            with open(filename,"r") as file:
                data = json.load(file)
            selectedRoom = ComboDesRoom.get()
            selectedRoom,RoomNumber = selectedRoom.split('-')   

            #comboDesList = []
            #decodersList.clear()
            for room in data['rooms']:
                if room['number'] == RoomNumber:
                    for dec in room['decoders']:
                        if dec['name']==ComboDes.get():
                            #room['decoders'].remove(dec)
                            #room['decoders'].append(app)
                            dec['ip']=ip
                            dec['name']=name
                            room['decoders'].sort(key=lambda x:
                            x["ip"])  
                            decodersList.append(Decoder(dec['ip'],dec['name']))

                            with open(filename,"w") as file:
                                json.dump(data,file)
                            comboDesList = []
                            decodersList.clear()
                            filename = 'db.json'
                            with open(filename,"r") as file:
                                    data = json.load(file)
                            for room in data['rooms']:
                                if room['number'] == RoomNumber:
                                    for dec in room['decoders']:
                                       decodersList.append(Decoder(dec['ip'],dec['name']))
                                       comboDesList.append(dec['name'])
                            ComboDes.configure(value=comboDesList)
                            ComboDes.set("")
                            ComboDes.set("בחר יעד")



                           

                            ComboDes.set(name)


            
            editdesWindow.destroy()
    print("edited")
def Addnewsour():
    #print("new sour")
    if ComboSourRoom.get()!='בחר חמ"ל':
        name = sournameentry.get()
        ip = souripentry.get()
        multi=sourmultientry.get()
        #print(ip,name,multi)
        if (name=='' or ip=='' or multi==''):
            #print('empty')
            sourerrorlabel.configure(text='יש שדות ריקים*')
        elif ilegalonly(name) or ilegal(ip) or ilegal(multi):
            sourerrorlabel.configure(text='תו לא חוקי \ קיים כבר*')
        else:
            filename = 'db.json'
            app = {
                   "ip": ip,
                   "multicast": multi,
                   "name": name                  
                   }
            with open(filename,"r") as file:
                data = json.load(file)
            selectedRoom = ComboSourRoom.get()
            selectedRoom,RoomNumber = selectedRoom.split('-')   
            for room in data['rooms']:
                if room['name'] == selectedRoom:

                    #data[room].append(app)

                    room['encoders'].append(app)
                    room['encoders'].sort(key=lambda x:
                    x["ip"])  
            
            with open(filename,"w") as file:
                json.dump(data,file)
        
            
            comboSourList = []
            encodersList.clear()
            for room in data['rooms']:
                if room['number'] == RoomNumber:
                    for enc in room['encoders']:
                       encodersList.append(Encoder(enc['ip'],enc['multicast'],enc['name']))
                       comboSourList.append(enc['name'])
            ComboSour.configure(value=comboSourList)

            ComboSour.set(name)
            newsourWindow.destroy()
def RefreshAdd(vlist,name,number):
    print('refresh')
    
    Combo.configure(value=vlist)
    Combo.set('')
    Combo.set('{}-{}'.format(name,number))
    ComboDesRoom.configure(value=vlist)
    ComboDesRoom.set('')
    ComboDesRoom.set('{}-{}'.format(name,number))
    ComboSourRoom.configure(value=vlist)
    ComboSourRoom.set('')
    ComboSourRoom.set('{}-{}'.format(name,number))

    emptylist=[]
    ComboDes.set('')
    ComboDes.set('בחר יעד')
    ComboDes.configure(value=emptylist)
    ComboSour.set('')
    ComboSour.set('בחר מקור')
    ComboSour.configure(value=emptylist)
    
def RefreshDel(vlist):
    print('refresh')
    
    Combo.configure(value=vlist)
    Combo.set('')
    Combo.set('בחר חמ"ל')
    ComboDesRoom.configure(value=vlist)
    ComboDesRoom.set('בחר חמ"ל')
    ComboSourRoom.configure(value=vlist)
    ComboSourRoom.set('בחר חמ"ל')
    ComboDes.set('')
    ComboDes.set('בחר יעד')
    ComboDes.configure(value=[])
    ComboSour.set('')
    ComboSour.set('בחר מקור')
    ComboSour.configure(value=[])
def threadping(ip):
    if ping(ip.ip): #If ping test is 0, it' reachable     
           reached.append(ip)
    else:
           not_reached.append(ip)           
def threadping2(ip):
    if ping(ip.ip): #If ping test is 0, it' reachable     
           reached2.append(ip)
    else:
           not_reached2.append(ip)           

def Check():
    selectedRoom = Combo.get()
    if selectedRoom != 'בחר חמ"ל':
        #global checkWindow
        checkWindow= Toplevel(root)
        checkWindow.title("בודק- לא לגעת")
        checkWindow.geometry("600x300")
        #checkWindow.resizable(0, 0)
        #global bg_frame
        bgfram=Frame(checkWindow,bg='white')
        bgfram.pack(expand=True, fill=BOTH)

        yscrollbar2 = Scrollbar(bgfram)
        
        

        bg_frame=Listbox(bgfram,yscrollcommand = yscrollbar2.set,height=200,
                        selectmode = "multiple", justify='center',font=('Times New Roman', 18))
        yscrollbar2.config(command = bg_frame.yview),
        


        #bg_frame.bind("<<ListboxSelect>>",
        #                  lambda: listbox.selection_clear(0, 'end'))
        #
       # def no_selection():
       #     bg_frame.selection_clear(index)
        #list = checkWindow.pack_slaves()
        #for l in list:
        #    l.destroy()
        l1 = Label(bgfram,font = ("Times New Roman",24), bg='white',
        text='{} סטטוס'.format(Combo.get())).pack()
        checkWindow.iconphoto(False, image)

        #global yscrollbar
        
        #bg_frame.config(width=300,height=300)
        #bg_frame.config(yscrollcommand=yscrollbar.set)
        #bg_frame.pack(fill=BOTH)
        bg_frame.pack(fill=BOTH)
        yscrollbar2.pack(side="right",fill="y")
        global reached
        reached= []                           #Empty list to collect reachable hosts
        global not_reached
        not_reached = []                          #Empty list to collect unreachable hosts

        threads=[]
        for ip in encodersList:
            #t=threading.Thread(target=ping,args=[ip.ip])
            t=threading.Thread(target=threadping,args=[ip])
            #t.start()
            #threads.append(t)

            #if ping(ip.ip): 
                               #If ping test is 0, it' reachable     
            t.start()       
            #if t.start():
            #    reached.append(ip)
            #else:
            #    not_reached.append(ip)                              #Else, it's not reachable
            threads.append(t)
        for ip in decodersList:
            t=threading.Thread(target=threadping,args=[ip])
            #if ping(ip.ip):                    #If ping test is 0, it' reachable
            #if t.start():
            #    reached.append(ip)
            #
            #else:
            #    not_reached.append(ip) 
            t.start() 
            threads.append(t)

        for thread in threads:
            thread.join()

        for x in reached:
            bg_frame.insert(END, "{} {} עם רשת".format(x.name,x.ip))
            bg_frame.itemconfig(bg_frame.index("end")-1, {'bg':'green'})
            bg_frame.itemconfig(bg_frame.index("end")-1,{'fg':'white'})
            #Label(bg_frame,text="{} {} עם רשת".format(x.name,x.ip),font=("Times New Roman",13),fg='#006400').pack()
        for x in not_reached:
            bg_frame.insert(END, "{} {} בלי רשת".format(x.name,x.ip))
            bg_frame.itemconfig(bg_frame.index("end")-1, {'bg':'red'})
            bg_frame.itemconfig(bg_frame.index("end")-1,{'fg':'white'})
            #Label(bg_frame,text="{} {} ללא רשת".format(x.name,x.ip),font=("Times New Roman",13),fg='#FF0000').pack()
def statusdes2():
    #print('2')
    selectedecoders=[]
    listcur=list.curselection()
    for i in listcur:
        op=list.get(i)
        selectedecoders.append(op)
    
    tempdecip = 0#check later
    tempenip = 0
    decsclas=[]
    for dec in decodersList:
         if dec.name in selectedecoders:
                 decsclas.append(dec)

    if len(selectedecoders)!= 0:
        checkWindow = Toplevel(root)
        checkWindow.title("בודק- לא לגעת")
        checkWindow.geometry("600x300")
        bgfram=Frame(checkWindow,bg='white')
        bgfram.pack(fill=BOTH)
        yscrollbar2 = Scrollbar(bgfram)
        bg_frame=Listbox(bgfram,yscrollcommand = yscrollbar2.set,height=200,
                        selectmode = "multiple", justify='center',font=('Times New Roman', 18))
        yscrollbar2.config(command = bg_frame.yview)

        l1 = Label(bgfram,font = ("Times New Roman",24), bg='white',
        text='{} סטטוס'.format(Combo.get())).pack()
        checkWindow.iconphoto(False, image)



        bg_frame.pack(fill=BOTH)
        yscrollbar2.pack(side="right",fill="y")
        global reached2
        reached2= []                           #Empty list to collect reachable hosts
        global not_reached2
        not_reached2 = []                          #Empty list to collect unreachable hosts

        threads=[]
        for ip in decsclas:
            t=threading.Thread(target=threadping2,args=[ip])  
            t.start()                                   #Else, it's not reachable
            threads.append(t)


        for thread in threads:
            thread.join()

        for x in reached2:
            bg_frame.insert(END, "{} {} עם רשת".format(x.name,x.ip))
            bg_frame.itemconfig(bg_frame.index("end")-1, {'bg':'green'})
            bg_frame.itemconfig(bg_frame.index("end")-1,{'fg':'white'})
            #Label(bg_frame,text="{} {} עם רשת".format(x.name,x.ip),font=("Times New Roman",13),fg='#006400').pack()
        for x in not_reached2:
            bg_frame.insert(END, "{} {} בלי רשת".format(x.name,x.ip))
            bg_frame.itemconfig(bg_frame.index("end")-1, {'bg':'red'})
            bg_frame.itemconfig(bg_frame.index("end")-1,{'fg':'white'})

        #reached = []                           #Empty list to collect reachable hosts
        #not_reached = []                          #Empty list to collect unreachable hosts
        #
        #
        #for decip in decsclas:
        #    if ping(decip.ip):                    #If ping test is 0, it' reachable
        #        reached.append(decip)
        #    else:
        #        not_reached.append(decip)     
        #
        #
        #
        #for x in reached:
        #    Label(checkWindow,text="{} {} עם רשת".format(x.name,x.ip),font=("Times New Roman",13),fg='#006400').pack()
        #for x in not_reached:
        #    Label(checkWindow,text="{} {} ללא רשת".format(x.name,x.ip),font=("Times New Roman",13),fg='#FF0000').pack()
def statusdes():
    if ComboDes.get()!='בחר יעד':
        #print ('ping ')
        filename = 'db.json'
   
        with open(filename,"r") as file:
            data = json.load(file)
        selectedRoom = ComboDesRoom.get()
        selectedRoom,RoomNumber = selectedRoom.split('-')   

        for room in data['rooms']:
            if room['number'] == RoomNumber:
                for dec in room['decoders']:
                    if dec['name']==ComboDes.get():
                        #print ('ping ', dec['ip'])
                        if ping(dec['ip']):                      
                            statdes.configure(bg='#00FF00')                       
                        else:
                            statdes.configure(bg='#FF0000')           
def statussour():
    if ComboSour.get()!='בחר מקור':
        #print ('ping ')
        filename = 'db.json'
   
        with open(filename,"r") as file:
            data = json.load(file)
        selectedRoom = ComboSourRoom.get()
        selectedRoom,RoomNumber = selectedRoom.split('-')   

        for room in data['rooms']:
            if room['number'] == RoomNumber:
                for enc in room['encoders']:
                    if enc['name']==ComboSour.get():
                        #print ('ping ', dec['ip'])
                        if ping(enc['ip']):                      
                            statsour.configure(bg='#00FF00')                       
                        else:
                            statsour.configure(bg='#FF0000')    
def rebootdes():
    if ComboDes.get()!='בחר יעד':
        #print ('ping ')
        filename = 'db.json'
   
        with open(filename,"r") as file:
            data = json.load(file)
        selectedRoom = ComboDesRoom.get()
        selectedRoom,RoomNumber = selectedRoom.split('-')   

        for room in data['rooms']:
            if room['number'] == RoomNumber:
                for dec in room['decoders']:
                    if dec['name']==ComboDes.get():
                        #print ('reboot  ', dec['ip'])
                        reboot(dec['ip'])
def rebootdes2():
    selectedecoders=[]
    listcur=list.curselection()
    for i in listcur:
        op=list.get(i)
        selectedecoders.append(op)
    
    tempdecip = 0#check later
    tempenip = 0
    decsclas=[]
    for dec in decodersList:
         if dec.name in selectedecoders:
                 decsclas.append(dec)

    #selectedRoom = ComboSour.get()
    #if selectedRoom != "בחר מקור":
    #    for enc in encodersList:
    #        if enc.name == selectedRoom:
    #            encip = enc#for execute
    #            tempenip = 1
    if len(selectedecoders)!= 0:
        threads=[]#
        for decip in decsclas:
            t=threading.Thread(target=reboot,args=[decip.ip])  
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()#
def rebootsour():
    if ComboSour.get()!='בחר מקור':
        #print ('ping ')
        filename = 'db.json'
   
        with open(filename,"r") as file:
            data = json.load(file)
        selectedRoom = ComboSourRoom.get()
        selectedRoom,RoomNumber = selectedRoom.split('-')   

        for room in data['rooms']:
            if room['number'] == RoomNumber:
                for enc in room['encoders']:
                    if enc['name']==ComboSour.get():
                        reboot(enc['ip'])
def getdecoders():
    decoders=[]
    if ComboDesRoom.get() != 'בחר חמ"ל':
        selectedRoom = ComboDesRoom.get()
        selectedRoom,RoomNumber = selectedRoom.split('-')
        #comboDesList = []
        #decodersList.clear()
        filename = 'db.json'
        with open(filename,"r") as file:
                data = json.load(file)
        for room in data['rooms']:
            if room['number'] == RoomNumber:
                for dec in room['decoders']:
                   decoders.append(dec['name'])
                   #comboDesList.append(dec['name'])
    else:
        decoders.append('לא נבחר חמ"ל')
    return decoders
def nothing():
    pass
def ilegalonly(str):
    flag = False
    if '-' in str:
        flag = True
    return flag
def ilegal(str):
    flag = False
    if '-' in str:
        flag = True

    filename = 'db.json'
    with open(filename,"r") as file:
        data = json.load(file)

    for room in data['rooms']:
        if room['name'] == str:
            flag = True
        elif room['number'] == str:
            flag = True

        for dec in room['decoders']:
            if dec['ip']==str:
                flag = True
            elif dec['name']==str:
                flag = True
        for enc in room['encoders']:
            if enc['ip']==str:
                flag = True
            elif enc['name']==str:
                flag = True
            elif enc['multicast']==str:
                flag = True

    return flag
def info():
    print('info')
    infoWindow = Toplevel(root)
    infoWindow.title("מידע")
    infoWindow.geometry("800x400")
    infoWindow.resizable(0, 0)
    
    infoWindow.iconphoto(False, image)
    infoWindow.grid_rowconfigure(2, weight=1)
    infoWindow.grid_columnconfigure(2, weight=1)
    all_frame = Frame(infoWindow, bg='white',height=400,width=800)#minimum
    all_frame.grid(rowspan=4,columnspan=2,sticky="nsew")
    
    title = Label(infoWindow,text="SQUID", font = ("Times New Roman",24),bg='white')
    
    #yesbutton = Button(infoWindow,text="כן", font=(fon,17),fg='White', bg='#6495ED',relief='groove',width=10)
    #nobutton = Button(infoWindow,text="לא", font=(fon,17),fg='White', bg='#212121',relief='groove',width=10,command=infoWindow.destroy)
    
    title.grid(row=0, column=0, columnspan=2,sticky='ew')

    mycanvas = Canvas(all_frame, height=400, width=800,bg='red')
    #myframe_inner = Frame(mycanvas)
    myscroll = Scrollbar(all_frame, orient='vertical', command=mycanvas.yview)
    mycanvas.configure(yscrollcommand=myscroll.set)
    
    mycanvas.grid(rowspan=2,columnspan=2, sticky='nesw')
    myscroll.grid(row=0,rowspan=2,column=1, sticky='nse')
    #mycanvas.create_window(0, 0, window=myframe_inner, anchor='nw')

    #mylabel=Label(mycanvas,bg='green')
    #mylabel.grid(row=1,column=0)

    #yesbutton.grid(row=3,column=1,sticky='e',padx=(0,25))
    #nobutton.grid(row=3,column=0,sticky='w',padx=(25,0))

f = open('db.json')
data = json.load(f)
#f.close() close in end

root = Tk()
root.title('SQUID')
root.resizable(0, 0)

root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(6, weight=1)







top_frame = Frame(root, bg='white')#minimum
top_frame.grid(rowspan=7,columnspan=6,sticky="nsew")

right_frame = Frame(root, bg='#EEE9E9',height=240)#minimum
right_frame.grid(row=1,rowspan=5,column=3,columnspan=3,sticky="nsew",padx=(0,10),pady=(0,10))
left_frame = Frame(root, bg='#EEE9E9',height=210)#minimum
left_frame.grid(row=1,rowspan=5,column=0,columnspan=3,sticky="nsew",padx=(5,10),pady=(0,10))
#style parameters
fon = "Times New Roman"

root.option_add("*TCombobox*Listbox*justify", 'right')
root.option_add("*TCombobox*justify", 'right')
root.option_add("*TCombobox*Listbox*font", (fon,12))


image = PhotoImage(file="383.png")
labelgdud = Label(root, image=image,bg='white').grid(column=0,row=0,padx=20)
root.iconphoto(False, image)

# create the widgets for the top frame
addroom = Button(root,text="הוסף", font=(fon,15),fg='White', bg='#6495ED',relief='groove',width=4,command = Addroomwindow)
delroom = Button(root,text="מחק", font=(fon,15),fg='White', bg='#212121',relief='groove',width=4,command=Delroomwindow)
editroom = Button(root,text="ערוך", font=(fon,15),fg='White', bg='#B0B0B0',relief='groove',width=4,command = Editroomwindow)
checkroom = Button(root,text="בדיקה", font=(fon,15),fg='White', bg='#E3A869',relief='groove',width=4,command = Check)
vlist = []
for room in data['rooms']:
    vlist.append('{}-{}'.format(room['name'], room['number']))
global Combo
Combo = ttk.Combobox(root,value=vlist, font=(fon,20), state='readonly')
Combo.set('בחר חמ"ל')
roomlabel = Label(root, text='חמ"ל', font=(fon,24), bg="white")

# layout the widgets in the top frame
addroom.grid(row=0,column=2,sticky="e",padx=(0,10))
delroom.grid(row=0,column=2,sticky="e",padx=(0,75))
editroom.grid(row=0,column=2,sticky="e",padx=(0,140))
checkroom.grid(row=0,column=2,sticky="e",padx=(0,205))
Combo.grid(row=0,column=3,columnspan=2)
roomlabel.grid(row=0,column=5,pady=5)

Combo.bind('<<ComboboxSelected>>', RoomSelected)



deslabel = Label(root, text='יעד',font=(fon,18),bg="#EEE9E9")
deslabel.grid(row=1,column=5)
ComboDesRoom = ttk.Combobox(root,value=vlist, font=(fon,12), state='readonly',width=30)
ComboDesRoom.set('בחר חמ"ל')
ComboDesRoom.grid(row=2,column=5,padx=20,pady=7)
deslist = []
ComboDes = ttk.Combobox(root,value=deslist, font=(fon,13), state='readonly')
ComboDes.set('בחר יעד')
ComboDes.grid(row=2,column=4)
adddes = Button(root,text="הוסף", font=(fon,11),fg='White', bg='#6495ED',width=4,relief='flat',command = Adddeswindow)
adddes.grid(row=2,column=3,padx=10)
remdes = Button(root,text="מחק", font=(fon,11),fg='White', bg='#212121',width=4,relief='flat',command=Deldeswindow)
remdes.grid(row=3,column=3)
editdes = Button(root,text="ערוך", font=(fon,11),fg='White', bg='#B0B0B0',width=4,relief='flat',command = Editdeswindow)
editdes.grid(row=4,column=3,pady=4)
statdes = Button(root,text="סטטוס", font=(fon,11),bg='white',width=6,height=2,relief='flat',command=statusdes)
statdes.grid(row=5,column=3,pady=(50,20))
rebdes = Button(root,text="reboot", font=(fon,11),fg='White', bg='#FF7F50',width=4, height=0,relief='flat',command=rebootdes)
rebdes.grid(row=5,column=3,pady=(0,40))
ComboDes.bind('<<ComboboxSelected>>', DesSelected)

sourlabel = Label(root, text='מקור',font=(fon,18),bg="#EEE9E9").grid(row=1,column=2)
ComboSourRoom = ttk.Combobox(root,value=vlist, font=(fon,12), state='readonly',width=30)
ComboSourRoom.set('בחר חמ"ל')
ComboSourRoom.grid(row=2,column=2,padx=20,pady=7)
sourlist = []
ComboSour = ttk.Combobox(root,value=sourlist, font=(fon,13), state='readonly')
ComboSour.set('בחר מקור')
ComboSour.grid(row=2,column=1)
addsour = Button(root,text="הוסף", font=(fon,11),fg='White', bg='#6495ED',width=4,relief='flat',command = Addsourwindow)
addsour.grid(row=2,column=0,padx=10)
remsour = Button(root,text="מחק", font=(fon,11),fg='White', bg='#212121',width=4,relief='flat',command=Delsourwindow)
remsour.grid(row=3,column=0)
editsour = Button(root,text="ערוך", font=(fon,11),fg='White', bg='#B0B0B0',width=4,relief='flat',command = Editsourwindow)
editsour.grid(row=4,column=0,pady=4)
statsour = Button(root,text="סטטוס", font=(fon,11),bg='white',width=6,height=2,relief='flat',command=statussour)
statsour.grid(row=5,column=0,pady=(50,20))
rebsour = Button(root,text="reboot", font=(fon,11),fg='White', bg='#FF7F50',width=4, height=0,relief='flat',command=rebootsour)
rebsour.grid(row=5,column=0,pady=(0,40))
ComboSour.bind('<<ComboboxSelected>>', SourSelected)

do = Button(root,text="ניתוב", command=Do, font=(fon,17),fg='White', bg='#6495ED',width=10,relief='groove')
do.grid(row=6, columnspan=6,pady=10)

ComboDesRoom.bind('<<ComboboxSelected>>', DesRoomSelected)
ComboSourRoom.bind('<<ComboboxSelected>>', SourRoomSelected)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
#filemenu.add_command(label="New")
#filemenu.add_command(label="Open")
#filemenu.add_command(label="Save")
#filemenu.add_command(label="Save as...")
#filemenu.add_command(label="Close")
#
#filemenu.add_separator()
#filemenu.add_command(label="Exit", command=root.quit)
#menubar.add_cascade(label="File", menu=filemenu)
#editmenu = Menu(menubar, tearoff=0)
#editmenu.add_command(label="Undo")
#
#editmenu.add_separator()
#
#editmenu.add_command(label="Cut")
#editmenu.add_command(label="Copy")
#editmenu.add_command(label="Paste")
#editmenu.add_command(label="Delete")
#editmenu.add_command(label="Select All")

#menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="עזרה")
#helpmenu.add_command(label="מידע",command=info)
helpmenu.add_command(label="מידע")

#menubar.add_cascade(label="Help")
menubar.add_cascade(label="?", menu=helpmenu)
root.config(menu=menubar)

addroom.bind('<Enter>', blue1_enter)
addroom.bind('<Leave>', blue1_leave)
delroom.bind('<Enter>', gray1_enter)
delroom.bind('<Leave>', gray1_leave)
editroom.bind('<Enter>', edit3_enter)
editroom.bind('<Leave>', edit3_leave)
adddes.bind('<Enter>', blue2_enter)
adddes.bind('<Leave>', blue2_leave)
remdes.bind('<Enter>', gray2_enter)
remdes.bind('<Leave>', gray2_leave)
addsour.bind('<Enter>', blue3_enter)
addsour.bind('<Leave>', blue3_leave)
remsour.bind('<Enter>', gray3_enter)
remsour.bind('<Leave>', gray3_leave)
do.bind('<Enter>', blue4_enter)
do.bind('<Leave>', blue4_leave)
editdes.bind('<Enter>', edit1_enter)
editdes.bind('<Leave>', edit1_leave)
editsour.bind('<Enter>', edit2_enter)
editsour.bind('<Leave>', edit2_leave)
checkroom.bind('<Enter>', check_enter)
checkroom.bind('<Leave>', check_leave)
rebdes.bind('<Enter>', reb1_enter)
rebdes.bind('<Leave>', reb1_leave)
rebsour.bind('<Enter>', reb2_enter)
rebsour.bind('<Leave>', reb2_leave)

is_on = True
#is_onflag=True
my_label = Label(root,
    text = "The Switch Is On!",
    fg = "green",
    font = ("Helvetica", 32))
 
#my_label.grid(pady = 20)
 
# Define our switch function
def switch():
    global is_on
     
    # Determine is on or off
    if is_on:
        on_button.configure(image = on)
        deslabel.configure(text = "יעדים", fg = "#104E8B")

        global yscrollbar
        yscrollbar = Scrollbar(root)
          
        #label = Label(window,
        #              text = "Select the languages below :  ",
        #              font = ("Times New Roman", 10), 
        #              padx = 10, pady = 10)
        #label.pack()
        global list
        list = Listbox(root, selectmode = "multiple",width=26, height=10, justify='right',font=('Times New Roman', 12),
                       yscrollcommand = yscrollbar.set)
          
        # Widget expands horizontally and 
        # vertically by assigning both to
        # fill option
        #list.pack(padx = 10, pady = 10,
          #        expand = YES, fill = "both")
          
        x =["C", "C++", "C#", "Java", "Python",
            "R", "Go", "Ruby", "JavaScript", "Swift",
            "SQL", "Perl", "XML","C", "C++", "C#", "Java", "Python",
            "R", "Go", "Ruby", "JavaScript", "Swift",
            "SQL", "Perl", "XML"]
        x=getdecoders()  
        for each_item in range(len(x)):
              
            list.insert(END, x[each_item])
            #list.itemconfig(each_item, bg = "lime")
          
        # Attach listbox to vertical scrollbar
        yscrollbar.config(command = list.yview)
        list.place(relx=0.565,rely=0.3)#place
        yscrollbar.grid(row=2,rowspan=4,column=4,sticky='nse')
        #Main = Canvas(root,background="blue", height = 500,width =500)
        #Main.configure(scrollregion=Main.bbox("all"))
        #if keep==False:
        is_on = False

        do.configure(command=Do2)
        rebdes.configure(command=rebootdes2)
        statdes.configure(command=statusdes2)
        adddes.configure(command = nothing, bg='#212121')
        remdes.configure(command = nothing, bg='#212121')
        editdes.configure(command = nothing, bg='#212121')
        

            #print(list.get(i))
        #is_onflag=not is_onflag
    else:
        

        on_button.config(image = off)
        deslabel.configure(text = "יעד",
                        fg = "black")       
        yscrollbar.destroy()
        list.destroy()
        is_on = True
        do.configure(command=Do)
        rebdes.configure(command=rebootdes)
        statdes.configure(command=statusdes)
        adddes.configure(command = Adddeswindow, bg='#6495ED')
        remdes.configure(command = Deldeswindow, bg='#212121')
        editdes.configure(command = Editdeswindow, bg='#B0B0B0')
        #is_onflag=not is_onflag
# Define Our Images
on = PhotoImage(file = "on.png")
off = PhotoImage(file = "off.png")
 
# Create A Button
on_button = Button(root, image = off, bd = 0,
                   #command = partial(switch,False))
                   command = (switch))
#on_button.place(relx = 0.95, rely = 0.27, anchor = CENTER)

root.mainloop()
