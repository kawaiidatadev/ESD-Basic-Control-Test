import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog, StringVar, ttk
from PIL import Image, ImageTk
import sqlite3
import subprocess
from datetime import datetime  # Importa solo la clase datetime
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
import shutil
import locale
import win32com.client as win32  # Para manipulación de Excel en Windows
import pytz
import webbrowser
import time
import getpass
from tkcalendar import DateEntry