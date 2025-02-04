from libraries import *
from paths import *
# Path to the invoice templates (replace your invoice templates in the templates file)
def resource_path(relative_path):

    try:
       
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# main invoice generator application

class InvoiceApp(QtWidgets.QWidget):

    def __init__(self, invoice_template, template_name):
        super().__init__()
        self.template_path = invoice_template
        self.template = Image.open(self.template_path)
        self.template_name = template_name
        self.connection = self.get_database_connection()

        if self.connection:
            self.invoice_number = self.get_next_invoice_number_1()
        self.initUI()

    def get_database_connection(self):
        """ Establishes a connection to the SQL Server database. """
        try:
            connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER= "your server name";'  # Update this 
                'DATABASE="your databse name";'    # The name of your database
                'Trusted_Connection=yes;' 
            )
            return connection
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", str(e))
            return None
    def add_invoice_to_db(self, details , details_2):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO invoices (invoice_number, seller) VALUES (?,?)",
                (self.invoice_number, details_2)
            )
            self.connection.commit()
            cursor.close()
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", str(e))
            print(f"Database Error: {e}")


        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", str(e))
            print(f"Database Error: {e}")

    def get_next_invoice_number_1(self):

        try:
            cursor = self.connection.cursor()
        
        # Fetch the max invoice number and increment by 1
            cursor.execute("SELECT COALESCE(MAX(invoice_number), 0) + 1 FROM invoices")
            result = cursor.fetchone()
            next_invoice_number = result[0] if result else 1
        
            return next_invoice_number
    
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", str(e))
            return None
    
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Exception Occurred", str(e))
            return None

        finally:
            cursor.close()


    def get_jalali_date(self):
        """ Returns the current date in Jalali (Shamsi) format. """
        current_date = datetime.now()
        jalali_date = JalaliDate(current_date)
        return jalali_date.isoformat()

    def set_jalali_date(self):
        """ Sets the Jalali date in QLineEdit for display. """
        self.date_line_edit.setText(self.get_jalali_date())

    def initUI(self):
        self.setWindowTitle("تولید کننده فاکتور - " + self.template_name)
        self.layout = QVBoxLayout()
        self.resize(559, 794)
        self.setStyleSheet("background-color: #FFFDFE;")

        # Customer Details
        customer_frame = QGroupBox()
        customer_layout = QVBoxLayout()

        logo_label = QLabel(self)
        logo_path = os.path.join(base_dir, 'assets', 'your logo path in the assets folder') # update this 
        pixmap = QPixmap(logo_path)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(QtCore.Qt.AlignCenter)

        # Add some offset from the top
        self.layout.addSpacing(20)  # Offset from top
        self.layout.addWidget(logo_label)

        customer_grid = QGridLayout()

        # Customer Name
        customer_name_label = QLabel("نام خریدار:")
        self.customer_name = QLineEdit()
        customer_name_label.setAlignment(QtCore.Qt.AlignLeft)
        self.customer_name.setAlignment(QtCore.Qt.AlignLeft)
        customer_grid.addWidget(customer_name_label, 0, 6)
        customer_grid.addWidget(self.customer_name, 0, 5)


        seller_name_label = QLabel("نام فروشنده")
        self.seller = QLineEdit()
        seller_name_label.setAlignment(QtCore.Qt.AlignLeft)
        self.seller.setAlignment(QtCore.Qt.AlignLeft)
        customer_grid.addWidget(seller_name_label, 0, 2)
        customer_grid.addWidget(self.seller, 0, 1)


        # National ID
        national_id_label = QLabel("کد ملی خریدار:")
        self.customer_id = QLineEdit()
        national_id_label.setAlignment(QtCore.Qt.AlignLeft)
        self.customer_id.setAlignment(QtCore.Qt.AlignLeft)
        customer_grid.addWidget(national_id_label, 1, 6)
        customer_grid.addWidget(self.customer_id, 1, 3, 1, 3)

        customer_layout.addLayout(customer_grid)
        customer_frame.setLayout(customer_layout)
        self.layout.addWidget(customer_frame)

        # Date with Shamsi (Jalali) Calendar
        date_label = QLabel("تاریخ:")
        self.date_line_edit = QLineEdit()
        self.date_line_edit.setReadOnly(True)
        self.set_jalali_date()
        date_label.setAlignment(QtCore.Qt.AlignRight)
        customer_grid.addWidget(date_label, 1, 3)
        customer_grid.addWidget(self.date_line_edit, 1, 2, 1, 1)

        customer_layout.addLayout(customer_grid)
        customer_frame.setLayout(customer_layout)
        self.layout.addWidget(customer_frame)
        
        # Item Details
        items_frame = QGroupBox("جزئیات کالا")
        items_layout = QVBoxLayout()

        self.items_area = QScrollArea()
        self.items_area.setWidgetResizable(True)
        self.items_container = QFrame()
        self.items_layout = QVBoxLayout()

        self.add_item_button = QPushButton("اضافه کردن کالا")
        if self.template_name == "طلا":
            self.add_item_button.clicked.connect(self.add_item_2)
        else:
            self.add_item_button.clicked.connect(self.add_item)
        items_layout.addWidget(self.add_item_button)
        items_layout.addWidget(self.items_area)

        self.items_container.setLayout(self.items_layout)
        self.items_area.setWidget(self.items_container)
        items_frame.setLayout(items_layout)
        self.layout.addWidget(items_frame)

    # Generate Button
        self.generate_button = QPushButton("تولید فاکتور")
        self.generate_button.clicked.connect(self.generate_invoice)
        self.layout.addWidget(self.generate_button)

        # Set Layout
        self.setLayout(self.layout)
    def generate_invoice(self):
        details , details_3 = self.get_invoice_details()
        details_2 , details_4 = self.get_invoice_details_2()
    # Call the appropriate fill_template function based on the template
        if self.template_name == "طلا":
            filled_invoice = self.fill_template_gold(details_2, self.invoice_number)

        else:
            filled_invoice = self.fill_template(details, self.invoice_number)
        if self.template_name == "طلا":
            self.add_invoice_to_db(details_2,details_4)

        else:
            self.add_invoice_to_db(details,details_3)

        self.save_invoice(filled_invoice, self.invoice_number)
            # Add the invoice information to the database

    #  show a success message or any post-process actions
        QtWidgets.QMessageBox.information(self, "موفقیت", f"فاکتور با شماره {self.invoice_number} با موفقیت تولید شد.")
        self.close()
        home = HomePage()
        home.show()
    def add_item(self):
        item_frame = QFrame()
        item_layout = QVBoxLayout()

        # Common item fields
        item_fields = [
            ("کد جنس", QLineEdit()),
            ("نوع جنس:", QLineEdit()),
            ("وزن طلا:", QLineEdit()),
            ("قیمت:", QLineEdit()),
            ("شرح سنگ", QLineEdit()),
            ("توضیحات", QLineEdit()),
            ("مبلغ قابل پرداخت", QLineEdit())
        ]

        for label, widget in item_fields:
            item_layout.addLayout(self.create_hbox(label, widget))

        item_frame.setLayout(item_layout)
        self.items_layout.addWidget(item_frame)



    def add_item_2(self):
        item_frame = QFrame()
        item_layout = QVBoxLayout()

        # Common item fields
        item_fields = [
            ("نوع جنس:", QLineEdit()),
            ("وزن", QLineEdit()),
            ("قیمت:", QLineEdit()),
            ("قیمت هر گرم", QLineEdit()),
            ("توضیحات", QLineEdit()),
            ("مبلغ قابل پرداخت", QLineEdit())
            
        ]

        for label, widget in item_fields:
            item_layout.addLayout(self.create_hbox(label, widget))

        item_frame.setLayout(item_layout)
        self.items_layout.addWidget(item_frame)



    def create_hbox(self, label_text, widget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(QtCore.Qt.AlignRight)
        widget.setAlignment(QtCore.Qt.AlignRight)
        layout.addWidget(widget)
        layout.addWidget(label)
        return layout

    def get_invoice_details(self):
        details = {
            "customer_name": self.customer_name.text() or '_',
            "customer_id": self.customer_id.text() if hasattr(self, 'customer_id') else '_',
            "date": self.date_line_edit.text() or '_',
            "items": []
        }
        details_3 = self.seller.text()

        for i in range(self.items_layout.count()):
            item_frame = self.items_layout.itemAt(i).widget()
            item_details = {}
        
            for j in range(item_frame.layout().count()):
                layout = item_frame.layout().itemAt(j).layout()
                if layout.count() == 2:
                    widget = layout.itemAt(0).widget()
                    label = layout.itemAt(1).widget().text()
                    value = widget.text() or '_'  # Set default to underscore if the value is empty
                
                # Populate item_details with values or underscores
                    if label == "کد جنس":
                        item_details["item_code"] = value
                    elif label == "نوع جنس:":
                        item_details["item_type"] = value
                    elif label == "وزن طلا:":
                        item_details["gold_weight"] = value
                    elif label == "قیمت:":
                        item_details["price"] = value
                    elif label == "شرح سنگ":
                        item_details["stone_description"] = value
                    elif label == "توضیحات":
                        item_details["additional_notes"] = value    
                    elif label == "مبلغ قابل پرداخت":
                        item_details["pricep"] = value                        
        
        # Ensure all item fields that may not be set will default to "_"
            for key in ["item_code", "item_type", "gold_weight", "price", "stone_description", "additional_notes", "pricep"]:
                if key not in item_details or not item_details[key]:
                    item_details[key] = '_'
        
            details["items"].append(item_details)

        return details , details_3

    def get_invoice_details_2(self):
        details_2 = {
            "customer_name": self.customer_name.text() or '_',
            "customer_id": self.customer_id.text() if hasattr(self, 'customer_id') else '_',
            "date": self.date_line_edit.text() or '_',
            "items": []
        }
        details_4 = self.seller.text()

        for i in range(self.items_layout.count()):
            item_frame = self.items_layout.itemAt(i).widget()
            item_details = {}
            
            for j in range(item_frame.layout().count()):
                layout = item_frame.layout().itemAt(j).layout()
                if layout.count() == 2:  # Ensure there are 2 elements
                    widget = layout.itemAt(0).widget()
                    label_widget = layout.itemAt(1).widget()

                    if widget and label_widget:  # Ensure both widgets exist
                        label = label_widget.text()
                        value = widget.text() or '_'  # Set to underscore if empty
                    else:
                        continue  # Skip if the required widgets are not available

                    # Populate item_details with values or underscores
                    if label == "نوع جنس:":
                        item_details["item_type"] = value
                    elif label == "وزن":
                        item_details["gold_weight"] = value
                    elif label == "قیمت:":
                        item_details["price"] = value
                    elif label == "قیمت هر گرم":
                        item_details["stone_description"] = value
                    elif label == "توضیحات":
                        item_details["additional_notes"] = value
                    elif label == "مبلغ قابل پرداخت":
                        item_details["pricep"] = value
            
            # Provide default values for any missing fields in item_details
            for key in ["item_type", "gold_weight", "price", "stone_description", "additional_notes", "pricep"]:
                if key not in item_details or not item_details[key]:
                    item_details[key] = '_'
            
            details_2["items"].append(item_details)

        return details_2 , details_4











    def fill_template(self, details, invoice_number):
        # Create the PDF canvas
        pdf_file_name = f"invoice_{invoice_number}.pdf"
        c = canvas.Canvas(os.path.join(output_dir, f"invoice_{invoice_number}.pdf"), pagesize=A4)
        c.setFont("Arial", 14)  # Set the font and size

        # Reshape and display required text
        reshaped_texts = {
            "customer_name": arabic_reshaper.reshape(details["customer_name"]),
            "customer_id": arabic_reshaper.reshape(details["customer_id"]),
            "date": arabic_reshaper.reshape(details["date"]),
            "invoice_number": str(invoice_number),
        }

        bidi_texts = {key: get_display(text) for key, text in reshaped_texts.items()}
        positions = {
                "customer_name": (470, 619),
                "customer_id": (470, 594),
                "date": (110, 590),
                "invoice_number": (110, 615),
        }

        # Write the main details to PDF
        for key in positions:
            x, y = positions[key]
            text_width = pdfmetrics.stringWidth(bidi_texts[key], "Arial", 12)
            text = c.beginText()
            text.setTextOrigin(x - text_width, y)  # Adjust x position for left-to-right alignment
            text.textLine(bidi_texts[key])
            c.drawText(text)

        # Item listing
        item_y_start = 502
        for item in details["items"]:
            for text, x in zip(
                [item["item_code"], item["item_type"], item["gold_weight"], item["price"]],
                [538, 360, 205, 90],
            ):
                reshaped_text = arabic_reshaper.reshape(text)
                bidi_text = get_display(reshaped_text)
                text_width = pdfmetrics.stringWidth(bidi_text, "Arial", 12)
                text_obj = c.beginText()
                text_obj.setTextOrigin(x - text_width, item_y_start)  # Adjust x position for left-to-right alignment
                text_obj.textLine(bidi_text)
                c.drawText(text_obj)
            item_y_start += 28  # Adjust based on font size and spacing

        # Additional notes
        reshaped_text_8 = arabic_reshaper.reshape(details["items"][0]["stone_description"])
        reshaped_text_9 = arabic_reshaper.reshape(details["items"][0]["additional_notes"])
        bidi_text_8 = get_display(reshaped_text_8)
        bidi_text_9 = get_display(reshaped_text_9)

        text_width_8 = pdfmetrics.stringWidth(bidi_text_8, "Arial", 12)
        text_8 = c.beginText()
        text_8.setTextOrigin(490 - text_width_8, 417)  # Adjust x position for left-to-right alignment
        text_8.textLine(bidi_text_8)
        c.drawText(text_8)

        text_width_9 = pdfmetrics.stringWidth(bidi_text_9, "Arial", 12)
        text_9 = c.beginText()
        text_9.setTextOrigin(490 - text_width_9, 364)  # Adjust x position for left-to-right alignment
        text_9.textLine(bidi_text_9)
        c.drawText(text_9)

        c.drawString( 370, 271 , details["items"][0]["pricep"])

        c.save()

        return c


    def fill_template_gold(self, details_2, invoice_number):
        # Create the PDF canvas
        pdf_file_name = f"invoice_{invoice_number}.pdf"
        c = canvas.Canvas(os.path.join(output_dir, pdf_file_name), pagesize= A5)
        c.setFont("Arial", 12)  # Set the font and size


        # Reshape and display required text
        reshaped_texts = {
            "customer_name": arabic_reshaper.reshape(details_2["customer_name"]),
            "customer_id": arabic_reshaper.reshape(details_2["customer_id"]),
            "date": arabic_reshaper.reshape(details_2["date"]),
            "invoice_number": str(invoice_number),
        }

        bidi_texts = {key: get_display(text) for key, text in reshaped_texts.items()}
        positions = {
            "customer_name": (330, 435),
            "customer_id": (330, 418),
            "date": (75, 418),
            "invoice_number": (75, 435),
        }

        # Write the main details to PDF
        for key in positions:
            x, y = positions[key]
            text_width = pdfmetrics.stringWidth(bidi_texts[key], "Arial", 12)
            text = c.beginText()
            text.setTextOrigin(x - text_width, y)  # Adjust x position for left-to-right alignment
            text.textLine(bidi_texts[key])
            c.drawText(text)

        # Item listing
        item_y_start = 357
        for item in details_2["items"]:
            for key, x in [
                ('item_type', 300),
                ('gold_weight', 140),
                ('price', 75),
            ]:
                reshaped_text = arabic_reshaper.reshape(item[key])
                bidi_text = get_display(reshaped_text)
                text_width = pdfmetrics.stringWidth(bidi_text, "Arial", 12)
                text_obj = c.beginText()
                text_obj.setTextOrigin(x - text_width, item_y_start)  # Adjust x position for left-to-right alignment
                text_obj.textLine(bidi_text)
                c.drawText(text_obj)

            item_y_start += 22.67  # Increase y position for each new item

        # Additional notes
        i = details_2["items"][0]
        reshaped_text_1 = arabic_reshaper.reshape(i["stone_description"])
        reshaped_text_2 = arabic_reshaper.reshape(i["additional_notes"])
        reshaped_text_3 = arabic_reshaper.reshape(i["pricep"])
        bidi_text_1 = get_display(reshaped_text_1)
        bidi_text_2 = get_display(reshaped_text_2)
        bidi_text_3 = get_display(reshaped_text_3)

        text_width_1 = pdfmetrics.stringWidth(bidi_text_1, "Arial", 12)
        text_1 = c.beginText()
        text_1.setTextOrigin(365 - text_width_1, 197)  # Adjust x position for left-to-right alignment
        text_1.textLine(bidi_text_1)
        c.drawText(text_1)

        text_width_2 = pdfmetrics.stringWidth(bidi_text_2, "Arial", 12)
        text_2 = c.beginText()
        text_2.setTextOrigin(354 - text_width_2, 145)  # Adjust x position for left-to-right alignment
        text_2.textLine(bidi_text_2)
        c.drawText(text_2)

        text_width_3 = pdfmetrics.stringWidth(bidi_text_3, "Arial", 12)
        text_3 = c.beginText()
        text_3.setTextOrigin(170 - text_width_3, 210)  # Adjust x position for left-to-right alignment
        text_3.textLine(bidi_text_3)
        c.drawText(text_3)

        # Write the pricep value

        
        c.save()
        return c



    def save_invoice(self, c, invoice_number):
        output_path = os.path.join(output_dir, f"invoice_{invoice_number}.pdf")
        QtWidgets.QMessageBox.information(self, "موفقیت", f"فاکتور ذخیره شد در {output_path}")

class HomePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("انتخاب قالب فاکتور")
        self.layout = QVBoxLayout()

        self.label = QLabel("لطفا یک قالب فاکتور انتخاب کنید:")
        self.layout.addWidget(self.label)

        self.template_buttons = {}
        for name, path in templates.items():
            button = QPushButton(name)
            button.clicked.connect(lambda checked, p=path, n=name: self.open_invoice_app(p, n))
            self.template_buttons[name] = button
            self.layout.addWidget(button)

        self.setLayout(self.layout)

    def open_invoice_app(self, template_path, template_name):
        self.invoice_app = InvoiceApp(template_path, template_name)
        self.invoice_app.show()
        self.close()
    def show(self):
        super().show()

if __name__ == "__main__":
    app = QApplication([])
    home = HomePage()
    home.show()
    app.exec_()
