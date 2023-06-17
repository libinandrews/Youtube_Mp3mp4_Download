from datetime import datetime
import json
import logging
import os
import tkinter as tk
from tkinter import (
    Button,
    DISABLED,
    END,
    Entry,
    IntVar,
    Label,
    Listbox,
    NORMAL,
    Radiobutton,
    StringVar,
    Tk,
    messagebox,
    ttk,
    filedialog,
)
import numpy as np
import pandas as pd
import pyperclip
import pytube
from pytube import Playlist, YouTube
import pandasgui
from moviepy.editor import *
import socket
import random
import time
import requests


class YoutubeDownloader:
    def __init__(self, root):
        self.root = root
        self.settings = {}
      #  self.root.geometry("1100x900")
        self.root.title("Youtube Downloader")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_settings()
        self.dropdown_values = []
                
        logo = os.path.join(self.current_dir, "resources", "Images", "YouTubeicon.png")
        icon = tk.PhotoImage(file=logo)
        self.root.iconphoto(False, icon)
                # Get the width and height of the window
        self.width = 1100
        self.height = 650

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates for centering the window
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        # Set the window geometry
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
    def load_settings(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(self.current_dir, "resources", "settings.json")
        try:
            with open(settings_file, "r") as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = {"path": "C:\\Downloads"}
    def download_video(self):
        # Implement the video download functionality
        pass
    def on_closing(self):
        # Implement any cleanup tasks before closing the application
        self.save_settings()
        if messagebox.askyesno("Confirm", "Are you sure you want to quit?"):
            self.root.destroy()
    def save_settings(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(self.current_dir, "resources", "settings.json")
        try:
            with open(settings_file, "w") as file:
                json.dump(self.settings, file, indent=4)
        except:
            logging.warning("Failed to save settings file.")
    def file_explorer(self):
    # Display the directory selection dialog box
        folder_path = filedialog.askdirectory(initialdir="C:/Downloads")
        if folder_path: 
            self.folder_path = folder_path
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, self.folder_path)
            root.update_idletasks()
        else:
            self.folder_path = r"C:\Downloads"
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, self.folder_path)
    def excel_explorer(self):
    # Display the Excel file selection dialog box
        file_path = filedialog.askopenfilename(initialdir=self.current_dir, filetypes=[("Excel Files", "*.xlsx; *.xls")])
        if file_path:
            df = pd.read_excel(file_path)
            required_columns = ['FileType', 'url']
            status = all(column in df.columns for column in required_columns)
            if status :
                self.df = df
                self.savedata()
            else :
                print("please provide 'FileType', 'url' as heading")

        else:
            print("Excel file not found")
    def update_entry_data(self, event):
        self.folder_content.set(self.folder_entry.get())
        root.update_idletasks()
    def mp3_button_click(self):
        self.next_button.config(state=NORMAL)

    def video_button_click(self):
        self.next_button.config(state=NORMAL)
    def paste_from_clipboard(self):
       # pyperclip.copy('https://youtube.com/playlist?list=PLzMcBGfZo4-lOXGKoV-sIPKD7MOuHp3_Q')
        clipboard_text = pyperclip.paste()
        self.youtubelink.set(clipboard_text)
        self.get_video_info()
        self.Loadplaylists()
        root.update_idletasks()
    def choosefiles(self):
           new_window = tk.Toplevel(root)
           new_window.title("Select fIles")

    def get_video_info(self):
        playlist_url =  self.youtubelink.get()
        if playlist_url:
            try:
                playlist = Playlist(playlist_url)
                df = pd.DataFrame(columns=['Title', 'url'])
                for video in playlist.videos:
                    print(video.title)
                    df = df.append({'Title': video.title, 'url': video.watch_url}, ignore_index=True)
            except:
                try:
                    video = YouTube(playlist_url)
                    df = pd.DataFrame(columns=['Title', 'url'])
                    df = df.append({'Title': video.title, 'url': video.watch_url}, ignore_index=True)
                except:
                    df = pd.DataFrame(columns=['Title', 'url'])
                    df = df.append({'Title': 'Error to load link', 'url': playlist_url}, ignore_index=True)
            return df 
    def Loadplaylists(self):
        playlist_url =  self.youtubelink.get()
        if playlist_url :
            self.df = self.get_video_info()
            if self.radio_var.get() == 1 :
                self.df['FileType'] = "mp3"
            elif self.radio_var.get() == 2 :
                self.df['FileType'] = "mp4"
            else :
                self.df['FileType'] = "error"
           # pandasgui.show(self.df)
            List = list(self.df['Title'])
            self.dropdown_values = List
            self.dropdown['values'] = self.dropdown_values
            self.dropdown_var.set(self.dropdown_values[0])  # Set the first value as the default
            root.update_idletasks()
        else :
            print("Please Enter Playlist URL")    
            
    def delete_dropdown_item(self):
        df = self.df
        selected_item = self.dropdown_var.get()
        if selected_item:
            self.dropdown_values.remove(selected_item)
            self.dropdown["values"] = self.dropdown_values
            print(f"Deleted from dropdown: {selected_item}")
            self.df = df[df['Title'].isin(self.dropdown_values)]
    def savedata(self):
        newdf = self.df
        newdf['date'] = datetime.now()
        try :
            load_df = pd.read_json('data.json')
        except :
            load_df = newdf
        newdf = newdf.append(load_df, ignore_index=True)
        newdf.drop_duplicates(subset=['Title', 'url', 'FileType'], inplace=True)
        newdf.to_json('data.json')
        file_path = os.path.join(self.current_dir, 'youtubedata.xlsx')
        self.df = newdf
        try :
           self.df.to_excel(file_path, index=False)
        except :
            print("error to save as excel file")
        #pandasgui.show(self.df)
    def loaddata(self):
        try :
            self.df = pd.read_json('data.json') 
        except :
            print("File Not availabe")
       # pandasgui.show(self.df)
    def openinexcel(self):
        df = self.df
        new = ['date', 'Title', 'FileType', 'url']
        df = df.reindex(columns=new)
        file_path = os.path.join(self.current_dir, 'youtubedata.xlsx')
        df.to_excel(file_path, index=False)
        os.startfile(file_path)
    def update(self):
        self.df.to_json('data.json')
        try :
            file_path = os.path.join(self.current_dir, 'youtubedata.xlsx')
            self.df.to_excel(file_path, index=False)
        except : 
            print("Excel Error availabe")

    def check_networks(self):
        websites = [
            "https://www.google.com",
            "https://www.wikipedia.org",
            "https://www.amazon.com",
            "https://www.youtube.com",
            "https://www.reddit.com",
            "https://www.netflix.com",
            "https://www.nytimes.com",
            "https://www.github.com",
            "https://www.stackoverflow.com",
            "https://www.medium.com"
        ]
        while True:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%d %B %Y %I:%M %p")
            try:
                web = random.choice(websites)
                requests.get(web)
                network_available = True
                print(f"Current time: {formatted_time}, network status is {network_available}")
                return True
                break 
            except OSError:
                network_available = False
            if not network_available:
                print(f"Current time: {formatted_time}, network status is {network_available}")
                time.sleep(50)   
    def cleardata(self):
        os.remove('data.json')
        self.df = pd.DataFrame()   
         
    def download(self):
        def download_audio_from_youtube(url, output_folder):
            if self.check_networks():
                # Create a YouTube object and get the audio stream with the highest bitrate
                yt = YouTube(url)
                audio_streams = yt.streams.filter(only_audio=True)
                audio_stream = audio_streams.get_audio_only(subtype='mp4')
                highest_bitrate_audio = audio_streams.order_by('abr').desc().first()
            try:
                # Download the audio to a specific folder
                downloaded_file = audio_stream.download(output_path=output_folder)
                mp3_file = downloaded_file.replace('.mp4', '.mp3')
                
                try:
                    audio_clip = AudioFileClip(downloaded_file)
                    audio_clip.write_audiofile(mp3_file)
                    audio_clip.close()
                except Exception as e:
                    print("Conversion error:", str(e))
                # Remove the downloaded MP4 file
                os.remove(downloaded_file)

                return mp3_file

            except Exception as e:
                print("An error occurred:", str(e))      
        def download_video_from_youtube(url, output_folder): 
            if self.check_networks(): 
                try: 
                    yt = YouTube(url)
                    stream = yt.streams.get_highest_resolution()
                    downloaded_file = stream.download(output_path=output_folder)
                    if downloaded_file  is not None:
                         return downloaded_file
                    else:
                        print("Download error")
                except :
                    print("An error occurred to download video")   
       
        if isinstance(self.folder_path, str):
            output_folder = self.folder_path
        else :
            self.load_settings()
            output_folder = self.settings["path"]
        print(output_folder)
        df = self.df
        df = df.sort_values(by='FileType', ascending=True).reset_index(drop=True)
       # pandasgui.show(df)
        numb = 0
        total_iterations = len(df)
        self.progressbar["maximum"] = total_iterations * 10
        for index, key in df.iterrows():
            print(key["Title"])
            numb += 1
            self.progressbar["value"] = numb * 10
            url = key['url']
            root.update_idletasks()
            if key['FileType'] == 'mp3':
                print('--------------------------------')
                print( key['FileType'],key['url'])
                mp3_file_path = download_audio_from_youtube(url, output_folder)
                try :
                    if os.path.isfile(mp3_file_path) :
                        df = df.drop(index=index)
                        self.df = df
                        self.update()
                        print("Audio downloaded successfully:", mp3_file_path)
                except :
                    print("Audio download failed",key['Title'])
            elif key['FileType'] == 'mp4':
                print('--------------------------------')
                print( key['FileType'],key['url'])
                mp4_file_path = download_video_from_youtube(url, output_folder)
                try :
                    if os.path.isfile(mp4_file_path) :
                        df = df.drop(index=index)
                        self.df = df
                        self.update()
                        print("Audio downloaded successfully:", mp4_file_path)
                except :
                    print("Audio download failed",key['Title'])


            
        
    def GUI(self):
    # Label Frame
        #Creation of the Frame
        savefolder_frame = tk.LabelFrame(self.root, text="Save Folder", font=("Calibri", 12), foreground="gray")
        youtube_frame = tk.LabelFrame(self.root, text="youtube Data", font=("Calibri", 12), foreground="gray")
        download_frame = tk.LabelFrame(self.root, text="Download", font=("Calibri", 12), foreground="gray")
        disclaimer_frame = tk.LabelFrame(self.root, text="Disclaimer", font=("Calibri", 7), foreground="gray")
        
        # Allignment of Lable Frame 
        savefolder_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        youtube_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        download_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")       
        disclaimer_frame.grid(row=3, column=0, padx=10, pady=10, sticky="N")       
