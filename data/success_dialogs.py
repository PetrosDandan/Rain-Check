import sqlite3
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class CustomSuccessDialogBase(QDialog):
    """Base dialog container implementing the clean aesthetic, professional spacing, and shadow of the mockups."""
    def __init__(self, border_top_color, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedWidth(400)
        
        # Outer container for shadowing
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(10, 10, 10, 10)
        
        self.frame = QFrame()
        self.frame.setObjectName("DialogCard")
        # Top accent border, white background, rounded border
        self.frame.setStyleSheet(f"""
            QFrame#DialogCard {{
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-top: 4px solid {border_top_color};
                border-radius: 12px;
            }}
        """)
        
        # Soft shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(17, 24, 39, 25))
        self.frame.setGraphicsEffect(shadow)
        
        self.layout = QVBoxLayout(self.frame)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(14)
        
        self.outer_layout.addWidget(self.frame)
        
    def add_header(self, title, subtitle, is_orange=False):
        """Header with structured icon and text alignment."""
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Rounded Info Circle
        icon_lbl = QLabel()
        icon_lbl.setFixedSize(32, 32)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        circle_color = "#f59e0b" if is_orange else "#10b981"
        icon_char = "ℹ️"
        
        # Clean circular label styling
        icon_lbl.setStyleSheet(f"""
            QLabel {{
                border: 2px solid {circle_color};
                border-radius: 16px;
                background-color: transparent;
                font-size: 14px;
                color: {circle_color};
                font-weight: bold;
            }}
        """)
        icon_lbl.setText(icon_char)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        title_lbl = QLabel(title)
        title_lbl.setWordWrap(True)
        title_lbl.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #111827;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
        """)
        
        sub_lbl = QLabel(subtitle)
        sub_lbl.setWordWrap(True)
        sub_lbl.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #4b5563;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
        """)
        
        text_layout.addWidget(title_lbl)
        text_layout.addWidget(sub_lbl)
        
        header_layout.addWidget(icon_lbl)
        header_layout.addLayout(text_layout)
        header_layout.addStretch()
        
        self.layout.addLayout(header_layout)
        
    def add_ok_button(self):
        """Standard beautiful OK button aligned on the right."""
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.setFixedSize(60, 28)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #11224d;
                border: 1px solid #11224d;
                border-radius: 6px;
                font-size: 11px;
                font-weight: bold;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            QPushButton:hover {
                background-color: #f3f4f6;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        self.layout.addLayout(btn_layout)


class RentSuccessDialog(CustomSuccessDialogBase):
    """Custom high-fidelity rent transaction success modal dialog."""
    def __init__(self, rent_id, due_date, parent=None):
        super().__init__("#10b981", parent)
        self.add_header("Equipment successfully leased!", "Umbrella is now checked out and assigned.")
        
        # Info Box 1: Rental ID (light blue card)
        rent_card = QFrame()
        rent_card.setStyleSheet("""
            QFrame {
                background-color: #eff6ff;
                border: none;
                border-radius: 6px;
            }
        """)
        rent_card_layout = QHBoxLayout(rent_card)
        rent_card_layout.setContentsMargins(12, 8, 12, 8)
        
        rent_lbl = QLabel(f"📋 Rental ID: {rent_id}")
        rent_lbl.setStyleSheet("""
            QLabel {
                color: #1e40af;
                font-size: 11px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        rent_card_layout.addWidget(rent_lbl)
        self.layout.addWidget(rent_card)
        
        # Info Box 2: Due Date (light green card)
        due_card = QFrame()
        due_card.setStyleSheet("""
            QFrame {
                background-color: #ecfdf5;
                border: none;
                border-radius: 6px;
            }
        """)
        due_card_layout = QHBoxLayout(due_card)
        due_card_layout.setContentsMargins(12, 8, 12, 8)
        
        due_lbl = QLabel(f"🕒 Due on: {due_date}")
        due_lbl.setStyleSheet("""
            QLabel {
                color: #065f46;
                font-size: 11px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        due_card_layout.addWidget(due_lbl)
        self.layout.addWidget(due_card)
        
        self.add_ok_button()


class ReturnSuccessDialog(CustomSuccessDialogBase):
    """Custom high-fidelity simple return checklist success modal dialog."""
    def __init__(self, parent=None):
        super().__init__("#10b981", parent)
        self.add_header("Return successful", "Equipment safely returned and checked in.")
        self.add_ok_button()


class PaymentSuccessDialog(CustomSuccessDialogBase):
    """Custom high-fidelity payment transaction receipt generation modal."""
    def __init__(self, payment_id, parent=None):
        super().__init__("#10b981", parent)
        self.add_header(
            "Payment recorded", 
            f"Successfully settled balance! Payment receipt ID created:\n{payment_id}"
        )
        self.add_ok_button()


class ReturnPenaltySuccessDialog(CustomSuccessDialogBase):
    """Custom high-fidelity penalty invoice modal overlay following late returns or property liabilities."""
    def __init__(self, reason, amount, penalty_id, parent=None):
        super().__init__("#f59e0b", parent)
        self.add_header(
            "Return successful", 
            "Equipment safely returned and checked in. An invoice has been issued for the following penalty.",
            is_orange=True
        )
        
        # Cream/Orange Invoiced Penalty Card
        penalty_card = QFrame()
        penalty_card.setStyleSheet("""
            QFrame {
                background-color: #fffbeb;
                border: 1px solid #fef3c7;
                border-radius: 6px;
            }
        """)
        penalty_layout = QHBoxLayout(penalty_card)
        penalty_layout.setContentsMargins(12, 10, 12, 10)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        type_lbl = QLabel("INVOICED PENALTY")
        type_lbl.setStyleSheet("""
            QLabel {
                color: #b45309;
                font-size: 9px;
                font-weight: bold;
                letter-spacing: 0.5px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        
        desc_lbl = QLabel(reason)
        desc_lbl.setStyleSheet("""
            QLabel {
                color: #111827;
                font-size: 11px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        
        text_layout.addWidget(type_lbl)
        text_layout.addWidget(desc_lbl)
        
        amt_lbl = QLabel(f"₱ {amount:.2f}")
        amt_lbl.setStyleSheet("""
            QLabel {
                color: #b45309;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        amt_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        penalty_layout.addLayout(text_layout)
        penalty_layout.addStretch()
        penalty_layout.addWidget(amt_lbl)
        
        self.layout.addWidget(penalty_card)
        
        # Info Box 2: Reference Code Card (light blue)
        ref_card = QFrame()
        ref_card.setStyleSheet("""
            QFrame {
                background-color: #eff6ff;
                border: none;
                border-radius: 6px;
            }
        """)
        ref_layout = QHBoxLayout(ref_card)
        ref_layout.setContentsMargins(12, 8, 12, 8)
        
        ref_lbl = QLabel(f"REF: {penalty_id}")
        ref_lbl.setStyleSheet("""
            QLabel {
                color: #1e40af;
                font-size: 11px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        ref_layout.addWidget(ref_lbl)
        self.layout.addWidget(ref_card)
        
        self.add_ok_button()


class DeleteUmbrellaDialog(QDialog):
    """Custom high-fidelity delete confirmation dialog for umbrellas."""
    def __init__(self, umb_id, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedWidth(520)
        
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(10, 10, 10, 10)
        
        frame = QFrame()
        frame.setObjectName("DeleteCard")
        frame.setStyleSheet("""
            QFrame#DeleteCard {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-top: 4px solid #f87171;
                border-radius: 12px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(17, 24, 39, 25))
        frame.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Header Row Layout
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Trash Can Icon
        icon_lbl = QLabel("🗑️")
        icon_lbl.setFixedSize(40, 40)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("""
            QLabel {
                background-color: #fee2e2;
                border: 1px solid #fecaca;
                border-radius: 8px;
                font-size: 18px;
            }
        """)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        title_lbl = QLabel("Delete umbrella")
        title_lbl.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #111827;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
        """)
        
        # Rich Text Description highlighting the ID exactly like the tag
        desc_lbl = QLabel(
            f"Are you sure you want to permanently delete Umbrella ID "
            f"<span style='background-color: #fee2e2; color: #b91c1c; font-family: monospace; font-size: 12px; font-weight: bold; border-radius: 4px;'>&nbsp;{umb_id}&nbsp;</span>? "
            f"This action cannot be undone."
        )
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #4b5563;
                line-height: 1.6;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
        """)
        
        text_layout.addWidget(title_lbl)
        text_layout.addWidget(desc_lbl)
        
        header_layout.addWidget(icon_lbl)
        header_layout.addLayout(text_layout)
        
        layout.addLayout(header_layout)
        
        # Bottom Buttons Row
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setFixedSize(85, 32)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #2563eb;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        delete_btn = QPushButton("DELETE")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setFixedSize(100, 32)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        delete_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(delete_btn)
        
        layout.addLayout(btn_layout)
        outer_layout.addWidget(frame)


class CannotDeleteUmbrellaDialog(QDialog):
    """Custom high-fidelity warning dialog when umbrella cannot be deleted due to active leases."""
    def __init__(self, umb_id, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedWidth(520)
        
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(10, 10, 10, 10)
        
        frame = QFrame()
        frame.setObjectName("BlockCard")
        frame.setStyleSheet("""
            QFrame#BlockCard {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-top: 4px solid #f59e0b;
                border-radius: 12px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(17, 24, 39, 25))
        frame.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Header Row Layout
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Info 'i' Circle Icon
        icon_lbl = QLabel("i")
        icon_lbl.setFixedSize(36, 36)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("""
            QLabel {
                background-color: #fef3c7;
                border: 2px solid #fcd34d;
                border-radius: 18px;
                color: #d97706;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Georgia', serif;
            }
        """)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        title_lbl = QLabel("Cannot delete umbrella")
        title_lbl.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #111827;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
        """)
        
        # Rich Text Detail warning text matching colors completely
        desc_lbl = QLabel(
            f"Umbrella ID <span style='background-color: #fef3c7; color: #b45309; font-family: monospace; font-size: 12px; font-weight: bold; border-radius: 4px;'>&nbsp;{umb_id}&nbsp;</span> "
            f"cannot be deleted because it is currently rented out.<br>"
            f"<span style='color: #b45309; font-weight: bold;'>Please settle the active rental in the Return Tab before deleting this item.</span>"
        )
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #4b5563;
                line-height: 1.6;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
        """)
        
        text_layout.addWidget(title_lbl)
        text_layout.addWidget(desc_lbl)
        
        header_layout.addWidget(icon_lbl)
        header_layout.addLayout(text_layout)
        
        layout.addLayout(header_layout)
        
        # Bottom Buttons Row
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.setFixedSize(85, 32)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #1e3a8a;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)
        outer_layout.addWidget(frame)


class DeleteUserDialog(QDialog):
    """Custom high-fidelity delete confirmation dialog for users/students."""
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedWidth(520)
        
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(10, 10, 10, 10)
        
        frame = QFrame()
        frame.setObjectName("DeleteCard")
        frame.setStyleSheet("""
            QFrame#DeleteCard {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-top: 4px solid #f87171;
                border-radius: 12px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(17, 24, 39, 25))
        frame.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Header Row Layout
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Trash Can Icon
        icon_lbl = QLabel("🗑️")
        icon_lbl.setFixedSize(40, 40)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("""
            QLabel {
                background-color: #fee2e2;
                border: 1px solid #fecaca;
                border-radius: 8px;
                font-size: 18px;
            }
        """)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        title_lbl = QLabel("Delete user")
        title_lbl.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #111827;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
        """)
        
        # Rich Text Description highlighting the User ID tag
        desc_lbl = QLabel(
            f"Are you sure you want to permanently delete User ID "
            f"<span style='background-color: #fee2e2; color: #b91c1c; font-family: monospace; font-size: 12px; font-weight: bold; border-radius: 4px;'>&nbsp;{user_id}&nbsp;</span> "
            f"from the system database? This action cannot be undone."
        )
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #4b5563;
                line-height: 1.6;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
        """)
        
        text_layout.addWidget(title_lbl)
        text_layout.addWidget(desc_lbl)
        
        header_layout.addWidget(icon_lbl)
        header_layout.addLayout(text_layout)
        
        layout.addLayout(header_layout)
        
        # Bottom Buttons Row
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setFixedSize(85, 32)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #2563eb;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        delete_btn = QPushButton("DELETE")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setFixedSize(100, 32)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        delete_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(delete_btn)
        
        layout.addLayout(btn_layout)
        outer_layout.addWidget(frame)


class CannotDeleteUserDialog(QDialog):
    """Custom warning dialog when user cannot be deleted because they have outstanding rentals."""
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedWidth(520)
        
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(10, 10, 10, 10)
        
        frame = QFrame()
        frame.setObjectName("BlockCard")
        frame.setStyleSheet("""
            QFrame#BlockCard {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-top: 4px solid #f59e0b;
                border-radius: 12px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(17, 24, 39, 25))
        frame.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Header Row Layout
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Info 'i' Circle Icon
        icon_lbl = QLabel("i")
        icon_lbl.setFixedSize(36, 36)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("""
            QLabel {
                background-color: #fef3c7;
                border: 2px solid #fcd34d;
                border-radius: 18px;
                color: #d97706;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Georgia', serif;
            }
        """)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        title_lbl = QLabel("Cannot delete user")
        title_lbl.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #111827;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
        """)
        
        # Rich Text Detail warning matching mockups
        desc_lbl = QLabel(
            f"User ID <span style='background-color: #fef3c7; color: #b45309; font-family: monospace; font-size: 12px; font-weight: bold; border-radius: 4px;'>&nbsp;{user_id}&nbsp;</span> "
            f"cannot be deleted.<br>"
            f"<span style='color: #b45309; font-weight: bold;'>This student currently has an active umbrella rental checked out.</span>"
        )
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #4b5563;
                line-height: 1.6;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
        """)
        
        text_layout.addWidget(title_lbl)
        text_layout.addWidget(desc_lbl)
        
        header_layout.addWidget(icon_lbl)
        header_layout.addLayout(text_layout)
        
        layout.addLayout(header_layout)
        
        # Bottom Buttons Row
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.setFixedSize(85, 32)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #1e3a8a;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)
        outer_layout.addWidget(frame)
