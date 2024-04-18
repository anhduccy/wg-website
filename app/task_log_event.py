from enum import Enum

class TaskLogEventDescription(Enum):
    added = "Aufgabe erstellt"
    delete = "Aufgabe gelöscht"
    isDone_changed = "Aufgabe abgehakt"
    title_changed = "Aufgabentitel geändert"
    points_changed = "Punkte geändert"
    deadlineDate_changed = "Erstes Fälligkeitsdatum geändert"
    responsibility_changed = "Zuständigkeitsperson geändert"
    frequency_changed = "Wiedeholungen geändert"
    error = "Änderungsstatus unbekannt"
