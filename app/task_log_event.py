from enum import Enum

class TaskLogEventDescription(Enum):
    added = "Aufgabe erstellt"
    delete = "Aufgabe gelöscht"
    isDone_changed = "Aufgabe abgehakt"
    error = "Änderungsstatus unbekannt"
