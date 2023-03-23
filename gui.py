import logging
import os
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

from utilities import expand_path, shorten_path
from processing import process_directory, remove_empty_directories, load_config, save_config


class PathVariables:
    def __init__(self, base_path, albums_path, miscellaneous_path):
        self.base_path_var = tk.StringVar(value=shorten_path(base_path))
        self.albums_path_var = tk.StringVar(value=shorten_path(albums_path))
        self.miscellaneous_path_var = tk.StringVar(value=shorten_path(miscellaneous_path))


def browse_directory(directory_var):
    initial_dir = expand_path(directory_var.get())
    if not os.path.isdir(initial_dir):
        initial_dir = os.path.expanduser("~")
    dir_path = filedialog.askdirectory(initialdir=initial_dir)
    if dir_path:
        directory_var.set(shorten_path(dir_path))


def update_progress(root, status_label, status_message=None):
    if status_message is not None:
        status_label.config(text=status_message)
    root.update_idletasks()


def process_and_clean_directories(base_path, albums_path, miscellaneous_path):
    process_directory(base_path, albums_path, miscellaneous_path)
    remove_empty_directories(base_path)


def start_processing(root, path_vars, status_label):
    base_path = expand_path(path_vars.base_path_var.get())
    albums_path = expand_path(path_vars.albums_path_var.get())
    miscellaneous_path = expand_path(path_vars.miscellaneous_path_var.get())

    if os.path.isdir(base_path):
        update_progress(root, status_label, "Processing...")

        # Use a separate thread for processing files
        processing_thread = threading.Thread(target=process_and_clean_directories, args=(base_path, albums_path, miscellaneous_path))
        processing_thread.start()
        root.after(100, check_thread_status, root, processing_thread, path_vars, status_label)

        # Save the paths to the configuration file
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        config = load_config(config_path)
        config['Paths']['BasePath'] = base_path
        config['Paths']['AlbumsPath'] = albums_path
        config['Paths']['MiscellaneousPath'] = miscellaneous_path
        save_config(config, config_path)

        update_progress(root, status_label, "Complete.")
    else:
        logging.error(f"The base path '{base_path}' is not a directory.")
        update_progress("Error: Invalid base path")


def check_thread_status(root, thread, path_vars, status_label):
    if thread.is_alive():
        root.after(100, check_thread_status, root, thread, path_vars, status_label)
    else:
        remove_empty_directories(expand_path(path_vars.base_path_var.get()))
        update_progress(root, status_label, "Complete.")


def create_root_window():
    root = tk.Tk()
    root.title("Music Organizer")
    root.configure(padx=20, pady=20)
    
    # Load the paths from the configuration file
    config = load_config('config.ini')
    
    base_path = config['Paths'].get('BasePath', '')
    albums_path = config['Paths'].get('AlbumsPath', '')
    miscellaneous_path = config['Paths'].get('MiscellaneousPath', '')

    path_vars = PathVariables(base_path, albums_path, miscellaneous_path)

    # Create and place the GUI elements
    base_path_label = tk.Label(root, text="Source Path:")
    base_path_label.grid(row=0, column=0, sticky="e")
    base_path_entry = tk.Entry(root, textvariable=path_vars.base_path_var, width=40)
    base_path_entry.grid(row=0, column=1, sticky="ew")
    base_path_button = tk.Button(root, text="Browse", command=lambda: browse_directory(path_vars.base_path_var))
    base_path_button.grid(row=0, column=2)

    albums_path_label = tk.Label(root, text="Albums Path:")
    albums_path_label.grid(row=1, column=0, sticky="e")
    albums_path_entry = tk.Entry(root, textvariable=path_vars.albums_path_var, width=40)
    albums_path_entry.grid(row=1, column=1, sticky="ew")
    albums_path_button = tk.Button(root, text="Browse", command=lambda: browse_directory(path_vars.albums_path_var))
    albums_path_button.grid(row=1, column=2)

    miscellaneous_path_label = tk.Label(root, text="Miscellaneous Path:")
    miscellaneous_path_label.grid(row=2, column=0, sticky="e")
    miscellaneous_path_entry = tk.Entry(root, textvariable=path_vars.miscellaneous_path_var, width=40)
    miscellaneous_path_entry.grid(row=2, column=1, sticky="ew")
    miscellaneous_path_button = tk.Button(root, text="Browse", command=lambda: browse_directory(path_vars.miscellaneous_path_var))
    miscellaneous_path_button.grid(row=2, column=2)

    start_button = tk.Button(root, text="Organize My Files", command=lambda: start_processing(root, path_vars, status_label))
    start_button.grid(row=3, column=0, pady=20, padx=20, columnspan=3)

    separator = ttk.Separator(root, orient="horizontal")
    separator.grid(row=4, column=0, columnspan=3, sticky="ew", pady=10)

    status_label = tk.Label(root, text="")
    status_label.grid(row=5, column=0, columnspan=3)

    # Center the GUI on the screen
    root.update_idletasks()  # Ensure the window size is updated
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - window_height)
    root.geometry(f"+{x}+{y}")

    return root
