from statikk.core.domain.value_objects import ProjectID

class Project:
    """
    Represents a Project in the system.

    :param project_id: Unique identifier for the project.
    :type project_id: ProjectID
    :param name: The name of the project.
    :type name: str
    :param description: A description of the project.
    :type description: str
    """

    def __init__(self, project_id: ProjectID, name: str, description: str = ""):
        self.project_id = project_id
        self.name = name
        self.description = description
