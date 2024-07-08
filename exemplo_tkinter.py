import tkinter as tk
import customtkinter as ctk

root = ctk.CTk()
root.geometry('400x400')

frame = ctk.CTkScrollableFrame(root,
                               orientation=tk.VERTICAL,
                               fg_color='teal',
                               scrollbar_button_color='orange',
                               scrollbar_button_hover_color='darkorange',
                               corner_radius=10,
                               label_text='Scrolled Data',
                               label_fg_color='#46ADF0'
                               )
frame.pack()

for i in range(50):
    ctk.CTkLabel(
        frame,
        text=f'label nr. {i}',
        text_color='#FF0000',  # Exemplo: Definir cor do texto para vermelho
        font=ctk.CTkFont('Consolas', 14, 'bold')
    ).pack()

root.mainloop()
