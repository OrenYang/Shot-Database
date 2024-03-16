from django.core.management.base import BaseCommand
import pandas as pd
from shots.models import Gas, GasConfig, Shot, Filter, XrayDetector, XuvImage, Schlieren
import tkinter as tk
from tkinter import filedialog

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
         root = tk.Tk()
         root.withdraw()

         filepath = filedialog.askopenfilename()

         df  = pd.read_excel(filepath,
                        skiprows=1,)

         print(df)
