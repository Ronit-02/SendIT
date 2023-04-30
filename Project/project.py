import tkinter as tk
from tkinter import *
import socket 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
import time
from cryptography.fernet import Fernet
from PIL import ImageTk, Image 
import base64

root = Tk()
root.title('SendIT')
root.geometry("1000x560+300+100")
root.config(bg='#fff')
root.resizable(False,False)

# login function
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "" and password == "":
        # destroy login frame
        login_frame.destroy()
        send_frame.pack(side=LEFT)
        receive_frame.pack(side=RIGHT)
    else:
        error_label.config(text="Invalid username or password")

# login frame
login_frame = tk.Frame(root, width=800, height=1000, bg='#fff')
login_frame.pack()

# Load an image in the script
img= (Image.open("images/login.jpg"))

# Resize the Image using resize method
resized_image= img.resize((450,500))
new_image= ImageTk.PhotoImage(resized_image)

# Add image to the Frame
label = Label(login_frame, image = new_image)
label.place(x=0,  y=30)

# title 
title_label = tk.Label(login_frame, text="Log In", font='arial 20 bold',bg='#fff')
title_label.place(relx=0.8,y=30)

# username
username_label = tk.Label(login_frame, text="Username:",bg='#fff',font='arial 12 bold')
username_label.place(x=550,y=160)
username_entry = tk.Entry(login_frame)
username_entry.place(x=650,y=163)

# password
password_label = tk.Label(login_frame, text="Password:",bg='#fff',font='arial 12 bold')
password_label.place(x=550,y=220)
password_entry = tk.Entry(login_frame, show="*")
password_entry.place(x=650,y=223)

# button
login_button = tk.Button(login_frame, text="Login", height=2, width=10, fg="#fff",bg='#0BA6FF', font=('arial', 12, 'bold'), cursor="hand2", command=login)
login_button.place(relx=0.82,y=350)

# error
error_label = tk.Label(login_frame, fg="red",bg='#fff')
error_label.place(relx=0.7,y=300)

def Send():
    window=Toplevel(send_frame,bg='#fff')
    window.title("SendIT")
    window.geometry("500x560+300+100")
    window.resizable(False,False)

    progress_bar=ttk.Progressbar(window, orient="horizontal", length=200, mode="determinate")
    progress_bar.place(x=160,y=420)

    def select_file():
        global filename
        progress_bar['value']=0
        filetypes=(('All Files','*.*'),('Text','*.txt'),('PDF','*.pdf'),('Word','*.docx'),('Python','*.py'),('C++','*.cpp'),('PNG','*.png'))
        filename=filedialog.askopenfilename(initialdir=os.getcwd(),title='Select Image File',filetypes=filetypes)
        
        if filename:
            os.chmod(filename, 0o444)

        messagebox.showinfo("Alert", "File is locked & is ready to be sent!")
        Label(window, text='Selected File', font=('arial',14), bg='#fff').place(x=80,y=80)
        Label(window, text=f'{filename}', font=('arial',10), bg='#fff').place(x=80,y=120)

    def sender():
        s=socket.socket()
        host=socket.gethostname()
        port=8080
        s.bind((host,port))
        s.listen(5)
        print(host)
        print('Waiting for any incoming connections..........')
        conn,addr=s.accept()
        filesize = os.path.getsize(filename)
        conn.send(f"{filename.split('/')[-1]}|{filesize}".encode())
        progress_bar['value']=0
        
        start_time=time.time()
        sent=0
        with open(filename,'rb') as file:
            while True:
                file_data=file.read(1024)
                if not file_data:
                    break
                sent+=len(file_data)
                progress_bar['value']=sent / filesize * 100
                conn.send(file_data)
                window.update_idletasks()
        end_time=time.time()
        
        Label( window,text=f'Time elapsed (in seconds): {end_time-start_time}',bg='white',fg='black').place(x=190,y=10)
        os.chmod(filename, 0o777)

        messagebox.showinfo("Successfull", f"{filename} has been sent successfully and is now Unlocked")

    host=socket.gethostname()
    
    Label( window, text=f'ID: {host}', bg='white',fg='black', font=('Acumin Variable Concept',12)).place(x=380,y=500)

    Button(window, text="+ Select Files", width=14, height=2, font=('arial', 12),bg='#fff', cursor="hand2", command=select_file).place(x=190,y=200)
    
    Button(window, text="Send", width=10, height=2, font='arial 12 bold',bg='#0BA6FF',fg='#fff', cursor="hand2", command=sender).place(x=200,y=290)

    window.mainloop()

