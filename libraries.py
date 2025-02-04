import os
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QHBoxLayout, QGroupBox, QScrollArea, QFrame, QApplication, QGridLayout
from bidi.algorithm import get_display
import arabic_reshaper
from persiantools.jdatetime import JalaliDate
import pyodbc
from io import BytesIO
from datetime import datetime
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A5
