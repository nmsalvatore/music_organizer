from utilities import setup_logging
from gui import create_root_window


def main():
    # Set up logging
    setup_logging()

    # Create the main GUI window
    root = create_root_window()

    # Run the main GUI loop
    root.mainloop()

if __name__ == "__main__":
    main()
