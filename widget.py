from tkinter import *
import requests
from PIL import ImageTk, Image
from io import BytesIO

import os.path
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import importlib

from tkinter import messagebox 


root = Tk()
root.geometry("620x620+0+0")
root.title("MY WIDGET")
root.resizable(0, 0)
root.config(bg="#053d69")
image = Image.open('bgg.jpg')
image = image.resize((620, 620), Image.ANTIALIAS)
my_img = ImageTk.PhotoImage(image)
img = Label(root,image = my_img)
img.pack()
F1 = Frame(root,bg="#0096C7")
F1.place(x=20, y=20,width=280,height=280)

F3 = Frame(root,bg="#0096C7")
F3.place(x=20, y=320,width=280,height=280)
F4 = Frame(root,bg="#0096C7")
F4.place(x=320,y=220,width=280,height=380)
def newsa(a):
    try:
        txtarea.config(state=NORMAL)
        nurl='http://newsapi.org/v2/top-headlines?country=in&category='+a+'&apiKey=your-api-key'
        response1 = requests.get(nurl)
        news = response1.json()
        txtarea.delete("1.0", END)
        articles = news['articles']
        if(articles != 0):
            for i in range(len(articles)):
                txtarea.insert(END, f"{articles[i]['title']}\n")
                txtarea.insert(END, "________________________________\n")
        txtarea.config(state=DISABLED)
    except:
        messagebox.showerror('ERROR', "Sorry cant connect to internet :(")
        


def movie(a):
    try:
        txtarea1.config(state=NORMAL)
        murl='https://imdb-api.com/tel/API/'+a+'/api-key'
        response2 = requests.get(murl)
        movies = response2.json()
        txtarea1.delete("1.0", END)
        ms=movies['items']
        if(ms != 0):
            for i in range(len(ms)):
                txtarea1.insert(END, f"{ms[i]['fullTitle']}\n")
                txtarea1.insert(END, "________________________________\n")
        txtarea1.config(state=DISABLED)
    except:
        messagebox.showerror('ERROR', "Sorry cant connect to internet :(")

def mails():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    mails = results.get('messages',[])
    for mail in range(0,20):
        txt = service.users().messages().get(userId='me', id=mails[mail]['id']).execute()
                    # Get value of 'payload' from dictionary 'txt'
        payload = txt['payload']
        headers = payload['headers']
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']
        t1area.insert(INSERT,subject)
        t1area.insert(END, "\nSender: ")
        t1area.insert(INSERT,sender)
        t1area.insert(END, "\n________________________________\n")
    t1area.config(state=DISABLED)

    #news
scroll_y = Scrollbar(F1, orient=VERTICAL)
txtarea = Text(F1, yscrollcommand=scroll_y.set,bg="#D3E0EA",fg="black")

news_title = Label(F1, text="News Area", relief=GROOVE,bg="#1687A7",fg="white").pack(fill=X)
BF1=Frame(F1,bg="#0096C7",height=20)
Button(BF1,text="General",command=lambda: newsa("general")).place(x=0,y=0,height=20,width=60)
Button(BF1,text="Technology",command=lambda:newsa("technology")).place(x=60,y=0,height=20,width=70)
Button(BF1,text="Sports",command=lambda:newsa("sports")).place(x=130,y=0,height=20,width=50)
Button(BF1,text="Entertainment",command=lambda:newsa("entertainment")).place(x=180,y=0,height=20,width=100)

BF1.pack(fill=X)



scroll_y.pack(side=RIGHT, fill=Y)
scroll_y.config(command=txtarea.yview)
txtarea.pack(fill=BOTH, expand=1)













    #movies

scroll_y = Scrollbar(F3, orient=VERTICAL)
txtarea1 = Text(F3, yscrollcommand=scroll_y.set,bg="#D3E0EA",fg="black")

news_title = Label(F3, text="Movies Area", relief=GROOVE,bg="#1687A7",fg="white").pack(fill=X)
BF2=Frame(F3,bg="#0096C7",height=20)
Button(BF2,text="In Theatres",command=lambda: movie("InTheaters")).place(x=0,y=0,height=20,width=90)
Button(BF2,text="Coming Soon",command=lambda:movie("ComingSoon")).place(x=90,y=0,height=20,width=98)
Button(BF2,text="IMDB top 250",command=lambda:movie("Top250Movies")).place(x=188,y=0,height=20,width=92)

BF2.pack(fill=X)



scroll_y.pack(side=RIGHT, fill=Y)
scroll_y.config(command=txtarea1.yview)
txtarea1.pack(fill=BOTH, expand=1)



#mails
mail_title = Label(F4, text="Mails", relief=GROOVE,bg="#1687A7",fg="white").pack(fill=X)
scroll_x = Scrollbar(F4, orient=VERTICAL)
t1area = Text(F4, yscrollcommand=scroll_x.set,height=10,width=28,bg="#D3E0EA",fg="black")
scroll_x.pack(side=RIGHT, fill=Y)
scroll_x.config(command=t1area.yview)
t1area.pack(fill=BOTH, expand=1)
try:
    mails()   
except:
    pass



F2 = Frame(root,bg="#0096C7")
F2.place(x=320, y=20,width=280,height=180)
try:

    surl = "https://ipinfo.io/json?token=api-key"
    response1 = requests.get(surl)
            
    city1 = response1.json()
    n=city1['city']+","+city1['region']

    #n="Vijayawada,AndhraPradesh"
    try:
        wurl = 'https://api.openweathermap.org/data/2.5/weather?q='+n+'&appid=api-key'
        response = requests.get(wurl)
        weather = response.json()
        name1=n
        desc=weather['weather'][0]['description']
    except:
        n="Vijayawada,AndhraPradesh"
        wurl = 'https://api.openweathermap.org/data/2.5/weather?q='+n+'&appid=api-key'
        response = requests.get(wurl)
        weather = response.json()
        name1=n
        desc=weather['weather'][0]['description']
        
    temp=int(weather['main']['temp'])-273
    temp1=str(temp)+"°c"
    l=weather['weather'][0]['icon']
    u="http://openweathermap.org/img/w/"+l+".png"
    res=requests.get(u)
    img_data = res.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))



    Label(F2,text=name1,bg="#0096C7",fg="white",font=("verdana",12),anchor="w").place(x=10,y=20,height=30,width=280)
    Label(F2,text=desc,bg="#0096C7",fg="white",font=("verdana",12),anchor="w").place(x=10,y=50,height=30,width=280)
    panel =Label(F2, image=img,bg="#0096C7")
    panel.place(x=50,y=80,height=80,width=50)
    Label(F2,text=temp1,bg="#0096C7",fg="white",font=("verdana",25),height=50,width=70).place(x=100,y=80,height=80,width=80)
except Exception as e :
    print(e)
    messagebox.showerror('ERROR', "Sorry cant connect to internet :(")
    root.destroy()
   
root.mainloop()

