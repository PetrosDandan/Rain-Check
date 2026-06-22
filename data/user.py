import sqlite3
import re
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

def add_subtle_shadow(widget):
    import PyQt6.QtWidgets as QW
    shadow = QW.QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)
    shadow.setXOffset(0)
    shadow.setYOffset(2)
    shadow.setColor(QColor(17, 24, 39, 15))
    widget.setGraphicsEffect(shadow)

class UsersTab(QWidget):
    """Clean widget grouping student user registries with a quick search filters panel."""
    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f3f4f6;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Control Row Card
        control_card = QFrame()
        control_card.setObjectName("ControlCard")
        control_card.setStyleSheet("""
            QFrame#ControlCard {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
        """)
        ctl_layout = QHBoxLayout(control_card)
        ctl_layout.setContentsMargins(16, 16, 16, 16)
        ctl_layout.setSpacing(10)

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search student ID, name or RFID...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                min-width: 250px;
            }
            QLineEdit:focus {
                border: 1px solid #11224d;
            }
        """)
        self.search_input.textChanged.connect(self.load_users)

        # Add Student Button
        self.add_btn = QPushButton("Register New Student")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #11224d;
                color: #ffffff;
                border: none;
                padding: 8px 18px;
                font-weight: bold;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1a3066;
            }
        """)
        self.add_btn.clicked.connect(self.add_student)

        ctl_layout.addWidget(self.search_input)
        ctl_layout.addStretch()
        ctl_layout.addWidget(self.add_btn)
        add_subtle_shadow(control_card)
        layout.addWidget(control_card)

        # Table title
        table_lbl = QLabel("STUDENT & STAFF REGISTRIES")
        table_lbl.setStyleSheet("color: #111827; font-weight: bold; font-size: 11px; letter-spacing: 0.5px; margin-top: 5px;")
        layout.addWidget(table_lbl)

        # Users Table (Expanded to 6 columns for Action Buttons)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Student / User ID", "First Name", "Last Name", "M.I.", "RFID UID", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Give the action column a fixed size so it stays compact
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 50)  # Shrinks M.I. down to only 50 pixels wide
        
        # 3. Secure clean spacing for the inventory style Action buttons (index 5)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 140)
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                color: #111827;
                gridline-color: #f3f4f6;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #f9fafb;
                color: #4b5563;
                padding: 8px;
                border: 1px solid #e5e7eb;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.table)
        self.load_users()

    def load_users(self):
        query_str = self.search_input.text().strip()
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if query_str:
                cursor.execute("""
                    SELECT user_id, first_name, last_name, m_i, rfid_uid 
                    FROM USER 
                    WHERE user_id LIKE ? OR first_name LIKE ? OR last_name LIKE ? OR rfid_uid LIKE ?
                    ORDER BY user_id ASC
                """, (f"%{query_str}%", f"%{query_str}%", f"%{query_str}%", f"%{query_str}%"))
            else:
                cursor.execute("SELECT user_id, first_name, last_name, m_i, rfid_uid FROM USER ORDER BY user_id ASC")
            rows = cursor.fetchall()
            conn.close()

            self.table.setRowCount(0)
            for idx, row in enumerate(rows):
                self.table.insertRow(idx)
                for col_idx, val in enumerate(row):
                    item = QTableWidgetItem(str(val) if val else "")
                    item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                    if col_idx in [0, 3, 4]:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        if col_idx == 0:
                            item.setForeground(QColor("#11224d"))
                    self.table.setItem(idx, col_idx, item)
                
                # --- ACTIONS Widget (Edit/Delete buttons nicely grouped like the inventory tab) ---
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(6, 2, 6, 2)
                actions_layout.setSpacing(10)
                actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Green Tinted Edit Button
                edit_btn = QPushButton("✏ Edit")
                edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ecfdf5;
                        color: #047857;
                        border: 1px solid #a7f3d0;
                        border-radius: 4px;
                        font-size: 10px;
                        padding: 3px 8px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #34d399;
                        color: #ffffff;
                    }
                """)
                edit_btn.clicked.connect(lambda checked, r=row: self.edit_student(r))
                
                # Red Tinted Delete Button
                del_btn = QPushButton("🗑 Delete")
                del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                del_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #fef2f2;
                        color: #b91c1c;
                        border: 1px solid #fecaca;
                        border-radius: 4px;
                        font-size: 10px;
                        padding: 3px 8px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #ef4444;
                        color: #ffffff;
                    }
                """)
                del_btn.clicked.connect(lambda checked, uid=row[0]: self.delete_student(uid))
                
                actions_layout.addWidget(edit_btn)
                actions_layout.addWidget(del_btn)
                
                # Places it in column index 5 (the "Actions" header column)
                self.table.setCellWidget(idx, 5, actions_widget)
                
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to retrieve user registry: {e}")

    def add_student(self):
        dialog = StudentRegistrationDialog(self.db_path, parent=self)
        if dialog.exec():
            self.load_users()

    def edit_student(self, user_data):
        # Open dialog in edit mode passing the existing row tuple data
        dialog = StudentRegistrationDialog(self.db_path, edit_user_data=user_data, parent=self)
        if dialog.exec():
            self.load_users()

    def delete_student(self, user_id):
        confirm = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to permanently delete Student ID {user_id} from the system database?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM USER WHERE user_id = ?", (user_id,))
                conn.commit()
                conn.close()
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to remove user: {e}")


