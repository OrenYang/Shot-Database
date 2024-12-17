from django.core.management.base import BaseCommand
import pandas as pd
from shots.models import Gas, GasConfig, Shot, Filter, XrayDetector, XuvImage, Schlieren
import tkinter as tk
from tkinter import filedialog
import os
from django.core.files import File

class Command(BaseCommand):

    def  handle(self, *args, **kwargs):
        root = tk.Tk()
        root.withdraw()

        directory = filedialog.askdirectory()

        for filename in os.listdir(directory):
            if filename[-3:] == 'JPG':
                f = os.path.join(directory, filename)

                shot = filename[:4]
                num = filename.split('.')[0][-1]

                try:
                    num = float(num)
                except Exception:
                    continue
                try:
                    shot = float(shot)
                except Exception:
                    continue

                if filename.split('_')[1][0] != 'S':
                    continue

                if Shot.objects.filter(num=shot).exists():
                    shot_model = Shot.objects.get(num=shot)

                    if Schlieren.objects.filter(shot=shot_model, num=num):
                        schlieren_model = Schlieren.objects.get(shot=shot_model, num=num)

                        schlieren_model.image.save(os.path.basename(f),File(open(f,'rb')))
                        schlieren_model.save()


        print('done')
