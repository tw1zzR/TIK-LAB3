import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from calculate_methods import calculate_entropies


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.H_a_label = QLabel(self)
        self.H_b_label = QLabel(self)
        self.H_ab_label = QLabel(self)
        self.H_b_to_a_label = QLabel(self)
        self.H_a_to_b_label = QLabel(self)
        self.H_b_to_a_and_a_to_b_label = QLabel(self)

        self.input_text = QTextEdit(self)
        self.calculate_btn = QPushButton("CALCULATE", self)

        self.labels = [self.H_a_label, self.H_b_label, self.H_ab_label,
                       self.H_b_to_a_label, self.H_a_to_b_label, self.H_b_to_a_and_a_to_b_label]

        self.layout = QVBoxLayout()
        self.container = QWidget()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Entropy Calculator")
        self.setGeometry(1000, 500, 500, 600)
        self.setWindowIcon(QIcon("icon.png"))

        self.input_text.setPlaceholderText("Enter matrix rows separated by newlines, values separated by spaces.\nExample:\n0 0.24 0.26\n0.01 0.05 0.14\n0.14 0.1 0.06")
        self.input_text.setFixedHeight(150)

        self.calculate_btn.clicked.connect(self.calculate_and_display)
        self.calculate_btn.setFixedHeight(50)

        self.layout.addWidget(self.input_text)

        for label_result in self.labels:
            self.layout.addWidget(label_result, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.calculate_btn)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                font-family: Arial;
            }
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                font-family: Arial;
                background-color: rgb(95, 237, 107);
                border: 2px solid rgb(62, 130, 68);
            }
            QMainWindow {
                font-size: 16px;
                font-weight: bold;
                font-family: Arial;
                background-color: rgb(197, 201, 198);
            }
            QTextEdit {
                font-size: 14px;
                font-family: Arial;
            }
        """)

    def calculate_and_display(self):
        try:
            p_ab = self.get_matrix_from_input()
            results = calculate_entropies(p_ab)

            for label, (key, value) in zip(self.labels, results.items()):
                label.setText(f"{key}: {value:.4f}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid input.\n{str(e)}")

    def get_matrix_from_input(self):
        text = self.input_text.toPlainText().strip()
        lines = text.splitlines()

        if not lines:
            raise ValueError("Input is empty.")

        matrix = []
        for line in lines:
            values = [float(val) for val in line.strip().split()]
            matrix.append(values)

        num_cols = len(matrix[0])
        if any(len(row) != num_cols for row in matrix):
            raise ValueError("Matrix rows must have the same number of values.")

        return np.array(matrix)