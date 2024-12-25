import os
import tkinter as tk
from tkinter import ttk, simpledialog
from treelib import Tree


class CustomTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Linux Terminal")
        self.root.geometry("1200x700")
        self.current_dir = os.getcwd()

        # Scratch-inspired color scheme
        bg_color = "#f7f3e9"
        sidebar_color = "#ffd43b"
        button_color = "#ffad33"
        text_color = "#333"

        # Frames
        self.command_frame = tk.Frame(self.root, bg=sidebar_color, width=250)
        self.command_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.output_frame = tk.Frame(self.root, bg=bg_color)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Command Buttons
        tk.Label(self.command_frame, text="Commands", bg=sidebar_color, fg=text_color, font=("Arial", 16)).pack(pady=10)
        commands = [
            ("List Files (ls)", self.list_files_with_animation),
            ("Change Directory (cd)", self.change_directory),
            ("Make Directory (mkdir)", self.create_directory),
            ("Remove Directory (rmdir)", self.remove_directory),
            ("Create File (touch)", self.create_file_with_animation),
            ("Echo Message (echo)", self.echo_message),
            ("Go Back (..)", self.go_back),
        ]

        for cmd_text, cmd_action in commands:
            button = tk.Button(
                self.command_frame,
                text=cmd_text,
                bg=button_color,
                fg="white",
                font=("Arial", 12),
                command=cmd_action,
                relief="flat",
            )
            button.pack(pady=5, padx=10, fill=tk.X)

        # Output Area
        self.output_area = tk.Text(self.output_frame, bg=bg_color, fg=text_color, font=("Courier", 12), state=tk.NORMAL)
        self.output_area.pack(fill=tk.BOTH, expand=True)

        # Input Area
        self.input_area = ttk.Entry(self.root, font=("Courier", 14))
        self.input_area.pack(fill=tk.X, side=tk.BOTTOM)
        self.input_area.bind("<Return>", self.execute_input_command)

        # Display Initial Directory
        self.display_current_directory()

    def display_current_directory(self):
        """Display the current directory in the terminal."""
        self.output_area.insert(tk.END, f"\n[Directory]: {self.current_dir}\n", "highlight")
        self.output_area.tag_config("highlight", foreground="#ff5722")
        self.output_area.see(tk.END)
    def list_files_with_animation(self):
        """List files with an animated tree structure."""
        self.output_area.insert(tk.END, "$ ls\n")
        self.output_area.see(tk.END)

        tree = Tree()
        tree.create_node("Root", self.current_dir)  # Root directory
        for root, dirs, files in os.walk(self.current_dir):
            parent_node = root
            for d in dirs:
                tree.create_node(d, os.path.join(root, d), parent=parent_node)
            for f in files:
                tree.create_node(f, os.path.join(root, f), parent=parent_node)

    # Animate the tree structure
        for line in self.tree_to_list(tree):
            self.output_area.insert(tk.END, line + "\n")
            self.output_area.see(tk.END)
            self.output_area.update()
            self.root.after(100)  # Pause for animation effect

    def tree_to_list(self, tree):
        """Convert a Tree object into a list of strings representing the structure."""
        result = []
        for line in tree._Tree__generate_tree(tree.root, tree.level, tree.filter_nodes):
            result.append(line)
        return result

  

    def animate_tree(self, tree):
        """Animate the tree structure display."""
        for line in tree.to_string().splitlines():
            self.output_area.insert(tk.END, line + "\n")
            self.output_area.see(tk.END)
            self.output_area.update()
            self.root.after(100)  # Pause for animation effect

    def create_file_with_animation(self):
        """Create a file with a popping animation."""
        file_name = simpledialog.askstring("Create File", "Enter file name:")
        if file_name:
            file_path = os.path.join(self.current_dir, file_name)
            try:
                with open(file_path, 'w') as f:
                    f.write("")
                self.output_area.insert(tk.END, f"$ touch {file_name}\nFile '{file_name}' created successfully.\n")
                self.output_area.see(tk.END)

                # Trigger pop animation
                self.pop_animation(file_name)
            except Exception as e:
                self.output_area.insert(tk.END, f"Error creating file: {str(e)}\n")

    def pop_animation(self, file_name):
        """Animate the creation of a file."""
        for size in range(10, 101, 10):
            self.output_area.insert(tk.END, f"Creating '{file_name}'... {size}% complete\n")
            self.output_area.see(tk.END)
            self.output_area.update()
            self.root.after(50)  # Delay for animation

    def change_directory(self):
        """Change the directory."""
        target_dir = simpledialog.askstring("Change Directory", "Enter target directory path:")
        if target_dir:
            try:
                os.chdir(target_dir)
                self.current_dir = os.getcwd()
                self.output_area.insert(tk.END, f"$ cd {target_dir}\nChanged directory to: {self.current_dir}\n")
                self.display_current_directory()
            except Exception as e:
                self.output_area.insert(tk.END, f"Error changing directory: {str(e)}\n")

    def create_directory(self):
        """Create a directory."""
        dir_name = simpledialog.askstring("Create Directory", "Enter directory name:")
        if dir_name:
            try:
                os.makedirs(os.path.join(self.current_dir, dir_name), exist_ok=True)
                self.output_area.insert(tk.END, f"$ mkdir {dir_name}\nDirectory '{dir_name}' created successfully.\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error creating directory: {str(e)}\n")

    def remove_directory(self):
        """Remove a directory."""
        dir_name = simpledialog.askstring("Remove Directory", "Enter directory name:")
        if dir_name:
            try:
                os.rmdir(os.path.join(self.current_dir, dir_name))
                self.output_area.insert(tk.END, f"$ rmdir {dir_name}\nDirectory '{dir_name}' removed successfully.\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error removing directory: {str(e)}\n")

    def echo_message(self):
        """Echo a message."""
        message = simpledialog.askstring("Echo Message", "Enter message:")
        if message:
            self.output_area.insert(tk.END, f"$ echo {message}\n{message}\n")

    def go_back(self):
        """Navigate to the parent directory."""
        try:
            os.chdir("..")
            self.current_dir = os.getcwd()
            self.output_area.insert(tk.END, f"$ cd ..\nMoved back to: {self.current_dir}\n")
            self.display_current_directory()
        except Exception as e:
            self.output_area.insert(tk.END, f"Error navigating back: {str(e)}\n")

    def execute_input_command(self, event):
        """Execute a command entered in the input box."""
        command = self.input_area.get().strip()
        self.input_area.delete(0, tk.END)
        if command:
            self.output_area.insert(tk.END, f"$ {command}\n")
            self.output_area.see(tk.END)
            try:
                os.system(command)
            except Exception as e:
                self.output_area.insert(tk.END, f"Error executing command: {str(e)}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomTerminal(root)
    root.mainloop()

