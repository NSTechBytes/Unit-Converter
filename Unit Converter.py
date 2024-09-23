import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox,
    QGridLayout, QMessageBox, QPushButton, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

class UnitConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unit Converter")
        self.setFixedSize(500, 300)  # Fixed window size
        self.setWindowIcon(QIcon('icons\\Unit Converter.png'))  # Set application icon
        self.initUI()

    def initUI(self):
        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Input Section
        input_layout = QHBoxLayout()
        input_label = QLabel("Value:")
        input_label.setFixedWidth(80)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter value to convert")
        self.input_field.textChanged.connect(self.convert)
        
        # Copy Input Button with Icon
        self.copy_input_button = QPushButton()
        self.copy_input_button.setIcon(QIcon('icons\\copy.png'))  # Set copy icon
        self.copy_input_button.setToolTip("Copy input value to clipboard")
        self.copy_input_button.setFixedSize(30, 30)
        self.copy_input_button.clicked.connect(self.copy_input)

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.copy_input_button)

        # Unit Type Selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Unit Type:")
        type_label.setFixedWidth(80)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Length", "Weight", "Temperature", "Volume"])
        self.type_combo.currentIndexChanged.connect(self.update_units)

        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)

        # Source and Target Units
        units_layout = QHBoxLayout()
        source_label = QLabel("From:")
        source_label.setFixedWidth(80)
        self.source_combo = QComboBox()

        target_label = QLabel("To:")
        target_label.setFixedWidth(80)
        self.target_combo = QComboBox()

        units_layout.addWidget(source_label)
        units_layout.addWidget(self.source_combo)
        units_layout.addSpacing(20)
        units_layout.addWidget(target_label)
        units_layout.addWidget(self.target_combo)

        # Output Section
        output_layout = QHBoxLayout()
        output_label = QLabel("Converted Value:")
        output_label.setFixedWidth(120)
        self.output_field = QLineEdit()
        self.output_field.setReadOnly(True)
        self.output_field.setStyleSheet("background-color: #f0f0f0;")

        # Copy Output Button with Icon
        self.copy_output_button = QPushButton()
        self.copy_output_button.setIcon(QIcon('icons\\copy.png'))  # Set copy icon
        self.copy_output_button.setToolTip("Copy converted value to clipboard")
        self.copy_output_button.setFixedSize(30, 30)
        self.copy_output_button.clicked.connect(self.copy_output)

        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_field)
        output_layout.addWidget(self.copy_output_button)

        # Error Message
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")
        self.error_label.setAlignment(Qt.AlignCenter)

        # Add all layouts to main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(type_layout)
        main_layout.addLayout(units_layout)
        main_layout.addLayout(output_layout)
        main_layout.addWidget(self.error_label)

        self.setLayout(main_layout)

        # Define units
        self.units = {
            "Length": ["meters", "kilometers", "miles", "inches", "feet"],
            "Weight": ["grams", "kilograms", "pounds", "ounces"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Volume": ["liters", "milliliters", "gallons", "cups"]
        }

        # Conversion factors relative to base units
        self.length_factors = {
            "meters": 1,
            "kilometers": 1000,
            "miles": 1609.34,
            "inches": 0.0254,
            "feet": 0.3048
        }

        self.weight_factors = {
            "grams": 1,
            "kilograms": 1000,
            "pounds": 453.592,
            "ounces": 28.3495
        }

        self.volume_factors = {
            "liters": 1,
            "milliliters": 0.001,
            "gallons": 3.78541,
            "cups": 0.24
        }

        # Initialize source and target units
        self.update_units()

        # Apply Stylesheet for Visual Appeal
        self.apply_styles()

    def apply_styles(self):
        """Apply styles to the application for better visual appeal."""
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
                margin: 2px 1px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def update_units(self):
        """Update the source and target unit dropdowns based on selected type."""
        unit_type = self.type_combo.currentText()
        units = self.units.get(unit_type, [])

        # Clear existing items
        self.source_combo.clear()
        self.target_combo.clear()

        # Add new items
        self.source_combo.addItems(units)
        self.target_combo.addItems(units)

        # Perform conversion after updating units
        self.convert()

    def convert(self):
        """Perform unit conversion based on user input and selections."""
        value = self.input_field.text()
        unit_type = self.type_combo.currentText()
        source_unit = self.source_combo.currentText()
        target_unit = self.target_combo.currentText()

        # Clear previous error message
        self.error_label.setText("")

        if not value:
            self.output_field.setText("")
            return

        try:
            # Attempt to convert input to float
            value = float(value)
        except ValueError:
            # Show error if input is not numeric
            self.output_field.setText("")
            self.error_label.setText("Please enter a valid numeric value.")
            return

        try:
            if unit_type == "Length":
                converted_value = self.convert_length(value, source_unit, target_unit)
            elif unit_type == "Weight":
                converted_value = self.convert_weight(value, source_unit, target_unit)
            elif unit_type == "Temperature":
                converted_value = self.convert_temperature(value, source_unit, target_unit)
            elif unit_type == "Volume":
                converted_value = self.convert_volume(value, source_unit, target_unit)
            else:
                converted_value = "N/A"

            self.output_field.setText(f"{converted_value:.4f}")
        except Exception as e:
            # Catch any unexpected errors
            self.output_field.setText("")
            self.error_label.setText("Error in conversion.")

    def convert_length(self, value, from_unit, to_unit):
        """Convert length units."""
        # Convert from source to meters
        meters = value * self.length_factors[from_unit]
        # Convert meters to target unit
        return meters / self.length_factors[to_unit]

    def convert_weight(self, value, from_unit, to_unit):
        """Convert weight units."""
        # Convert from source to grams
        grams = value * self.weight_factors[from_unit]
        # Convert grams to target unit
        return grams / self.weight_factors[to_unit]

    def convert_volume(self, value, from_unit, to_unit):
        """Convert volume units."""
        # Convert from source to liters
        liters = value * self.volume_factors[from_unit]
        # Convert liters to target unit
        return liters / self.volume_factors[to_unit]

    def convert_temperature(self, value, from_unit, to_unit):
        """Convert temperature units."""
        # First, convert from source to Celsius
        if from_unit == "Celsius":
            celsius = value
        elif from_unit == "Fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "Kelvin":
            celsius = value - 273.15
        else:
            raise ValueError("Unsupported temperature unit.")

        # Then, convert from Celsius to target unit
        if to_unit == "Celsius":
            return celsius
        elif to_unit == "Fahrenheit":
            return (celsius * 9/5) + 32
        elif to_unit == "Kelvin":
            return celsius + 273.15
        else:
            raise ValueError("Unsupported temperature unit.")

    def copy_input(self):
        """Copy the input value to the clipboard."""
        input_text = self.input_field.text()
        if input_text:
            clipboard = QApplication.clipboard()
            clipboard.setText(input_text)
            self.show_message("Input value copied to clipboard.")

    def copy_output(self):
        """Copy the converted value to the clipboard."""
        output_text = self.output_field.text()
        if output_text:
            clipboard = QApplication.clipboard()
            clipboard.setText(output_text)
            self.show_message("Converted value copied to clipboard.")

    def show_message(self, message):
        """Display a temporary message box."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    converter = UnitConverter()
    converter.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
