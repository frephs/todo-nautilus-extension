# Todo Nautilus File Manager Integration
This Python script provides an extension for the Nautilus file manager, allowing users to mark files with different statuses by managing a to-do list file named ".todo" in the same directory as the file. It utilizes emojis to indicate the status of the task associated with each file.

## Usage 

1. Clone or download this repository.
2. Copy the `todo_nautilus_extension.py` file to the appropriate Nautilus extensions directory (usually `~/.local/share/nautilus-python/extensions/`).
3. Give the extension executable permissions by running `chmod +x todo_nautilus_extension.py` in the terminal.
4. Restart Nautilus by running `nautilus -q` in the terminal.

## Features

### Task Status Column

A new column named "Status" is added to the file view, indicating the status of the task associated with each file. The column displays a red circle (🔴) for `todo` tasks, a yellow circle (🟡) for `in_progress` tasks, and a green circle (🟢) for `done` tasks.

Enable it by right-clicking on some empty space and selecting `Status` from the context menu opened when clicking `Visible columns`.
### Toggle Task Status

- Right-click on one or more files in Nautilus.
- Select "Toggle status for item" or "Toggle status for items" from the context menu to change the status of the selected file(s).

### Toggle Progress Tracking

- Right-click on one or more files in Nautilus.
- Select "Enable progress tracking for item" or "Enable progress tracking for items" from the context menu to start tracking the progress of the selected file(s).
- Select "Disable progress tracking for item" or "Disable progress tracking for items" from the context menu to stop tracking the progress of the selected file(s).
- If the files are mixed tracked and untracked, the context menu will show "Toggle progress tracking for items" to toggle the tracking status of all selected files. 

## Implementation Details

The extension utilizes the Nautilus extension API and integrates with the Nautilus file manager to provide the mentioned features. It parses the file paths, checks for the presence of a ".todo" file, and updates the file icons and the "Status" column accordingly based on the task status.

### Files

- `todo_nautilus_extension.py`: Contains the main extension logic and integrates with Nautilus to provide the functionality.

## Note

This extension assumes the existence of a `.todo` file in the same directory as the file being examined. The extension considers a task associated with a file as "done" if the file name is found in the `.todo` file.

For any issues or improvements, feel free to open an issue or submit a pull request.

Enjoy managing your file-related tasks efficiently with Nautilus!

##  Demo
<video controls>
  <source src="src/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>