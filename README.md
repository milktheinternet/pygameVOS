![alt text](https://github.com/milktheinternet/pygameVOS/blob/main/assets/screenshot.png?raw=true)

---

# Virtual Operating System (VOS)

Welcome to VOS, your personal virtual environment where you can interact with various applications seamlessly!

## Overview

VOS is built using Python and Pygame, providing a graphical interface to run multiple applications. It supports a variety of functionalities such as file management, application launching, and interactive user interfaces.

## Features

- **Application Management**: Run multiple applications concurrently.
- **File Operations**: Manage files and folders within the VOS environment.
- **User Interface**: Utilizes Pygame for graphical display and interactive elements.
- **Extensible**: Easily add new applications by extending base classes.

## Applications Included

- **Calculator**: Perform basic arithmetic operations.
- **Text Editor**: Edit and save text files.
- **Unminimizer**: Restore minimized applications.
- And more!

## Getting Started

1. **Installation**
   - Ensure Python and Pygame are installed.
   - Clone this repository:
     ```
     git clone https://github.com/milktheinternet/pygameVOS
     ```
   
2. **Setup**
   - Run the VOS application:
     ```
     python vos.py
     ```

3. **Usage**
   - Navigate using the GUI to access different applications.
   - Use the input methods supported by Pygame (keyboard, mouse) for interaction.

## Development

- **Adding New Applications**:
  - Create a new directory under `apps/` with an `app.py` file.
  - Extend the base application class defined in `app_loader.py`.

- **File Operations**:
  - Utilize VOS methods (`copy()`, `delete()`, `save()`, `load()`, etc.) for file handling.

## Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the CC0 License - see the `LICENSE` file for details.

## Acknowledgments

- You will be here if you submit a pull request!

---

Feel free to tailor this README to include specific details about your applications, installation instructions, and any other relevant information. Good luck with your VOS project!
