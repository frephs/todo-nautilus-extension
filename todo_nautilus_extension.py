import os
from urllib.parse import unquote, urlparse
from gi.repository import Nautilus, GObject

# Define a mapping of states to their corresponding emojis
STATUS_EMOJI_MAP = {
    "todo": "🔴",          # Red circle for todo
    "in_progress": "🟡",   # Yellow circle for in progress
    "done": "🟢"           # Green circle for done
}

class TaskStatusProvider(GObject.GObject, Nautilus.ColumnProvider, Nautilus.InfoProvider):
    def get_columns(self):
        column = Nautilus.Column(
            name="file_task_status",
            attribute="file_task_status",
            label="Status",
            description="The status of the task associated with the file"
        )
        return column,

    def update_file_info(self, file):
        file_path = unquote(urlparse(file.get_uri()).path)
        directory = os.path.dirname(file_path)
        todo_file_path = os.path.join(directory, ".todo")

        if os.path.exists(todo_file_path):
            with open(todo_file_path, 'r') as todo_file:
                todo_file_content = todo_file.readlines()
                file_name = os.path.basename(file_path)

                for line in todo_file_content:
                    line = line.strip()
                    if line.endswith(file_name):  # Check if the line ends with the filename
                        status = line.split(' ')[0]  # Get the status (todo, in_progress, done)
                        emoji = STATUS_EMOJI_MAP.get(status, '')  # Get the corresponding emoji
                        file.add_string_attribute('file_task_status', emoji)
                        return

        # If the file is not found in the todo file, set it to empty
        file.add_string_attribute('file_task_status', '')
class ToggleStatusExtension(GObject.GObject, Nautilus.MenuProvider):
    def toggle(self, menu, files):
        for file in files:
            file_path = unquote(urlparse(file.get_uri()).path)
            directory = os.path.dirname(file_path)
            todo_file_path = os.path.join(directory, ".todo")
            file_name = os.path.basename(file_path)

            # Ensure the .todo file exists
            if not os.path.exists(todo_file_path):
                with open(todo_file_path, 'w') as todo_file:
                    todo_file.write('')

            # Read the current status from the .todo file
            with open(todo_file_path, 'r') as todo_file:
                todo_file_content = todo_file.readlines()

            # Check the current status of the file
            current_status = None
            new_todo_file_content = []
            for line in todo_file_content:
                if line.strip().endswith(file_name):  # Check if the line ends with the filename
                    current_status = line.strip().split(' ')[0]  # Get the current status
                else:
                    new_todo_file_content.append(line)  # Keep lines that do not match

            # Determine the new status
            if current_status in STATUS_EMOJI_MAP:
                current_index = list(STATUS_EMOJI_MAP.keys()).index(current_status)
                new_index = (current_index + 1) % len(STATUS_EMOJI_MAP)
                new_status = list(STATUS_EMOJI_MAP.keys())[new_index]
            else:
                new_status = "todo"  # Default to todo if not found

            # Append the new status at the end of the list
            new_todo_file_content.append(f"{new_status} {file_name}\n")

            # Write the updated content back to the .todo file
            with open(todo_file_path, 'w') as todo_file:
                todo_file.writelines(new_todo_file_content)

    def get_file_items(self, files):
        if len(files) > 1:
            item_label = 'Toggle next status for items'
        else:
            item_label = 'Toggle next status for item'

        toggle_status = Nautilus.MenuItem(
            name='ToggleStatus',
            label=item_label,
            tip='Toggle status for items'
        )
         
        # if the file is not in the todo file, return
        
        current_status = None
        
        for file in files:
            file_path = unquote(urlparse(file.get_uri()).path)
            directory = os.path.dirname(file_path)
            todo_file_path = os.path.join(directory, ".todo")
            file_name = os.path.basename(file_path)
        
            if os.path.exists(todo_file_path):
            
                with open(todo_file_path, 'r') as todo_file:
                    todo_file_content = todo_file.readlines()
                
                for line in todo_file_content:
                    if line.strip().endswith(file_name):
                        current_status = line.strip().split(' ')[0]
                        todo_file_content.remove(line)
                        break
            
            else :
                return
        
        if current_status is None:
            return        
        
        toggle_status.connect('activate', self.toggle, files)
        return toggle_status,
class ToggleTrackingExtension(GObject.GObject, Nautilus.MenuProvider):
    def toggle(self, menu, files):
        for file in files:
            file_path = unquote(urlparse(file.get_uri()).path)
            directory = os.path.dirname(file_path)
            todo_file_path = os.path.join(directory, ".todo")
            
            if not os.path.exists(todo_file_path):
                with open(todo_file_path, 'w') as todo_file:
                    todo_file.write('')                
                
            file_name = os.path.basename(file_path)

            with open(todo_file_path, 'r') as todo_file:
                todo_file_content = todo_file.readlines()
            
            # Check if file_name is in the todo_file_content
            if any(line.strip().endswith(file_name) for line in todo_file_content):
                # Remove the line that contains the file name
                todo_file_content = [line for line in todo_file_content if not line.strip().endswith(file_name)]                

                # Write the updated content back to the .todo file
                with open(todo_file_path, 'w') as todo_file:
                    todo_file.writelines(todo_file_content)
            else:
                with open(todo_file_path, 'a') as todo_file:
                    todo_file.write(f"todo {file_name}\n")

    def get_file_items(self, files):
        item_label = ''
        for file in files:
            file_path = unquote(urlparse(file.get_uri()).path)
            directory = os.path.dirname(file_path)
            todo_file_path = os.path.join(directory, ".todo")
            file_name = os.path.basename(file_path)
                        
            if os.path.exists(todo_file_path):
                with open(todo_file_path, 'r') as todo_file:
                    todo_file_content = todo_file.readlines()

                if (item_label == '' or item_label.startswith("Disable")) and any(line.strip().endswith(file_name) for line in todo_file_content):
                    item_label = 'Disable progress tracking for item'
                    if len(files) > 1:
                        item_label = 'Disable progress tracking for items'
                else:
                    if (item_label == '' or item_label.startswith("Enable")) and not any(line.strip().endswith(file_name) for line in todo_file_content):
                        item_label = 'Enable progress tracking for item'
                        if len(files) > 1:
                            item_label = 'Enable progress tracking for items'
                    else:
                        item_label = 'Toggle progress tracking for items'

            else:
                item_label = 'Enable progress tracking for item'
                if len(files) > 1:
                    item_label = 'Enable progress tracking for items'

        toggle_tracking = Nautilus.MenuItem(
            name='ToggleTracking',
            label=item_label,
            tip='Toggle tracking for items'
        )
        
        toggle_tracking.connect('activate', self.toggle, files)
        return toggle_tracking,
