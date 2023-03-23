import tkinter as tk
from tkinter import ttk

def on_configure(event, root):
    # Get the size of the window
    width = event.width
    height = event.height

    # Get a list of all the buttons in the window
    buttons = [widget for widget in root.winfo_children() if isinstance(widget, ttk.Button)]

    # Calculate the new size and position of each button
    for i, button in enumerate(buttons):
        button_width = int(width * 0.2)
        button_height = int(height * 0.1)
        button_x = int(width * 0.4)
        button_y = int(height * (0.3 + i * 0.2))

        # Update the size and position of the button
        button.place(width=button_width, height=button_height, x=button_x, y=button_y)

def main():
    root = tk.Tk()

    # Create some buttons
    for i in range(5):
        button = ttk.Button(root, text=f"Button {i+1}")
        button.pack()

    # Bind the <Configure> event to the root window
    root.bind("<Configure>", lambda event: on_configure(event, root))

    root.mainloop()

if __name__ == "__main__":
    main()