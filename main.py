from thoughts import Collection, Project, Note

app_folder = "C:/test/thoughts/"

# Create or load a collection
collection = Collection(folder=app_folder, name="MyFirstCollection")


# Create a project under the collection
project = collection.add_project(project_name="MyFirstProject")


# Create a note under the project
note = project.add_note()


# TODO: Make a funtion to write to the note file
# TODO: Update the note file when the note is no longer referenced
# TODO: Make a GUI
