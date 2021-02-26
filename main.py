import os
import ssl
import pytube
import requests
import io
import tkinter
from tkinter import ttk
from PIL import Image,ImageTk

class yt_dowloader():
    def __init__(self, root : tkinter.Tk):
        self.root = root
        self.root.title("Youtube Downloader | By Michael Moore")
        self.root.geometry("520x450+300+300")
        self.root.resizable(False,False)
        self.root.config(bg="white")
        title = tkinter.Label(self.root, text="Youtube Downloader | By Michael Moore",font=('times new roman', 13),bg='#324232',fg='white').pack(side=tkinter.TOP,fill=tkinter.X)

        self.var_url=tkinter.StringVar()
        lab_url = tkinter.Label(self.root, text="Link", font=('times new roman', 13, 'bold'),bg="white",fg="red").place(x=10, y=50)
        entry_url = tkinter.Entry(self.root, font=('times new roman', 11),textvariable=self.var_url,bg="lightyellow",fg="red").place(x=120, y=50, width=320)

        lab_file_type = tkinter.Label(self.root, text="File Type", font=('times new roman', 13, 'bold'),bg="white",fg="red").place(x=10, y=90)

        self.var_fileType = tkinter.StringVar()
        self.var_fileType.set('Video')
        video_radio = tkinter.Radiobutton(self.root, text="Video", variable=self.var_fileType, value='Video',  font=('times new roman', 11, 'bold'),bg="white",fg="red", activebackground='black',activeforeground='black').place(x=120, y=90)
        audio_radio = tkinter.Radiobutton(self.root, text="Audio", variable=self.var_fileType, value='Audio', font=('times new roman', 11, 'bold'),bg="white",fg="red", activebackground='black',activeforeground='black').place(x=200, y=90)


        search_btn = tkinter.Button(self.root, text="Search",font=('times new roman', 15),command=self.search,bg='blue',fg='black').place(x=280, y=90,height=25,width=150)

        frame1 = tkinter.Frame(self.root, bd=2, relief=tkinter.RIDGE, bg='lightyellow')
        frame1.place(x=10,y=130,width=490, height=180)

        self.video_title = tkinter.Label(frame1, text="video Title here",font=('times new roman', 13),bg='lightgray',fg='white', anchor='w')
        self.video_title.place(x=0,y=0, relwidth=1)

        self.video_image = tkinter.Label(frame1, text="Video \nImage", font=('times new roman', 13), bg='lightgray', fg='white')
        self.video_image.place(x=5, y=30, width=180, height=140)


        label_video_description = tkinter.Label(frame1, text="Description", font=('times new roman', 13), bg='lightyellow').place(x=190, y=30)

        self.video_desc = tkinter.Text(frame1, font=('times new roman', 11), bg='lightgray')
        self.video_desc.place(x=190, y=60, width=295, height=110)

        self.label_video_size = tkinter.Label(self.root, text="Total Size: ", font=('times new roman', 13), bg='white')
        self.label_video_size.place(x=10, y=320)

        self.label_percentage = tkinter.Label(self.root, text="Downloading: %", font=('times new roman', 13), bg='white')
        self.label_percentage.place(x=130, y=320)

        clear_btn = tkinter.Button(self.root, text="Clear",font=('times new roman', 15),bg='blue',fg='black', command=self.clear).place(x=330, y=320,height=25,width=70)
        self.download_btn = tkinter.Button(self.root, text="Download",font=('times new roman', 15),state=tkinter.DISABLED,bg='green',highlightbackground='green',fg='white', command=self.download)
        self.download_btn.place(x=415, y=320,height=25,width=90)

        self.prog = ttk.Progressbar(self.root, orient=tkinter.HORIZONTAL,length=590, mode='determinate')
        self.prog.place(x=10,y=360,width=485,height=25)

        self.label_message = tkinter.Label(self.root, text="Error Messages", font=('times new roman', 13), bg='white')
        self.label_message.place(x=0, y=400, relwidth=1)

        #=======Making directory for files
        if os.path.exists('Audios') == False:
            os.mkdir('Audios')
        if not os.path.exists('Videos'):
            os.mkdir('Videos')



    def search(self):
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        if self.var_url.get() == '':
            self.label_message.config(text='Video URL is required', fg='red')
        else:
            yt = pytube.YouTube(self.var_url.get())

            #===convert image url to image
            response = requests.get(yt.thumbnail_url)
            img_byte = io.BytesIO(response.content)
            self.img = Image.open(img_byte)
            self.img = self.img.resize((180,140), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            self.video_image.config(image=self.img)

            #===fetch the sixe as per type
            if self.var_fileType.get() == 'Audio':
                select_file = audio_file = yt.streams.filter(only_audio=True).first()
            if self.var_fileType.get() == "Video":
                select_file = yt.streams.filter(progressive=True).first()

            self.size_inByte = select_file.filesize
            max_size = self.size_inByte / 1024000
            self.mb = str(round(max_size, 2)) + 'MB'
            self.label_video_size.config(text=f'Total Size: {self.mb}')
            #===updating the frame elements
            self.video_title.config(text=yt.title)
            self.video_desc.delete('1.0',tkinter.END)
            self.video_desc.insert(tkinter.END,yt.description[:200])
            self.download_btn.config(state=tkinter.NORMAL)


    def progress_(self,streams,chunk,bytes_remaining):
        percent= (float(abs(bytes_remaining-self.size_inByte)/self.size_inByte))*float(100)
        self.prog['value'] = percent
        self.prog.update()
        self.label_percentage.config(text=f'Downloading: {str(round(percent,2))}%')
        if round(percent,2) == 100:
            self.label_message.config(text='Download Complete', fg='green')

    def download(self):
        # https://www.youtube.com/watch?v=-FjW5E0U8gY&t=459s
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        yt = pytube.YouTube(self.var_url.get(),on_progress_callback=self.progress_)

        # ===convert image url to image
        if self.var_fileType.get() == 'Video':
            select_file = yt.streams.filter(progressive=True).first()
            select_file.download('Videos/')
        if self.var_fileType.get() == 'Audio':
            select_file = yt.streams.filter(only_audio=True).first()
            select_file.download('Audios/')

        response = requests.get(yt.thumbnail_url)
        img_byte = io.BytesIO(response.content)
        self.img = Image.open(img_byte)
        self.img = self.img.resize((180, 140), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.video_image.config(image=self.img)

    def clear(self):
        self.var_fileType.set('Video')
        self.var_url.set('')
        self.prog['value'] - 0
        self.download_btn.config(stat=tkinter.DISABLED)
        self.label_message.config(text='')
        self.video_title.config(text='Video Title Here')
        self.video_image.config(image='')
        self.video_desc.delete('1.0',tkinter.END)
        self.label_video_size.config(text='Total Size: MB')
        self.label_percentage.config(text='Downloading 0%')









if __name__ == "__main__":
    root = tkinter.Tk()
    obj = yt_dowloader(root)

    root.mainloop()