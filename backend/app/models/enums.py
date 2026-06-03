from enum import Enum


class Role(str, Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"


class WidgetType(str, Enum):
    KPI = "KPI"
    LINE = "LINE"
    BAR = "BAR"
    PIE = "PIE"