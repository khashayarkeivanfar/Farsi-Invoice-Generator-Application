# Farsi Invoice Generator Application

Farsi Invoice Generator Application is a Python-based application designed to manage and generate Persian Gold/Jewelry store invoices effectively. This project allows users to customize templates, paths, logos, and database settings to fit their specific needs. To ensure Persian fields are set in the right place with the correct format, the `bidi` library and `arabic-reshaper` were used.

## Features

- Generate professional Farsi invoices.
- Customizable templates and logos.
- Configurable paths for running the application and saving invoices.
- Easy database initialization.

## Project Structure

- `InvoiceApp.py`: Main application file. You must initiate the database with your own setup here.
- `libraries.py`: Contains helper functions and libraries.
- `paths.py`: Define paths for running the application and saving invoices.
- `requirements.txt`: List of Python dependencies required for the project.
- `templates/`: Folder where you should add your own invoice templates.
- `assets/`: Folder to store your company logo and other related assets.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/InvoiceApp.git
   ```
2. Navigate to the project directory:
   ```bash
   cd InvoiceApp
   ```
3. Install the dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Specify Paths**:

   - Open `paths.py` and specify:
     - The directory where you want to run the application.
     - The directory where generated invoices will be saved.

2. **Add Your Templates**:

   - Place your custom invoice templates in the `templates/` folder.

3. **Add Your Logo**:

   - Add your company logo to the `assets/` folder.

4. **Database Initialization**:

   - In `InvoiceApp.py`, configure the database connection and initialize it with your own database.

5. **Customize Invoice Layout**:

   - Adjust the positions of elements on the invoice based on your design. This can be done through trial and error until the layout fits your requirements.

## Running the Application

To run the main application, execute the following command:

```bash
python InvoiceApp.py
```

## Requirements

- Python 3.8 or higher
- The following Python dependencies (specified in `requirements.txt`):
  ```bash
  pip install -r requirements.txt
  ```

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please fork the repository and submit a pull request.
