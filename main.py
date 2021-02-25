import tkinter
import requests
from bs4 import BeautifulSoup

class yt_dowloader():
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x500+500+500")
        row = 0
        col = 0
        tkinter.Label(self.root, text="Youtube Downloader").grid(row=row, column=col)
        row += 1

        tkinter.Label(self.root, text="Link").grid(row=row, column=col)
        col += 1
        self.input_field = tkinter.Entry(self.root)
        self.input_field.grid(row=row, column=col)
        col += 1

        dload_btn = tkinter.Button(self.root, text="download", command=self.download_btn_click)
        dload_btn.grid(row=row, column=col)
        dload_btn

        row += 1
        col = 0

    def download_btn_click(self):
        # https://www.youtube.com/watch?v=-FjW5E0U8gY&t=459s
        soup = ""
        try:
            url = self.input_field.get()
            page = requests.get(url).text
            soup = BeautifulSoup(page, "html.parser")

        except :
            print("error")

        print(soup)
        pass







if __name__ == "__main__":
    root = tkinter.Tk()
    obj = yt_dowloader(root)

    root.mainloop()