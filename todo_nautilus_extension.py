import os
from urllib.parse import unquote, urlparse
from gi.repository import Nautilus, GObject#, Gdk, Gtk
import gi

CHECKED_CHAR = u'\u2713'  # Checkmark symbol
UNCHECKED_CHAR = u'\u2610'  # Empty checkbox symbol

class TaskStatusInfoProvider(GObject.GObject, Nautilus.ColumnProvider, Nautilus.InfoProvider):
    def get_columns(self):
        column = Nautilus.Column(
            name="file_task_done_checked",
            attribute="file_task_done_checked",
            label="Done",
            description="The task associated with the file has been done"
        )

        return column,

    def update_file_info(self, file):
        file_path = unquote(urlparse(file.get_uri()).path)

        # Check if todo.md exists in the same directory
        directory = os.path.dirname(file_path)
        todo_file_path = os.path.join(directory, "todo.md")

        # # Create a checkbox
        # checkbox = Gtk.CheckButton()
        # checkbox.connect("toggled", on_checkbox_toggled)

        # Check if todo.md exists and has the same name as the current file
        if os.path.exists(todo_file_path):
            with open(todo_file_path, 'r') as todo_file:
                todo_file_content = todo_file.read()
                file_name = os.path.basename(file_path)
                
                if file_name in todo_file_content:
                    # File name found in todo.md, set unchecked checkbox
                    file.add_emblem('unreadable')  # Replace with appropriate emblem
                    file.add_string_attribute('file_task_done_checked', UNCHECKED_CHAR)
                    
                else:
                    # File name not found in todo.md, set checked checkbox
                    file.add_emblem('default')  # Replace with appropriate emblem
                    file.add_string_attribute('file_task_done_checked', CHECKED_CHAR)
        else:
            # Todo.md doesn't exist, set checked checkbox
            file.add_emblem('checked')  # Replace with appropriate emblem
            file.add_string_attribute('file_task_done_checked', CHECKED_CHAR)

        # # Get the cell renderer for the "Done" column
        # cell_renderer = Nautilus.CellRendererPixbuf()
        # cell_renderer.set_padding(6, 6)

        # # Set the checkbox widget as the pixbuf for the cell renderer
        # if checkbox.get_active():
        #     pixbuf = Gtk.IconTheme.get_default().load_icon("checkbox-checked", 16, 0)
        # else:
        #     pixbuf = Gtk.IconTheme.get_default().load_icon("checkbox-unchecked", 16, 0)

        # cell_renderer.set_property("pixbuf", pixbuf)

        # # Add the cell renderer to the file info
        # file.add_info("standard::done_checkbox", cell_renderer)




class ToggleStatusExtension(GObject.GObject, Nautilus.MenuProvider):
   

    def toggle(self, menu, files):
        for file in files:
            file_path = unquote(urlparse(file.get_uri()).path)
            directory = os.path.dirname(file_path)
            todo_file_path = os.path.join(directory, "todo.md")
            file_name = os.path.basename(file_path)

            if os.path.exists(todo_file_path):
                with open(todo_file_path, 'r') as todo_file:
                    todo_file_content = todo_file.read()
                # Check if file_name is in todo_file_content
                if file_name in todo_file_content:
                    # File name found in todo.md, remove it
                    todo_file_content = todo_file_content.replace(file_name + '\n', '')
                    with open(todo_file_path, 'w') as todo_file:
                        todo_file.write(todo_file_content)
                else:
                    # File name not found in todo.md, insert it
                    with open(todo_file_path, 'a') as todo_file:
                        todo_file.write(file_name + '\n')
            else:
                # if todo.md doesn't exist create it and write the first task
                with open(todo_file_path, 'a') as todo_file:
                        todo_file.write(file_name + '\n')


    def get_file_items(self, files):
        if len(files) > 1:
            item_label = 'Toggle items'
        else:
            item_label = 'Toggle item'

        mark_as_done = Nautilus.MenuItem(
            name='MarkAsDone',
            label=item_label,
            tip='Toggle items as done or undone'
        )
        mark_as_done.connect('activate', self.toggle, files)
        #Nautilus.MenuProvider.emit_items_updated_signal();
        return mark_as_done,

   