# TODO Label Frame Data ------------Save Folder ------------------------
        # Button to Choose the Destination Folder
        folder_button = tk.Button(savefolder_frame, text="Choose Destination Folder", command=self.file_explorer)
        # Add the button to the frame using grid()
        folder_button.grid(row=0, column=0,padx=10, pady=10, sticky="nsew")
        
        self.folder_path = StringVar(value= self.settings["path"])
        self.folder_entry = Entry(savefolder_frame, textvariable=self.folder_path, width=148)
        self.folder_entry.grid(row=0, column=1, padx=0, pady=10, sticky="w")
        self.folder_entry.bind('<KeyRelease>', self.update_entry_data)

        self.folder_content = StringVar()  # Create a new StringVar for displaying the content
        self.folder_content.set(self.folder_path.get())  # Set initial value
        chosen_folder_label = Label(savefolder_frame, text="Chosen Folder:", font=("CALIBRI", 10))
        chosen_folder_label.grid(row=1, column=0, padx=10, pady=0, sticky="w")
        self.folder_choosed = Label(savefolder_frame, textvariable=self.folder_content, font=("CALIBRI", 10))
        self.folder_choosed.grid(row=2, column=0, columnspan=2, padx=10, pady=0, sticky="w")
# Label 2 Youtube Data


        label1 = tk.Label(youtube_frame, text="Enter Youtube Link")
        label1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.youtubelink = StringVar()
        self.youtubelink_entry = Entry(youtube_frame, textvariable=self.youtubelink, width= 148)
        self.youtubelink_entry.grid(row=0, column=1, padx=0, pady=10, sticky="w")
        self.youtubelink_entry.bind('<KeyRelease>', self.update_entry_data)
        btn_paste = tk.Button(youtube_frame, text="Paste", command=lambda: self.paste_from_clipboard())
        btn_paste.grid(row=0, column=2, padx=10, pady=10,sticky="W")
     
        

        self.radio_var = IntVar(value=2)

        self.mp3_radio = Radiobutton(youtube_frame, text="Only MP3", variable=self.radio_var, value=1, command=self.mp3_button_click)
        self.mp3_radio.grid(row=6, column=0, padx=10, pady=10)
        self.video_radio = Radiobutton(youtube_frame, text="Only Video", variable=self.radio_var, value=2, command=self.video_button_click)
        self.video_radio.grid(row=6, column=1, padx=10, pady=10)
        self.next_button = Button(youtube_frame, text="Next", state=DISABLED,command= self.Loadplaylists)
        self.next_button.grid(row=7, column=0, padx=10, pady=10)


        self.dropdown_var = StringVar()
        self.dropdown = ttk.Combobox(youtube_frame, textvariable=self.dropdown_var, values=self.dropdown_values,width =125)
        self.dropdown.grid(row=8, column=0,columnspan=2, padx=10, pady=10,sticky='w')
        self.delete_dropdown_button = Button(youtube_frame, text="Delete Dropdown Item", command=self.delete_dropdown_item)
        self.delete_dropdown_button.grid(row=8, column=1, padx=10, pady=10,sticky="E")
     
        self.savebttm = Button(youtube_frame, text="Save Data", command=self.savedata)
        self.savebttm.grid(row=9, column=0, padx=10, pady=10,sticky="E")
            
