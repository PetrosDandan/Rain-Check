import os
import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QListWidget, QListWidgetItem, QStackedWidget, 
                             QLabel, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

# Explicitly direct Python to look inside the correct project directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.user import UserTableWidget
from data.umbrella import UmbrellaTableWidget
from data.penalty import PenaltyTableWidget
from data.payment import PaymentTableWidget

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Raincheck.db')

def init_database():
    """Initializes the database schema seamlessly on boot."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS USER (
            user_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, m_i TEXT, rfid_uid TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Umbrella (
            umbrella_id TEXT PRIMARY KEY, current_status TEXT, condition TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rents (
            rent_id TEXT PRIMARY KEY, user_id TEXT, umbrella_id TEXT, rent_date TEXT, due_date TEXT,
            FOREIGN KEY(user_id) REFERENCES USER(user_id), FOREIGN KEY(umbrella_id) REFERENCES Umbrella(umbrella_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS returns (
            return_id INTEGER PRIMARY KEY AUTOINCREMENT, rent_id TEXT, return_date TEXT, return_condition TEXT,
            FOREIGN KEY(rent_id) REFERENCES rents(rent_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS penalty (
            penalty_id TEXT PRIMARY KEY, user_id TEXT, penalty_reason TEXT, date_issued TEXT, amount REAL, paid_status TEXT,
            FOREIGN KEY(user_id) REFERENCES USER(user_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id TEXT PRIMARY KEY, penalty_id TEXT, method TEXT, amount_paid REAL, payment_date TEXT,
            FOREIGN KEY(penalty_id) REFERENCES penalty(penalty_id)
        )
    """)
    conn.commit()
    conn.close()


