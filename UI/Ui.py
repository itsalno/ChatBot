import tkinter as tk
from tkinter import scrolledtext

def send_message():
    message = input_field.get()
    if message.strip():
        chat_display.insert(tk.END, f"You: {message}\n")
        input_field.delete(0, tk.END)

# Initialize main window
root = tk.Tk()
root.title("Chat UI")
root.geometry("400x500")
root.configure(bg="#f5f5f5")

# Subject Entry
subject_label = tk.Label(root, text="Enter Subject:", bg="#f5f5f5")
subject_label.pack(pady=(10, 0))
subject_entry = tk.Entry(root, width=50)
subject_entry.pack(pady=5)

# Chat Display
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, bg="white")
chat_display.pack(pady=10)
chat_display.config(state=tk.NORMAL)

# User Input Field
input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.pack(pady=5)

input_field = tk.Entry(input_frame, width=40)
input_field.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

root.mainloop()
