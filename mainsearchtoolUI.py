import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QLabel
import json
import subprocess
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QCheckBox, QDateEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QDateEdit
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.companies_data = []
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 700, 600)
        self.setWindowTitle('Project Jobs')

        self.dropdown = QComboBox(self)
        self.dropdown.setGeometry(30, 50, 200, 30)
        self.dropdown.setEditable(True)
        self.dropdown.setPlaceholderText('Enter text...')
        
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.searchCompany)
        self.search_button.setGeometry(30, 100, 200, 30)

        
        # Connect the activated signal to the updateSelectedCompany slot
        self.dropdown.activated[str].connect(self.updateSelectedCompany)

      
        with open('updated_companies.json', 'r') as file:
            companies_data = json.load(file)
            
            company_names = [entry['company'] for entry in companies_data if not entry['excluded_from_search']]
            self.dropdown.addItems(company_names)
            
            filtered_companies = [entry for entry in companies_data if not entry['excluded_from_search']]
            
            num_filtered_companies = len(filtered_companies)
            num_applied = sum(1 for entry in filtered_companies if entry['already_applied'])
            
            self.companies_info_label = QLabel(self)
            self.companies_info_label.setGeometry(30, 450, 600, 30)
            self.companies_info_label.setWordWrap(True)
            self.companies_info_label.setText(f"Included in the search: {num_filtered_companies}\n"
                                            f"Already applied to: {num_applied}")
            
            self.selected_company = None
        
        # Create a QLabel widget to display company description
        self.description_label = QLabel(self)
        self.description_label.setGeometry(30, 200, 600, 60)
        self.description_label.setWordWrap(True)
        
        self.info_label = QLabel(self)
        self.info_label.setGeometry(30, 280, 600, 30)
        self.info_label.setWordWrap(True)
        
        self.exclude_checkbox = QCheckBox('Exclude This Company', self)
        self.exclude_checkbox.setGeometry(30, 320, 200, 30)

        self.applied_checkbox = QCheckBox('Already Applied', self)
        self.applied_checkbox.setGeometry(230, 320, 200, 30)
        self.applied_checkbox.stateChanged.connect(self.toggleAppliedDateInput)

        self.applied_date_input = QDateEdit(self)
        self.applied_date_input.setGeometry(230, 350, 200, 30)
        self.applied_date_input.setCalendarPopup(True)
        self.applied_date_input.setDate(QDate.currentDate())
        self.applied_date_input.setVisible(False)  # Initially hidden
        
        self.save_button = QPushButton('Save Changes', self)
        self.save_button.clicked.connect(self.saveChanges)
        self.save_button.setGeometry(30, 520, 200, 30)
        
        self.website_label = QLabel(self)
        self.website_label.setGeometry(30, 150, 600, 30)
        self.website_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.website_label.setOpenExternalLinks(True)  # Make links clickable

        self.refreshUI()
        
    
    def refreshUI(self):
            with open('updated_companies.json', 'r') as file:
                companies_data = json.load(file)
                for entry in companies_data:
                    if entry['company'] == self.selected_company:
                        
                        excluded = entry['excluded_from_search']
                        applied = entry['already_applied']
                        applied_date = entry['application_date']
                        self.exclude_checkbox.setChecked(excluded)
                        self.applied_checkbox.setChecked(applied)
                        self.applied_date_input.setVisible(applied)
                        if applied_date:
                            applied_date = QDate.fromString(applied_date, Qt.ISODate)
                            self.applied_date_input.setDate(applied_date)
                        break

                # Update filtered and applied counts
                num_filtered_companies = sum(1 for entry in companies_data if not entry['excluded_from_search'])
                num_applied = sum(1 for entry in companies_data if entry['already_applied'])

                # Update companies info label text
                self.companies_info_label.setText(f"Included in the search: {num_filtered_companies}\n"
                                                    f"Already applied to: {num_applied}")
            
    def resetView(self):
        self.exclude_checkbox.setChecked(False)
        self.applied_checkbox.setChecked(False)
        self.applied_date_input.setVisible(False)  # Hide the date input when resetting
        self.applied_date_input.setDate(QDate.currentDate())
        self.description_label.setText("")
        self.info_label.setText("")
        self.selected_company = None  # Reset the selected company to None
        self.dropdown.setCurrentIndex(0)  # Reset the dropdown to the first item
        self.website_label.setText("")
        self.refreshUI() 


    # Slot to update the selected_company variable
    def updateSelectedCompany(self, company):
        self.selected_company = company

    def toggleAppliedDateInput(self, state):
        self.applied_date_input.setVisible(state == Qt.Checked)
    
    def searchCompany(self):
        if self.selected_company:
            print(f"Searching for: {self.selected_company}")
            # Find the selected company in the JSON data
            with open('updated_companies.json', 'r') as file:
                companies_data = json.load(file)
                for entry in companies_data:
                    if entry['company'] == self.selected_company:
                        website_link = entry['Website']
                        website_html = f'<a href="{website_link}">{website_link}</a>'
                        self.website_label.setText(website_html)
                        
                        description = entry['summary']
                        self.description_label.setText(f"{self.selected_company} describe themselves as: {description}")
                        
                        self.info_label.setText(f"Contact information: {entry['Email']}, {entry['Phone']}")
                    
                        break
        if self.applied_checkbox.isChecked():
            applied_date = self.applied_date_input.date().toString(Qt.ISODate)
            # Update JSON with applied status and date
            for entry in companies_data:
                if entry['company'] == self.selected_company:
                    entry['applied'] = True
                    entry['applied_date'] = applied_date
                    break
            with open('updated_companies.json', 'w') as file:
                json.dump(companies_data, file, indent=4)
            print(f"Updated {self.selected_company} with applied status and date")
            
    def saveChanges(self):
        if self.selected_company:
            with open('updated_companies.json', 'r') as file:
                companies_data = json.load(file)
                for entry in companies_data:
                    if entry['company'] == self.selected_company:
                        entry['excluded_from_search'] = self.exclude_checkbox.isChecked()
                        entry['already_applied'] = self.applied_checkbox.isChecked()
                        if self.applied_checkbox.isChecked():
                            applied_date = self.applied_date_input.date().toString(Qt.ISODate)
                            entry['application_date'] = applied_date
                        else:
                            entry['application_date'] = ""
                        break
            with open('updated_companies.json', 'w') as file:
                json.dump(companies_data, file, indent=4)
            print("Changes saved to JSON file.")
        self.resetView()
             
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


