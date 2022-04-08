import os

from .project import Project


class Collection:
    def __init__(self, folder:str,  name: str):
        self.folder = folder
        self.name = name
        self.collection_path = folder + name + "/"
        self.projects = {}

        if not os.path.isdir(self.collection_path):
            # Os makedirs to ensure intermediate folder levels are created
            # instead of throwing an error
            os.makedirs(self.collection_path)

        # Load all projects under the collection, if any
        sub_folders = [f.name for f in os.scandir(self.collection_path) if f.is_dir()]

        for project_name in sub_folders:
            self.projects.update({project_name: Project(
                parent_folder=self.collection_path,
                name=project_name
            )})

    def add_project(self, project_name: str):
        """
        Adds a project to the collection. If the project already exists
        under the collection a duplicate is NOT but the event is logged

        -----
        :param project_name:
            String with the name of the project
        -----
        """
        if project_name not in self.projects.keys():
            self.projects.update({
                project_name: Project(
                    parent_folder=self.collection_path,
                    name=project_name
                )
            })
        else:
            print(f"A project with name {project_name} already exists under"
                  f"the collectio {self.name}")

        return self.projects[project_name]

    def delete(self):
        """
        Deletes the collection. Notice, this is an irreversible decision
        """
        # TODO: Make this delete the instance as well
        for k, project in self.projects:
            project.delete()

        os.rmdir(self.collection_path)





