import customtkinter as ctk
import tkinter.messagebox as tkmb
from tkinterdnd2 import TkinterDnD, DND_FILES
import pandas as pd
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Ensure customtkinter is correctly initialized
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.title("Modern Login UI using Customtkinter")
        self.frame = FirstFrame(self)
        self.frame.pack()

    def change(self, frame):
        self.frame.pack_forget()  # delete current frame
        self.frame = frame(self)
        self.frame.pack()  # make new frame

class FirstFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        master.geometry("600x600")
        master.title("Enter credentials")

        self.status = ctk.CTkLabel(self, text="", text_color='red')
        self.status.pack(pady=10)

        lbl = ctk.CTkLabel(self, text="Enter your credentials")
        lbl.pack(pady=10)

        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.user_entry.pack(pady=10)
        self.user_entry.focus()

        self.pwd_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.pwd_entry.pack(pady=10)
        self.pwd_entry.bind('<Return>', self.check)

        btn_done = ctk.CTkButton(self, text="Done", command=self.check)
        btn_done.pack(pady=5)

        btn_cancel = ctk.CTkButton(self, text="Cancel", command=master.quit)
        btn_cancel.pack(pady=5)

    def check(self, event=None):
        username = "Umit"
        password = "12345"
        if self.user_entry.get() == username and self.pwd_entry.get() == password:
            tkmb.showinfo(title="Login Successful", message="You have logged in Successfully")
            self.master.change(SecondFrame)  # correct credentials, switch to the second frame
        elif self.user_entry.get() == username and self.pwd_entry.get() != password:
            self.status.configure(text="Wrong password")
        elif self.user_entry.get() != username and self.pwd_entry.get() == password:
            self.status.configure(text="Wrong username")
        else:
            self.status.configure(text="Invalid Username and password")

class SecondFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.label = ctk.CTkLabel(self, text="Drag and drop a CSV file here", width=40, height=10, fg_color=("white", "gray75"))
        self.label.pack(pady=20, padx=100, expand=True)

        # Frame for plotting
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.pack(pady=20, padx=100, fill='both', expand=True)

        # Ensure the correct registration and binding
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.drop)

        # Plot button
        self.plot_button = ctk.CTkButton(self, text="Plot", command=self.plot_data)
        self.plot_button.pack(pady=20)

        self.df = None  # Initialize dataframe variable

    def drop(self, event):
        file_path = event.data.strip('{}')
        if os.path.isfile(file_path) and file_path.endswith('.csv'):
            self.process_csv(file_path)
        else:
            self.label.configure(text="Please drop a valid CSV file")

    def process_csv(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            self.label.configure(text=f"File {file_path} successfully loaded!\nNumber of rows: {len(self.df)}")
        except Exception as e:
            self.label.configure(text="Failed to read the CSV file")
            print(e)

    def plot_data(self):
        if self.df is not None:
            # Clear the previous plot if any
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            fig, ax = plt.subplots()
            ax.plot(pd.to_datetime(self.df.iloc[:, 0]), self.df.iloc[:, 1])
            ax.set_xlabel('Timestamp')
            ax.set_ylabel('Data')
            ax.set_title('CSV Data Plot')

            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
        else:
            tkmb.showwarning("Warning", "No CSV file loaded. Please drop a CSV file first.")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
