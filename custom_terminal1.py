import os
import subprocess
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog
from treelib import Tree
import io


class CustomTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Linux Terminal")
        self.root.geometry("1200x700")
        self.current_dir = os.getcwd()
        self.command_history = []

        # Main layout
        self.command_frame = tk.Frame(self.root, bg="#2e2e2e", width=250)
        self.command_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.output_frame = tk.Frame(self.root, bg="black")
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Command Buttons
        tk.Label(self.command_frame, text="Commands", bg="#2e2e2e", fg="white", font=("Arial", 16)).pack(pady=10)
        commands = [
            ("List Files (ls)", self.list_files_with_animation),
            ("Change Directory (cd)", self.change_directory),
            ("Make Directory (mkdir)", self.create_directory),
            ("Remove Directory (rmdir)", self.remove_directory),
            ("Create File (touch)", self.create_file),
            ("Remove File (rm)", self.remove_file),
            ("Move File (mv)", self.move_file),
            ("Copy File (cp)", self.copy_file),
            ("View File Content (cat)", self.view_file_content),
            ("Search (grep)", self.search_in_files),
            ("Print Path (pwd)", self.print_current_directory),
            ("Concatenate Strings", self.concatenate_strings),
            ("History", self.show_command_history),
            ("Read File", self.read_file_content),
            ("Find Command", self.find_command),
            ("Echo Message", self.echo_message),
            ("Conditional Statements", self.conditional_statements),
        ]

        for cmd_text, cmd_action in commands:
            button = ttk.Button(self.command_frame, text=cmd_text, command=cmd_action)
            button.pack(pady=5, padx=10, fill=tk.X)

        # Output Area
        self.output_area = tk.Text(self.output_frame, bg="black", fg="white", font=("Courier", 12), state=tk.NORMAL)
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
        self.output_area.tag_config("highlight", foreground="cyan")
        self.output_area.see(tk.END)

    def tree_to_list(self, tree):
        """Convert a Tree object into a list of strings representing the structure."""
        buffer = io.StringIO()
        tree.show(stdout=buffer)
        buffer.seek(0)
        return buffer.read().splitlines()

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

        for line in self.tree_to_list(tree):
            self.output_area.insert(tk.END, line + "\n")
            self.output_area.see(tk.END)
            self.output_area.update()
            self.root.after(100)

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

    def create_file(self):
        """Create a file."""
        file_name = simpledialog.askstring("Create File", "Enter file name:")
        if file_name:
            try:
                with open(os.path.join(self.current_dir, file_name), 'w') as f:
                    f.write("")
                self.output_area.insert(tk.END, f"$ touch {file_name}\nFile '{file_name}' created successfully.\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error creating file: {str(e)}\n")

    def remove_file(self):
        """Remove a file."""
        file_name = simpledialog.askstring("Remove File", "Enter file name:")
        if file_name:
            try:
                os.remove(os.path.join(self.current_dir, file_name))
                self.output_area.insert(tk.END, f"$ rm {file_name}\nFile '{file_name}' removed successfully.\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error removing file: {str(e)}\n")

    def move_file(self):
        """Move a file."""
        source = simpledialog.askstring("Move File", "Enter source file path:")
        destination = simpledialog.askstring("Move File", "Enter destination file path:")
        if source and destination:
            try:
                os.rename(source, destination)
                self.output_area.insert(tk.END, f"$ mv {source} {destination}\nFile moved successfully.\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error moving file: {str(e)}\n")

    def copy_file(self):
        """Copy a file."""
        source = filedialog.askopenfilename(title="Select Source File")
        if source:
            destination = simpledialog.askstring("Copy File", "Enter destination path:")
            if destination:
                try:
                    with open(source, 'rb') as src_file:
                        with open(destination, 'wb') as dest_file:
                            dest_file.write(src_file.read())
                    self.output_area.insert(tk.END, f"$ cp {source} {destination}\nFile copied successfully.\n")
                except Exception as e:
                    self.output_area.insert(tk.END, f"Error copying file: {str(e)}\n")

    def view_file_content(self):
        """View file content."""
        file_name = simpledialog.askstring("View File Content", "Enter file name:")
        if file_name:
            try:
                with open(os.path.join(self.current_dir, file_name), 'r') as file:
                    content = file.read()
                self.output_area.insert(tk.END, f"$ cat {file_name}\n{content}\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error reading file: {str(e)}\n")

    def print_current_directory(self):
        """Print the current directory."""
        self.output_area.insert(tk.END, f"$ pwd\n{self.current_dir}\n")

    def concatenate_strings(self):
        """Concatenate strings."""
        string1 = simpledialog.askstring("Concatenate Strings", "Enter the first string:")
        string2 = simpledialog.askstring("Concatenate Strings", "Enter the second string:")
        if string1 and string2:
            self.output_area.insert(tk.END, f"$ concatenate\nResult: {string1 + string2}\n")

    def show_command_history(self):
        """Display the command history."""
        self.output_area.insert(tk.END, "$ history\n")
        for idx, command in enumerate(self.command_history, start=1):
            self.output_area.insert(tk.END, f"{idx}: {command}\n")

    def find_command(self):
        """Find a file or directory."""
        target = simpledialog.askstring("Find Command", "Enter file/directory name to search:")
        if target:
            result = []
            for root, dirs, files in os.walk(self.current_dir):
                if target in dirs or target in files:
                    result.append(os.path.join(root, target))
            if result:
                self.output_area.insert(tk.END, f"$ find {target}\nFound:\n" + "\n".join(result) + "\n")
            else:
                self.output_area.insert(tk.END, f"$ find {target}\nNo match found.\n")

    def search_in_files(self):
        """Search for a pattern in files."""
        pattern = simpledialog.askstring("Search (grep)", "Enter search pattern:")
        if pattern:
            try:
                result = subprocess.run(["grep", "-r", pattern, self.current_dir], capture_output=True, text=True)
                output = result.stdout if result.stdout else result.stderr
                self.output_area.insert(tk.END, f"$ grep {pattern}\n{output}\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error executing grep: {str(e)}\n")

    def read_file_content(self):
        """Read content of a file."""
        file_path = filedialog.askopenfilename(title="Select File to Read")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                self.output_area.insert(tk.END, f"$ read {file_path}\n{content}\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error reading file: {str(e)}\n")

    def echo_message(self):
        """Echo a message."""
        message = simpledialog.askstring("Echo Message", "Enter message:")
        if message:
            self.output_area.insert(tk.END, f"$ echo {message}\n{message}\n")

    def conditional_statements(self):
        """Handle a basic conditional statement."""
        condition = simpledialog.askstring("Conditional Statement", "Enter condition (e.g., '5 > 3'):")
        if condition:
            try:
                result = eval(condition)
                self.output_area.insert(tk.END, f"$ if {condition}\nCondition is {'true' if result else 'false'}\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error evaluating condition: {str(e)}\n")

    def execute_input_command(self, event):
        """Execute a command entered in the input box."""
        command = self.input_area.get().strip()
        self.input_area.delete(0, tk.END)
        if command:
            self.command_history.append(command)
            self.output_area.insert(tk.END, f"$ {command}\n")
            try:
                result = subprocess.run(command, shell=True, cwd=self.current_dir, capture_output=True, text=True)
                output = result.stdout if result.stdout else result.stderr
                self.output_area.insert(tk.END, output + "\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error executing command: {str(e)}\n")
            self.output_area.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomTerminal(root)
    root.mainloop()
