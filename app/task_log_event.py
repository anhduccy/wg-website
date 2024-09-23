from enum import Enum

class TaskLogEventDescription(Enum):
    added = "Aufgabe erstellt"
    delete = "Aufgabe gelöscht"
    error = "Änderungsstatus unbekannt"
