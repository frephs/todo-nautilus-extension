import os
from urllib.parse import unquote, urlparse
from gi.repository import Nautilus, GObject#, Gdk, Gtk
import gi

CHECKED_CHAR = u'\u2713'  # Checkmark symbol
UNCHECKED_CHAR = u'\u2610'  # Empty checkbox symbol
INPROGRESS_CHAR = u'\u25B6'  # Right-pointing triangle symbol

class TaskDoneInfoProvider(GObject.GObject, Nautilus.ColumnProvider, Nautilus.InfoProvider):
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
        todo_file_path = os.path.join(directory, ".todo.md")
        in_progress_file_path = os.path.join(directory, ".in_progress.md")
        done_file_path = os.path.join(directory, ".done.md")

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
                    #file.add_emblem('unreadable')  # Replace with appropriate emblem
                    file.add_string_attribute('file_task_done_checked', UNCHECKED_CHAR)
        if os.path.exists(in_progress_file_path):
            with open(in_progress_file_path, 'r') as in_progress_file:
                in_progress_file_content = in_progress_file.read()
                if file_name in in_progress_file_content:
                    # File name not found in todo.md, set checked checkbox
                    #file.add_emblem('synced')  # Replace with appropriate emblem
                    file.add_string_attribute('file_task_done_checked', INPROGRESS_CHAR)
        if os.path.exists(done_file_path):
            with open(done_file_path, 'r') as done_file:
                done_file_content = done_file.read()
                if file_name in done_file_content:
                    # File name not found in todo.md, set checked checkbox
                    file.add_string_attribute('file_task_done_checked', CHECKED_CHAR)
                    #file.add_emblem('default')
                        

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




class MarkAsDoneExtension(GObject.GObject, Nautilus.MenuProvider):
   

    def toggle(self, menu, files):

        # Get the paths for all the files.
        # Also, strip any protocol headers, if required.
        # TODO confirm with author:
        #  windows function doesn't sanitize file names here.
        #  is this correct? if so this behavior needs to change
        #  also, this would probably a lot cleaner with pathlib

        for file in files:
            file_path = unquote(urlparse(file.get_uri()).path)
            directory = os.path.dirname(file_path)
            
            todo_file_path = os.path.join(directory, ".todo.md")
            in_progress_file_path = os.path.join(directory, ".in_progress.md")
            done_file_path = os.path.join(directory, ".done.md")
            
            file_name = os.path.basename(file_path)

            if os.path.exists(todo_file_path):
                if not os.path.exists(in_progress_file_path):
                    with open(in_progress_file_path, 'w') as in_progress_file:
                        in_progress_file.write('\n')
                if not os.path.exists(done_file_path):
                    with open(done_file_path, 'w') as done_file:
                        done_file.write('\n')
                
                with open(todo_file_path, 'r') as todo_file:
                    todo_file_content = todo_file.read()
                with open(in_progress_file_path, 'r') as in_progress_file:
                    in_progress_file_content = in_progress_file.read()
                with open(done_file_path, 'r') as done_file:
                    done_file_content = done_file.read()
                
                # Check if file_name is in todo_file_content
                if file_name in todo_file_content:
                    todo_file_content = todo_file_content.replace(file_name + '\n', '')
                    with open(todo_file_path, 'w') as todo_file:
                        todo_file.write(todo_file_content)
                    with open(in_progress_file_path, 'a') as in_progress_file:
                        in_progress_file.write(file_name + '\n')
                    
                    
                elif file_name in in_progress_file_content:
                    in_progress_file_content = in_progress_file_content.replace(file_name + '\n', '')
                    with open(in_progress_file_path, 'w') as in_progress_file:
                        in_progress_file.write(in_progress_file_content)
                    with open(done_file_path, 'a') as done_file:
                        done_file.write(file_name + '\n')
                
                elif file_name in done_file_content:
                    done_file_content = done_file_content.replace(file_name + '\n', '')
                    with open(done_file_path, 'w') as done_file:
                        done_file.write(done_file_content)
                    with open(todo_file_path, 'a') as todo_file:
                        todo_file.write(file_name + '\n')
                
                else:
                    # File name not found in todo.md, in_progress.md, or done.md, we add it to todo.md                    
                    with open(todo_file_path, 'a') as todo_file:
                        todo_file.write(file_name + '\n')

                        
                        

    def get_file_items(self, files):
        # files = args[0] if gi_version_major == 4 else args[1]

        # If there are many items to copy, change the label
        # to reflect that.
        if len(files) > 1:
            item_label = 'Toggle items'
        else:
            item_label = 'Toggle item'

        mark_as_done = Nautilus.MenuItem(
            name='MarkAsDone',
            label=item_label,
            tip='Toggle items as done, undone, or in progress'
        )
        mark_as_done.connect('activate', self.toggle, files)
        #Nautilus.MenuProvider.emit_items_updated_signal();
        return mark_as_done,

   