class DashboardWidget(QWidget):
    """The analytical monitoring dashboard main screen containing live summary metric widgets."""
    def __init__(self, db_path, parent_window):
        super().__init__()
        self.db_path = db_path
        self.parent_window = parent_window
        self.init_ui()
        self.refresh_stats()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Logged-in Operator Badge Indicator Banner
        user_badge = QLabel("Logged in as: Front Desk Staff")
        user_badge.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        user_badge.setStyleSheet("""
            background-color: #1A365D; 
            color: white; 
            padding: 10px 20px; 
            border-radius: 8px;
        """)
        user_badge.setFixedWidth(260)
        layout.addWidget(user_badge)
        layout.addSpacing(10)

        # Section Header: Quick Stats
        stats_header = QLabel("QUICK STATS")
        stats_header.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        stats_header.setStyleSheet("color: #A0AEC0; letter-spacing: 1px;")
        layout.addWidget(stats_header)

        # --- GRAPHIC METRIC CARDS ROW ---
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(20)

        # Card 1: Available Umbrellas (Green Theme)
        self.card_avail = QFrame()
        self.setup_metric_card(self.card_avail, "☂", "Available Umbrellas", "Ready to rent", "#48BB78", "#E6FFFA")
        grid_layout.addWidget(self.card_avail)

        # Card 2: Active Rentals (Yellow Theme)
        self.card_rented = QFrame()
        self.setup_metric_card(self.card_rented, "🕒", "Active Rentals", "Currently Out", "#ECC94B", "#FEFCBF")
        grid_layout.addWidget(self.card_rented)

        # Card 3: Overdue Rentals (Red Theme - Centered Warning Badge)
        self.card_penalties = QFrame()
        self.setup_metric_card(self.card_penalties, "⚠️", "Overdue Rentals", "Past limit", "#F56565", "#FED7D7")
        grid_layout.addWidget(self.card_penalties)

        layout.addLayout(grid_layout)
        layout.addSpacing(20)

        # Section Header: Actions
        actions_header = QLabel("ACTIONS")
        actions_header.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        actions_header.setStyleSheet("color: #A0AEC0; letter-spacing: 1px;")
        layout.addWidget(actions_header)

        # --- QUICK ACTIONS BUTTON RUNWAY ---
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(25)

        # Rent Button (Hollow/Outline style hand indicator)
        btn_rent = QFrame()
        btn_rent.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_rent.setStyleSheet("background-color: #1A365D; border-radius: 12px;")
        btn_rent_layout = QVBoxLayout(btn_rent)
        btn_rent_layout.setContentsMargins(20, 30, 20, 30)
        btn_rent_layout.setSpacing(8)
        
        lbl_rent_icon = QLabel("📋")
        lbl_rent_icon.setFont(QFont("Arial", 22))
        lbl_rent_icon.setStyleSheet("color: #ECC94B;") # Yellow outline color styling
        lbl_rent_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_rent_text = QLabel("RENT UMBRELLA")
        lbl_rent_text.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        lbl_rent_text.setStyleSheet("color: white;")
        lbl_rent_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_rent_layout.addWidget(lbl_rent_icon)
        btn_rent_layout.addWidget(lbl_rent_text)
        btn_rent.mousePressEvent = lambda e: self.parent_window.sidebar_menu.setCurrentRow(1)
        actions_layout.addWidget(btn_rent)

        # Return Button (Yellow return arrow indicator)
        btn_return = QFrame()
        btn_return.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_return.setStyleSheet("background-color: #1A365D; border-radius: 12px;")
        btn_return_layout = QVBoxLayout(btn_return)
        btn_return_layout.setContentsMargins(20, 30, 20, 30)
        btn_return_layout.setSpacing(8)
        
        lbl_return_icon = QLabel("↩")
        lbl_return_icon.setFont(QFont("Arial", 22))
        lbl_return_icon.setStyleSheet("color: #ECC94B;") # Yellow arrow styling
        lbl_return_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_return_text = QLabel("RETURN UMBRELLA")
        lbl_return_text.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        lbl_return_text.setStyleSheet("color: white;")
        lbl_return_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_return_layout.addWidget(lbl_return_icon)
        btn_return_layout.addWidget(lbl_return_text)
        btn_return.mousePressEvent = lambda e: self.parent_window.sidebar_menu.setCurrentRow(1)
        actions_layout.addWidget(btn_return)

        layout.addLayout(actions_layout)
        layout.addStretch()

    def setup_metric_card(self, frame, icon_char, title_text, bottom_text, color_hex, bg_hex):
        """Assembles the layout structure matching the UI blueprint layout requirements."""
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
        """)
        
        card_layout = QVBoxLayout(frame)
        card_layout.setContentsMargins(20, 25, 20, 25)
        card_layout.setSpacing(8)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Balanced Horizontal Layout to Ensure Absolute Center Alignment for the Badges
        icon_wrapper = QHBoxLayout()
        icon_wrapper.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_badge = QLabel(icon_char)
        icon_badge.setFixedSize(42, 42)
        icon_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_badge.setFont(QFont("Arial", 16))
        icon_badge.setStyleSheet(f"""
            background-color: {bg_hex};
            color: {color_hex};
            border: none;
            border-radius: 21px;
        """)
        icon_wrapper.addWidget(icon_badge)
        card_layout.addLayout(icon_wrapper)

        # Big Stat Numeric Count Output
        val_lbl = QLabel("0")
        val_lbl.setObjectName("counter_value")
        val_lbl.setFont(QFont("Arial", 36, QFont.Weight.Medium))
        val_lbl.setStyleSheet("color: #1A202C; border: none; background: transparent;")
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(val_lbl)

        # Mid Card Title Label
        title_lbl = QLabel(title_text)
        title_lbl.setFont(QFont("Arial", 11, QFont.Weight.Medium))
        title_lbl.setStyleSheet("color: #4A5568; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_lbl)

        # Dynamic Status Footer Tag
        desc_lbl = QLabel(bottom_text)
        desc_lbl.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        desc_lbl.setStyleSheet(f"color: {color_hex}; border: none; background: transparent;")
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(desc_lbl)

    def refresh_stats(self):
        """Pulls updated aggregates straight from SQLite tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Umbrella WHERE current_status = 'Available'")
        self.card_avail.findChild(QLabel, "counter_value").setText(str(cursor.fetchone()[0]))

        cursor.execute("SELECT COUNT(*) FROM Umbrella WHERE current_status = 'Rented'")
        self.card_rented.findChild(QLabel, "counter_value").setText(str(cursor.fetchone()[0]))

        cursor.execute("SELECT COUNT(*) FROM penalty WHERE paid_status = 'Unpaid'")
        self.card_penalties.findChild(QLabel, "counter_value").setText(str(cursor.fetchone()[0]))

        conn.close()


class MainApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raincheck")
        self.setGeometry(100, 100, 1250, 780)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # =====================================================================
        # SIDEBAR NAVIGATION
        # =====================================================================
        sidebar_panel = QFrame()
        sidebar_panel.setFixedWidth(240)
        sidebar_panel.setStyleSheet("background-color: #1A365D; border: none;") 
        sidebar_layout = QVBoxLayout(sidebar_panel)
        sidebar_layout.setContentsMargins(15, 30, 15, 30)
        sidebar_layout.setSpacing(10)
        
        brand_icon = QLabel("☂")
        brand_icon.setFont(QFont("Arial", 32))
        brand_icon.setStyleSheet("color: #ECC94B; padding-left: 5px;")
        
        brand_title = QLabel("Raincheck")
        brand_title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        brand_title.setStyleSheet("color: white;")
        
        brand_subtitle = QLabel("Umbrella Rental System")
        brand_subtitle.setFont(QFont("Arial", 9))
        brand_subtitle.setStyleSheet("color: #A0AEC0;")
        
        sidebar_layout.addWidget(brand_icon)
        sidebar_layout.addWidget(brand_title)
        sidebar_layout.addWidget(brand_subtitle)
        sidebar_layout.addSpacing(25)
        
        self.sidebar_menu = QListWidget()
        self.sidebar_menu.setSpacing(5)
        
        # Hides the vertical and horizontal scrollbars explicitly
        self.sidebar_menu.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sidebar_menu.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.sidebar_menu.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
            }
            QListWidget::item {
                color: #CBD5E0;
                padding: 10px 15px;
                border-radius: 6px;
                font-family: 'Arial';
                font-size: 13px;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #2D3748;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #2B6CB0;
                color: white;
            }
        """)
        
        # Ordered Menu Items Array
        menu_items = ["Dashboard", "Rentals & Inventory", "Penalties", "Payments", "Users"]
        for item_text in menu_items:
            item = QListWidgetItem(item_text)
            item.setSizeHint(QSize(200, 42))
            self.sidebar_menu.addItem(item)
            
        sidebar_layout.addWidget(self.sidebar_menu)
        sidebar_layout.addStretch()
        
        # =====================================================================
        # DISPLAY STACK CONTENT REGISTER
        # =====================================================================
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #F7FAFC;")
        
        # Load Modular views
        self.dashboard_view = DashboardWidget(DB_FILE, self)
        self.umbrella_view = UmbrellaTableWidget(DB_FILE)
        self.penalty_view = PenaltyTableWidget(DB_FILE)
        self.payment_view = PaymentTableWidget(DB_FILE)
        self.user_view = UserTableWidget(DB_FILE)
        
        # Map subviews to Stack container indexes sequential layout order
        self.content_stack.addWidget(self.dashboard_view) # Index 0: Dashboard Home
        self.content_stack.addWidget(self.umbrella_view)  # Index 1: Rentals & Inventory
        self.content_stack.addWidget(self.penalty_view)   # Index 2: Penalties Grid Logs
        self.content_stack.addWidget(self.payment_view)   # Index 3: Payments Ledger Records
        self.content_stack.addWidget(self.user_view)      # Index 4: Student Users Directory
        
        main_layout.addWidget(sidebar_panel)
        main_layout.addWidget(self.content_stack)
        
        self.sidebar_menu.currentRowChanged.connect(self.switch_view_panel)
        self.sidebar_menu.setCurrentRow(0) # Launch cleanly into dashboard layout on boot

    def switch_view_panel(self, index):
        """Switches window and fires background data reload functions."""
        self.content_stack.setCurrentIndex(index)
        try:
            if index == 0: self.dashboard_view.refresh_stats()
            elif index == 1: self.umbrella_view.load_all_data()
            elif index == 2: self.penalty_view.load_data()
            elif index == 3: self.payment_view.load_data()
            elif index == 4: self.user_view.load_data()
        except Exception as e:
            print(f"Stack interface notice: {e}")


if __name__ == "__main__":
    init_database()
    app = QApplication(sys.argv)
    window = MainApplicationWindow()
    window.show()
    sys.exit(app.exec())