import tkinter as tk
from tkinter import messagebox
import os
import shutil
import subprocess

# =========================================
# Z4OS EXTENSION MANAGER
# =========================================

root = tk.Tk()
root.title("Z4OS Extension Manager")
root.geometry("700x450")
root.configure(bg="black")

# =========================================
# PATH
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APP_FOLDER = BASE_DIR



# =========================================
# OFFICIAL EXTENSIONS
# =========================================
if not os.path.exists(APP_FOLDER):

    messagebox.showerror(
        "Error",
        f"Program folder not found:\n{APP_FOLDER}"
    )

    root.destroy()
official_extensions = {
    "capp": "https://github.com/Z4RN-cmd/capp",
    "document-editor": "https://github.com/Z4RN-cmd/document-editor",
}

# =========================================
# INSTALL EXTENSION
# =========================================

def install_extension(name, repo):

    temp_folder = "temp_repo"

    try:

        status_label.config(text=f"Installing {name}...")

        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)

        subprocess.run(
            ["git", "clone", repo, temp_folder],
            check=True
        )

        for item in os.listdir(temp_folder):

            s = os.path.join(temp_folder, item)
            d = os.path.join(APP_FOLDER, item)

            if os.path.exists(d):

                if os.path.isdir(d):
                    shutil.rmtree(d)
                else:
                    os.remove(d)

            shutil.move(s, d)

        shutil.rmtree(temp_folder)

        status_label.config(text=f"{name} installed successfully.")
        refresh_installed()

    except Exception as e:

        status_label.config(text="Install failed.")
        messagebox.showerror("Error", str(e))


# =========================================
# UNINSTALL EXTENSION
# =========================================

def uninstall_extension(file_name):

    path = os.path.join(APP_FOLDER, file_name)

    confirm = messagebox.askyesno(
        "Confirm",
        f"Delete {file_name}?"
    )

    if not confirm:
        return

    try:

        os.remove(path)

        status_label.config(
            text=f"{file_name} removed."
        )

        refresh_installed()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# =========================================
# REFRESH INSTALLED APPS
# =========================================

def refresh_installed():

    installed_list.delete(0, tk.END)

    for file in os.listdir(APP_FOLDER):

        if file.endswith(".py"):

            installed_list.insert(
                tk.END,
                file
            )


# =========================================
# INSTALL BUTTON
# =========================================

def install_selected():

    selected = official_list.curselection()

    if not selected:
        return

    name = official_list.get(selected[0])

    repo = official_extensions[name]

    install_extension(name, repo)


# =========================================
# REMOVE BUTTON
# =========================================

def remove_selected():

    selected = installed_list.curselection()

    if not selected:
        return

    file_name = installed_list.get(selected[0])

    uninstall_extension(file_name)


# =========================================
# TITLE
# =========================================

title = tk.Label(
    root,
    text="Z4OS Extension Manager",
    font=("Arial", 20, "bold"),
    bg="black",
    fg="white"
)
title.pack(pady=10)

# =========================================
# MAIN FRAME
# =========================================

main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill="both", expand=True)

# =========================================
# LEFT SIDE
# =========================================

left_frame = tk.Frame(main_frame, bg="black")
left_frame.pack(side="left", fill="both", expand=True, padx=10)

tk.Label(
    left_frame,
    text="Official Extensions",
    font=("Arial", 14, "bold"),
    bg="black",
    fg="white"
).pack()

official_list = tk.Listbox(
    left_frame,
    font=("Arial", 12),
    height=15,
    bg="#1e1e1e",
    fg="white",
    selectbackground="#333333"
)
official_list.pack(fill="both", expand=True)

for ext in official_extensions:
    official_list.insert(tk.END, ext)

tk.Button(
    left_frame,
    text="Install",
    font=("Arial", 12),
    command=install_selected,
    bg="#1e1e1e",
    fg="white"
).pack(fill="x", pady=5)

# =========================================
# RIGHT SIDE
# =========================================

right_frame = tk.Frame(main_frame, bg="black")
right_frame.pack(side="right", fill="both", expand=True, padx=10)

tk.Label(
    right_frame,
    text="Installed Extensions",
    font=("Arial", 14, "bold"),
    bg="black",
    fg="white"
).pack()

installed_list = tk.Listbox(
    right_frame,
    font=("Arial", 12),
    height=15,
    bg="#1e1e1e",
    fg="white",
    selectbackground="#333333"
)
installed_list.pack(fill="both", expand=True)

tk.Button(
    right_frame,
    text="Uninstall",
    font=("Arial", 12),
    command=remove_selected,
    bg="#1e1e1e",
    fg="white"
).pack(fill="x", pady=5)

# =========================================
# STATUS
# =========================================

status_label = tk.Label(
    root,
    text="Ready.",
    bg="black",
    fg="white",
    font=("Arial", 10)
)
status_label.pack(pady=5)

refresh_installed()

root.mainloop()