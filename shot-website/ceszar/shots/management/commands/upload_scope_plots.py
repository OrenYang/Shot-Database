from django.core.management.base import BaseCommand
import pandas as pd
from shots.models import Gas, GasConfig, Shot, Filter, XrayDetector, XuvImage, Schlieren, ScopePlots
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
            if filename[-3:] == 'png':
                f = os.path.join(directory, filename)

                shot = filename[:4]
                type = filename.split('_')[1]

                if len(filename.split('_'))>=3:
                    continue

                try:
                    shot = float(shot)
                except Exception:
                    continue

                if Shot.objects.filter(num=shot).exists():
                    shot_model = Shot.objects.get(num=shot)

                    scopePlots_model, created = ScopePlots.objects.get_or_create(shot=shot_model)

                    # Save the image to the ScopePlots object
                    if type == 'extras.png':
                        scopePlots_model.extras.save(os.path.basename(f), File(open(f, 'rb')))
                    elif type == 'Iavg.png':
                        scopePlots_model.current.save(os.path.basename(f), File(open(f, 'rb')))
                    elif type == 'timing.png':
                        scopePlots_model.gas_timing.save(os.path.basename(f), File(open(f, 'rb')))
                    elif type == 'switches.png':
                        scopePlots_model.switches.save(os.path.basename(f), File(open(f, 'rb')))

                    scopePlots_model.save()


        print('done')