class StudentRegistrationDialog(QDialog):
    """Custom registration dialog supporting both creation and non-RFID modification modes."""
    def __init__(self, db_path, edit_user_data=None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.edit_user_data = edit_user_data # Tuple structure if editing: (user_id, first_name, last_name, m_i, rfid_uid)
        self.is_edit_mode = edit_user_data is not None
        self.rfid_uid = edit_user_data[4] if self.is_edit_mode else ""
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Edit Student Profile" if self.is_edit_mode else "Register New Student")
        self.setFixedWidth(460)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- HEADER CARD PANEL ---
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #11224d;
                border: none;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 18, 20, 18)
        header_layout.setSpacing(14)
        
        icon_badge = QLabel()
        icon_badge.setFixedSize(44, 44)
        icon_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_badge.setStyleSheet("""
            QLabel {
                background-color: #f59e0b;
                border-radius: 8px;
                font-size: 22px;
                color: #ffffff;
                font-weight: bold;
                border: none;
            }
        """)
        icon_badge.setText("👤")
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title_lbl = QLabel("Edit student profile" if self.is_edit_mode else "Register new student")
        title_lbl.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        subtitle_lbl = QLabel("Raincheck | Umbrella Rental System")
        subtitle_lbl.setStyleSheet("""
            QLabel {
                color: #8da2cf;
                font-size: 11px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        title_layout.addWidget(title_lbl)
        title_layout.addWidget(subtitle_lbl)
        
        header_layout.addWidget(icon_badge)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        main_layout.addWidget(header_frame)
        
        # --- BODY FORM WRAPPER ---
        body_frame = QFrame()
        body_frame.setStyleSheet("QFrame { background-color: #ffffff; border: none; }")
        body_layout = QVBoxLayout(body_frame)
        body_layout.setContentsMargins(24, 24, 24, 24)
        body_layout.setSpacing(18)
        
        # 1. Student ID layout
        id_layout = QVBoxLayout()
        id_layout.setSpacing(6)
        id_lbl = QLabel("STUDENT ID")
        id_lbl.setStyleSheet("QLabel { color: #6b7280; font-size: 10px; font-weight: bold; letter-spacing: 0.8px; }")
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("e.g. 2021-0008")
        self.id_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 10px 12px;
                font-size: 13px;
            }
            QLineEdit:focus { border: 2px solid #11224d; }
            QLineEdit:disabled { background-color: #f3f4f6; color: #6b7280; }
        """)
        if self.is_edit_mode:
            self.id_input.setText(self.edit_user_data[0])
            self.id_input.setEnabled(False)  # Lock primary key ID modification during alterations
            
        id_layout.addWidget(id_lbl)
        id_layout.addWidget(self.id_input)
        body_layout.addLayout(id_layout)
        
        # 2. Names row (First Name, Last Name, Middle Initial)
        names_layout = QHBoxLayout()
        names_layout.setSpacing(12)
        
        # First Name
        fn_layout = QVBoxLayout()
        fn_layout.setSpacing(6)
        fn_lbl = QLabel("FIRST NAME")
        fn_lbl.setStyleSheet("QLabel { color: #6b7280; font-size: 10px; font-weight: bold; letter-spacing: 0.8px; }")
        self.fn_input = QLineEdit()
        self.fn_input.setPlaceholderText("Maria")
        self.fn_input.setStyleSheet("QLineEdit { background-color: #ffffff; color: #111827; border: 1px solid #d1d5db; border-radius: 6px; padding: 10px 12px; font-size: 13px; } QLineEdit:focus { border: 2px solid #11224d; }")
        if self.is_edit_mode:
            self.fn_input.setText(self.edit_user_data[1])
        fn_layout.addWidget(fn_lbl)
        fn_layout.addWidget(self.fn_input)
        
        # Last Name
        ln_layout = QVBoxLayout()
        ln_layout.setSpacing(6)
        ln_lbl = QLabel("LAST NAME")
        ln_lbl.setStyleSheet("QLabel { color: #6b7280; font-size: 10px; font-weight: bold; letter-spacing: 0.8px; }")
        self.ln_input = QLineEdit()
        self.ln_input.setPlaceholderText("Reyes")
        self.ln_input.setStyleSheet("QLineEdit { background-color: #ffffff; color: #111827; border: 1px solid #d1d5db; border-radius: 6px; padding: 10px 12px; font-size: 13px; } QLineEdit:focus { border: 2px solid #11224d; }")
        if self.is_edit_mode:
            self.ln_input.setText(self.edit_user_data[2])
        ln_layout.addWidget(ln_lbl)
        ln_layout.addWidget(self.ln_input)
        
        # Middle Initial
        mi_layout = QVBoxLayout()
        mi_layout.setSpacing(6)
        mi_lbl = QLabel("MIDDLE INITIAL")
        mi_lbl.setStyleSheet("QLabel { color: #6b7280; font-size: 10px; font-weight: bold; letter-spacing: 0.8px; }")
        self.mi_input = QLineEdit()
        self.mi_input.setPlaceholderText("C.")
        self.mi_input.setStyleSheet("QLineEdit { background-color: #ffffff; color: #111827; border: 1px solid #d1d5db; border-radius: 6px; padding: 10px 12px; font-size: 13px; } QLineEdit:focus { border: 2px solid #11224d; }")
        if self.is_edit_mode and self.edit_user_data[3]:
            self.mi_input.setText(self.edit_user_data[3])
        mi_layout.addWidget(mi_lbl)
        mi_layout.addWidget(self.mi_input)
        
        names_layout.addLayout(fn_layout, 4)
        names_layout.addLayout(ln_layout, 4)
        names_layout.addLayout(mi_layout, 2)
        body_layout.addLayout(names_layout)
        
        # 3. Interactive RFID Card Enrollment Container (HIDDEN IN EDIT MODE)
        self.rfid_container = QFrame()
        self.rfid_container.setCursor(Qt.CursorShape.PointingHandCursor)
        self.rfid_container.setObjectName("RfidContainer")
        
        rfid_layout = QVBoxLayout(self.rfid_container)
        rfid_layout.setContentsMargins(18, 16, 18, 16)
        rfid_layout.setSpacing(12)
        
        self.signal_lbl = QLabel()
        self.signal_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_content_layout = QHBoxLayout()
        inner_content_layout.setSpacing(14)
        self.card_icon_badge = QLabel()
        self.card_icon_badge.setFixedSize(40, 40)
        self.card_icon_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        self.action_title_lbl = QLabel()
        self.action_desc_lbl = QLabel()
        text_layout.addWidget(self.action_title_lbl)
        text_layout.addWidget(self.action_desc_lbl)
        
        inner_content_layout.addWidget(self.card_icon_badge)
        inner_content_layout.addLayout(text_layout)
        inner_content_layout.addStretch()
        rfid_layout.addWidget(self.signal_lbl)
        rfid_layout.addLayout(inner_content_layout)
        body_layout.addWidget(self.rfid_container)
        
        self.rfid_container.mousePressEvent = self.simulate_rfid_scan
        self.update_rfid_ui()
        
        if self.is_edit_mode:
            self.rfid_container.hide() # Directly hide the RFID layout row if editing profile details
        
        # 4. Action Buttons row
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        buttons_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setStyleSheet("QPushButton { background-color: #ffffff; color: #11224d; border: 1px solid #11224d; border-radius: 6px; padding: 10px 24px; font-weight: bold; font-size: 13px; min-width: 80px; } QPushButton:hover { background-color: #f3f4f6; }")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet("QPushButton { background-color: #11224d; color: #ffffff; border: none; border-radius: 6px; padding: 10px 24px; font-weight: bold; font-size: 13px; min-width: 100px; } QPushButton:hover { background-color: #1c326b; }")
        self.save_btn.clicked.connect(self.save)
        
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)
        body_layout.addLayout(buttons_layout)
        
        main_layout.addWidget(body_frame)

    def update_rfid_ui(self):
        if not self.rfid_uid:
            self.rfid_container.setStyleSheet("QFrame#RfidContainer { background-color: #eff6ff; border: 2px dashed #3b82f6; border-radius: 8px; }")
            self.signal_lbl.setText("RFID CARD ENROLLMENT")
            self.signal_lbl.setStyleSheet("color: #2563eb; font-weight: bold; font-size: 11px;")
            self.card_icon_badge.setStyleSheet("QLabel { background-color: #dbeafe; color: #2563eb; font-size: 20px; border-radius: 6px; border: none; }")
            self.card_icon_badge.setText("💳")
            self.action_title_lbl.setText("Tap ID card on scanner now")
            self.action_title_lbl.setStyleSheet("color: #1e40af; font-weight: bold; font-size: 13px;")
            self.action_desc_lbl.setText("Hold card flat against the reader until confirmed")
            self.action_desc_lbl.setStyleSheet("color: #3b82f6; font-size: 11px;")
        else:
            self.rfid_container.setStyleSheet("QFrame#RfidContainer { background-color: #ecfdf5; border: 2px dashed #10b981; border-radius: 8px; }")
            self.signal_lbl.setText("CARD READ SUCCESSFULLY")
            self.signal_lbl.setStyleSheet("color: #059669; font-weight: bold; font-size: 11px;")
            self.card_icon_badge.setStyleSheet("QLabel { background-color: #d1fae5; color: #059669; font-size: 20px; border-radius: 6px; border: none; }")
            self.card_icon_badge.setText("💳")
            self.action_title_lbl.setText("Card detected - UID captured")
            self.action_title_lbl.setStyleSheet("color: #065f46; font-weight: bold; font-size: 13px;")
            self.action_desc_lbl.setText(f"RFID UID linked: {self.rfid_uid}")
            self.action_desc_lbl.setStyleSheet("color: #059669; font-size: 11px;")

    def simulate_rfid_scan(self, event):
        import random
        bytes_array = [f"{random.randint(0, 255):02X}" for _ in range(4)]
        self.rfid_uid = "-".join(bytes_array)
        self.update_rfid_ui()

    def save(self):
        uid = self.id_input.text().strip()
        fn = self.fn_input.text().strip()
        ln = self.ln_input.text().strip()
        mi = self.mi_input.text().strip()
        
        # --- 1. STUDENT ID RANGE VALIDATIONS (Skip checks if in edit mode since ID is locked) ---
        if not self.is_edit_mode:
            id_match = re.match(r"^(\d+)-(\d+)$", uid)
            if not id_match:
                QMessageBox.warning(self, "Validation Error", "Please provide a valid Student ID in YYYY-XXXX format (e.g., 2021-0008).")
                return
            year_val = int(id_match.group(1))
            num_val = int(id_match.group(2))
            if not (2021 <= year_val <= 2026) or not (1 <= num_val <= 3000):
                QMessageBox.warning(self, "Validation Error", "Student ID constraints violated:\n- Year part must be between 2021 and 2026.\n- Id part must be between 0001 and 3000.")
                return
            uid = f"{year_val}-{num_val:04d}"

        # --- 2. NAMES VALIDATION & AUTO-CASE ---
        if not fn or not fn.replace(" ", "").isalpha():
            QMessageBox.warning(self, "Validation Error", "First Name is required and must only contain alphabet letters.")
            return
        if not ln or not ln.replace(" ", "").isalpha():
            QMessageBox.warning(self, "Validation Error", "Last Name is required and must only contain alphabet letters.")
            return
            
        fn = fn.capitalize()
        ln = ln.capitalize()

        # --- 3. MIDDLE INITIAL AUTO-CASE ---
        if mi:
            mi_clean = mi.rstrip('.')
            if len(mi_clean) != 1 or not mi_clean.isalpha():
                QMessageBox.warning(self, "Validation Error", "Middle Initial must be a single letter or left blank.")
                return
            mi = mi_clean.upper() + "."
        else:
            mi = ""
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if self.is_edit_mode:
                # Update details for an existing user row
                cursor.execute("""
                    UPDATE USER 
                    SET first_name = ?, last_name = ?, m_i = ? 
                    WHERE user_id = ?
                """, (fn, ln, mi, uid))
            else:
                # Unique constraints checks for an addition creation workflow
                cursor.execute("SELECT user_id FROM USER WHERE user_id = ?", (uid,))
                if cursor.fetchone():
                    QMessageBox.warning(self, "Duplicate Student ID", f"The Student ID '{uid}' is already registered.")
                    conn.close()
                    return
                    
                cursor.execute("SELECT user_id FROM USER WHERE rfid_uid = ?", (self.rfid_uid,))
                if cursor.fetchone():
                    QMessageBox.warning(self, "Duplicate RFID", "The scanned RFID tag is already enrolled.")
                    conn.close()
                    return
                    
                cursor.execute("""
                    INSERT INTO USER (user_id, first_name, last_name, m_i, rfid_uid)
                    VALUES (?, ?, ?, ?, ?)
                """, (uid, fn, ln, mi, self.rfid_uid))
                
            conn.commit()
            conn.close()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save record: {e}")