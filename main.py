import customtkinter as ctk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
import fitz
import pyttsx3
import pygame
import os


ctk.set_appearance_mode("light")


text = ""
file_path = ""
pdf_name = None
window = ctk.CTk()
window.geometry("300x300")
window.title("PDF Audio")

window.grid_rowconfigure((0, 1, 2), weight=1)
window.grid_columnconfigure((0, 1, 2), weight=1)


def get_text():
    global text, file_path, pdf_name
    text = ""

    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select file",
        filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")),
    )

    if not file_path.endswith(".pdf"):
        CTkMessagebox(
            title="Error", message="File must be a PDF.", icon="warning", option_1="Ok"
        )
        return

    if file_path:

        pdf_name = os.path.basename(file_path).split(".")[0].replace(" ", "")
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()

        if text.strip():
            engine = pyttsx3.init()
            engine.save_to_file(text, f"{pdf_name}.wav")
            engine.runAndWait()

        else:
            CTkMessagebox(
                title="Error",
                message="No readable text found in PDF.",
                icon="warning",
                option_1="Ok",
            )

    except Exception as e:
        CTkMessagebox(title="Error", message=str(e), icon="warning", option_1="Ok")


def play_audio():
    global pdf_name
    if os.path.exists(f"{pdf_name}.wav"):
        pygame.mixer.init()
        pygame.mixer.music.load(f"{pdf_name}.wav")
        pygame.mixer.music.play()

    else:
        CTkMessagebox(
            title="Error",
            message="Audio file not found.",
            icon="warning",
            option_1="Ok",
        )


upload_pdf = ctk.CTkButton(window, text="Upload PDF", command=get_text)
upload_pdf.grid(row=1, column=0, padx=20, pady=10)

play_audio_button = ctk.CTkButton(window, text="Play Audio", command=play_audio)
play_audio_button.grid(row=1, column=1, padx=20, pady=10)


window.mainloop()
