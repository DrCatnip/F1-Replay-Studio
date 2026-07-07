from app.constants import *


def load_stylesheet():

    return f"""

QMainWindow {{
    background:{BACKGROUND};
}}

QWidget {{
    background:{BACKGROUND};
    color:{TEXT};
    font-family:"Segoe UI Variable";
    font-size:10pt;
}}

QToolTip {{
    background:#11161D;
    color:{TEXT};
    border:1px solid {BORDER};
    border-radius:6px;
    padding:6px;
}}

QFrame {{
    background:transparent;
}}

#Card {{

    background:{SURFACE};

    border:1px solid {BORDER};

    border-radius:8px;

}}

#Panel {{
    background:{SURFACE};
    border:1px solid {BORDER};
    border-radius:8px;
}}

#PanelHeader {{

    font-size:13px;

    font-weight:700;

    color:{TEXT};

    letter-spacing:0px;

}}

#MetricCard {{

    background:{SURFACE_LIGHT};

    border:1px solid {BORDER};

    border-radius:8px;

}}

#MetricTitle {{

    color:{TEXT_SECONDARY};

    font-size:10pt;

}}

#MetricValue {{

    font-size:24px;

    font-weight:700;

}}

#MetricUnit {{

    color:{TEXT_SECONDARY};

}}

QPushButton {{

    background:{SURFACE_LIGHT};

    border:1px solid {BORDER};

    border-radius:8px;

    padding:8px 14px;

    color:{TEXT};

}}

QPushButton:disabled {{
    color:#667085;
    background:#151A21;
    border-color:#252C36;
}}

QPushButton:hover {{

    background:#2D3542;

    border-color:#485568;

}}

QPushButton:pressed {{

    background:#11151B;

}}

#PrimaryButton {{
    background:{ACCENT};
    color:white;
    border:1px solid {ACCENT};
}}

#PrimaryButton:hover {{
    background:#FF2A23;
    border-color:#FF2A23;
}}

#SecondaryButton {{
    background:{SURFACE_LIGHT};
    color:{TEXT};
}}

#IconButton {{
    min-width:32px;
    max-width:32px;
    padding:8px 0px;
}}

QComboBox {{

    background:{SURFACE_LIGHT};

    border:1px solid {BORDER};

    border-radius:8px;

    padding:8px;

}}

QComboBox::drop-down {{
    border:none;
    width:24px;
}}

QComboBox QAbstractItemView {{
    background:{SURFACE};
    color:{TEXT};
    border:1px solid {BORDER};
    selection-background-color:{SURFACE_LIGHT};
}}

QLabel {{

    background:transparent;

}}

#Sidebar {{
    background:#10141A;
    border:1px solid {BORDER};
    border-radius:8px;
}}

#Toolbar {{
    background:#10141A;
    border:1px solid {BORDER};
    border-radius:8px;
}}

#Timeline {{
    background:{SURFACE};
    border:1px solid {BORDER};
    border-radius:8px;
}}

#Timeline QLabel {{
    color:{TEXT_SECONDARY};
}}

#Timeline QSlider::groove:horizontal {{
    height:6px;
    background:#2C3440;
    border-radius:3px;
}}

#Timeline QSlider::handle:horizontal {{
    background:{ACCENT};
    width:12px;
    margin:-5px 0;
    border-radius:6px;
}}

#ViewportHeader {{

    background:#11161D;

    border-top-left-radius:8px;

    border-top-right-radius:8px;

    border:1px solid #313946;

    border-bottom:none;

}}

#ViewportFooter {{

    background:#11161D;

    border-bottom-left-radius:8px;

    border-bottom-right-radius:8px;

    border:1px solid #313946;

    border-top:none;

}}

#ViewportTitle {{

    font-size:14px;

    font-weight:700;

}}

#ViewportSubtitle {{

    color:#98A2B3;

}}

#ViewportTime {{

    font-weight:600;

}}

#ViewportFooter QPushButton {{

    min-width:64px;

}}

#StatusBadge {{
    background:#1B2430;
    border:1px solid {BORDER};
    border-radius:8px;
    padding:4px 8px;
    color:{TEXT_SECONDARY};
}}

#Divider {{
    background:{BORDER};
}}

"""