def Receive():
    main=Toplevel(receive_frame,bg='#0BA6FF')
    main.title("SendIT")
    main.geometry("500x560+800+100")
    main.resizable(False,False)

    # Sender Id
    Label(main,text='Sender ID',font=('arial',14,'bold'),bg='#0BA6FF', fg="#fff").place(x=140,y=90)
    senderID=Entry(main,width=25,fg='black',border=2,bg='white',font=('arial',13, 'bold'))
    senderID.place(x=140,y=140)
    senderID.focus()

    # Filename
    Label(main,text='Filename',font=('arial',14,'bold'),bg='#0BA6FF', fg="#fff").place(x=140,y=190)
    incoming_file=Entry(main,width=25,fg='black',border=2,bg='white',font=('arial',13, 'bold'))
    incoming_file.place(x=140,y=240)

    progress_bar=ttk.Progressbar(main, orient="horizontal", length=200, mode="determinate")
    progress_bar.place(x=160,y=420)
     
    def receiver():
        ID=senderID.get()
        filename1=incoming_file.get()

        s=socket.socket()
        port=8080
        s.connect((ID,port))
        progress_bar['value']=0

        data = s.recv(1024).decode()
        filename, filesize = data.split("|")
        filesize = int(filesize)

        Label(main,text=f'Receving file originally named as: {filename}\nFilze Size: {filesize//1024} KB',font=('arial',10,'bold'),bg='#f4fdfe').place(x=20,y=70)

        start_time=time.time()
        received=0
        with open(filename1,'wb') as file:
            while True:
                file_data=s.recv(1024)
                if not file_data:
                    break
                received+=len(file_data)
                progress_bar['value']=received / filesize * 100
                file.write(file_data)
                main.update_idletasks()

        end_time=time.time()
        Label(main,text=f'Time elapsed (in seconds): {end_time-start_time}',bg='white',fg='black').place(x=205,y=10)
        messagebox.showinfo("Successfull", "Data received successfully")

    Button(main,text='Receive',compound=LEFT,width=10,height=2,bg='#fff',fg="#0BA6FF", font='arial 12 bold', cursor="hand2", command=receiver).place(x=200,y=320)

    main.mainloop()

# Send Frame
send_frame = tk.Frame(root, width=500, height=800, padx=15, pady=15, bg="#fff")

Label(send_frame, text='Send File',font=('Acumin Variable Concept',25,'bold'), bg='#fff', fg="#0BA6FF").place(x=180,y=80)

b1 = Button(send_frame, text="Send", bg="#0BA6FF", fg="#fff" , height=2, width=10, font=('arial', 12, 'bold'), cursor="hand2", command=Send)
b1.place(x=200, y=250)

# Receive Frame
receive_frame = tk.Frame(root, width=500, height=1000, padx=15, pady=15, bg="#0BA6FF")

Label(receive_frame, text='Receive File',font=('Acumin Variable Concept',25,'bold'), bg='#0BA6FF', fg="#fff").place(x=150,y=80)

b2 = Button(receive_frame, text="Receive", bg="#fff", fg="#0BA6FF", height=2, width=10, font=('arial', 12, 'bold'), cursor="hand2" , command=Receive)
b2.place(x=200, y=250)

root.mainloop()