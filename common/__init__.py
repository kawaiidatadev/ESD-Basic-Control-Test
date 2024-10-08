import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog, StringVar, ttk
from PIL import Image, ImageTk
import sqlite3
import subprocess
from datetime import datetime, timedelta # Importa solo la clase datetime
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
from dateutil.relativedelta import relativedelta
import tkinter.font as tkfont
import pandas as pd
import pyautogui
import tempfile
import ctypes
import sqlite3
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
import pytz