# Label Frame 3 Download 
        self.loadbttn = Button(download_frame, text="Load Data for Download", command=self.loaddata)
        self.loadbttn.grid(row=0, column=0, padx=10, pady=10,sticky="E")
        self.excelbtn = Button(download_frame, text="Open in Excel", command=self.openinexcel)
        self.excelbtn.grid(row=0, column=1, padx=10, pady=10,sticky="E")
        self.editexcelbtn = Button(download_frame, text="Load from Excel", command=self.excel_explorer)
        self.editexcelbtn.grid(row=0, column=2, padx=10, pady=10,sticky="E")
        self.cleardatabtn = Button(download_frame, text="clear data", command=self.cleardata)
        self.cleardatabtn.grid(row=0, column=3, padx=10, pady=10,sticky="E")


        self.Downlaodbtn = Button(download_frame, text="Download", command=self.download)
        self.Downlaodbtn.grid(row=1, column=0,columnspan=3, padx=10, pady=10,sticky="nsew")
        self.progressbar = ttk.Progressbar(download_frame, orient='horizontal', mode='determinate',length=1000)
        self.progressbar.grid(column=0, row=4, columnspan=3, padx=0, pady=0,sticky="nsew")


# Label 3 Frame Data -----------disclaimer_frame ------------------------
 
        # Add widgets or content to the LabelFrame
        self.label_text = "It is illegal to download YouTube videos without obtaining consent from YouTube or the person who owns the copyright to the content. Downloading copyrighted content without permission is a violation of copyright law and can be very dangerous. The following are some of the illegal circumstances of downloading YouTube videos"
        label = tk.Label(disclaimer_frame, text=self.label_text, wraplength=self.width-25, fg="gray", font=("Calibri", 7))
        label.grid(row=0, column=0, padx=10, pady=10, sticky="N")

if __name__ == "__main__":
    root = Tk()
    app = YoutubeDownloader(root)
    app.GUI()
    root.mainloop()

