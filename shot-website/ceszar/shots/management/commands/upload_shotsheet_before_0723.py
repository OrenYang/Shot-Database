from django.core.management.base import BaseCommand
import pandas as pd
from shots.models import Gas, GasConfig, Shot, Filter, XrayDetector, XuvImage, Schlieren
import tkinter as tk
from tkinter import filedialog
import math
from django.conf import settings
from django.utils.timezone import make_aware
import datetime
import pytz

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        root = tk.Tk()
        root.withdraw()

        # Pop up for chosing the shot sheet
        filepath = filedialog.askopenfilename()

        df  = pd.read_excel(filepath,
                        skiprows=0,)

        ### REORGANIZE DATAFRAME ###

        # find all the unnamed columns and columns with wrong names
        # and assign them a non-zero value
        i=0
        ind=[]
        for col in df.columns:
            if df.columns.get_loc(col) < len(df.columns)-1:
                next = df.columns[df.columns.get_loc(col)+1]
            elif df.columns.get_loc(col) == len(df.columns)-1:
                next = 'end'
            if next.startswith('Unnamed'):
                i+=1
                ind.append(i)
            elif col.startswith('Unnamed'):
                i+=1
                ind.append(i)
                i=0
            else:
                i=0
                ind.append(i)

        # Take name from next row if the row was unnamed or wrong
        for col in df.columns:
            if ind[df.columns.get_loc(col)] != 0:
                new = df[col][0].replace('\n',' ').split('(')[0].lower().strip()
                df.rename(columns={col:new},inplace=True)

        # remove first row and image file columns
        df = df.drop(0)
        df = df.drop(columns='dcim image file')

        #rename duplicate columns EX: xd1 start time --> xd1 start time.1
        df.columns = pd.io.parsers.ParserBase({'names':df.columns})._maybe_dedup_names(df.columns)

        # rename p maxwell col if there are extra words
        for col in df.columns:
            if 'pt-55' in col or 'pt55' in col:
                df.rename(columns={col:'p maxwell'},inplace=True)

        df = df.reset_index()

        for index, row in df.iterrows():
            if '*' in str(row['SHOT #']):
                row['SHOT #']=float(str(row['SHOT #']).replace('*',''))
                df.loc[index,'SHOT #']=row['SHOT #']
                df.loc[index,'post-shot notes'] = str(df.loc[index,'post-shot notes'])
                df.loc[index,'post-shot notes']+='*a B-dot is not working'
            if isinstance(row['SHOT #'], datetime.date) or isinstance(row['SHOT #'],datetime.datetime):
                date = row['SHOT #']
                df = df.drop(index)
            elif isinstance(row['load type'], datetime.date) or isinstance(row['load type'],datetime.datetime) or math.isnan(row['SHOT #']):
                date = row['load type']
                df = df.drop(index)
            else:
                df.at[index, 'date'] = date

        for index, row in df.iterrows():
            for col in df.columns:
                if row[col]=='-' or row[col]=='?':
                    row[col]=None
                try:
                    if math.isnan(row[col]):
                        row[col]=None
                        df.loc[index, col]=row[col]
                except Exception:
                    continue
            row['t dip?']=None

            gasses = []
            config = []
            if row['lv press']:
                gas_model_inner = Gas.objects.get(chemical_symbol=row['lv gas'])
                gasses.append(gas_model_inner)
                config.append('liner')
            if row['tv press']:
                gas_model_target = Gas.objects.get(chemical_symbol=row['tv gas'])
                gasses.append(gas_model_target)
                config.append('target')

            if not row['lv press'] and not row['tv press']:
                continue


            if config[0]=='liner' and len(config)==2:
                gasConfig_model = GasConfig.objects.get_or_create(outer=None, inner=gasses[0], target=gasses[1])[0]
            elif config[0]=='target':
                gasConfig_model = GasConfig.objects.get_or_create(outer=None, inner=None, target=gasses[0])[0]
            elif config[0]=='liner':
                gasConfig_model = GasConfig.objects.get_or_create(outer=None, inner=gasses[0], target=None)[0]

            if isinstance(row['date'], str):
                 naive_datetime = datetime.datetime.strptime(row['date'], '%d/%m/%Y')  # Adjust the format if needed
                 row['date'] = make_aware(naive_datetime, pytz.timezone('America/Los_Angeles'))  # Adjust the timezone if needed

            shot_model, created = Shot.objects.get_or_create(num=row['SHOT #'], defaults={
                'date': row['date'],
                'loadType': row['load type'],
                'preNotes': row['pre-shot notes'],
                'postNotes': row['post-shot notes'],
                'gasConfig': gasConfig_model,
                'inner_press': row['lv press'],
                'target_press': row['tv press'],
                'inner_timing': row['lv timing'],
                'target_timing': row['tv timing'],
                'current': row['ipeak'],
                'current_time': row['tpeak'],
                'dip_time': row['t dip?'],
                'cavity_v': row['v cavity'],
                'cavity_p': row['p cavity'],
                'trigger_v': row['v trigger'],
                'trigger_p': row['p trigger'],
                'maxwell_p': row['p maxwell'],
                'premag_v': row['v premag'],
                'premag_t': row['t premag'],
                'pressure': row['vacuum'],
                'amfCharge': row['charge'],
                'amfB': row['bz']
            })

            if row['Bubble detector'] is not None:
                shot_model.bubbles=row['Bubble detector']
                shot_model.save()

            if created:
                if 'mcp1 frame 1' in df.columns:
                    if row['mcp1 frame 1'] is not None:
                        xuvImage_model = XuvImage(shot=shot_model,num=1,frame1=row['mcp1 frame 1'],frame2=row['mcp1 frame 2'],frame3=row['mcp1 frame 3'],frame4=row['mcp1 frame 4'])
                        xuvImage_model.save()
                if 'mcp2 frame 1' in df.columns:
                    if row['mcp2 frame 1'] is not None:
                        xuvImage_model = XuvImage(shot=shot_model,num=2,frame1=row['mcp2 frame 1'],frame2=row['mcp2 frame 2'],frame3=row['mcp2 frame 3'],frame4=row['mcp2 frame 4'])
                        xuvImage_model.save()
                if 'schlieren frame 1' in df.columns:
                    if row['schlieren frame 1'] is not None:
                        schlieren_model = Schlieren(shot=shot_model,num=1,time=row['schlieren frame 1'])
                        schlieren_model.save()
                        schlieren_model = Schlieren(shot=shot_model,num=2,time=row['schlieren frame 2'])
                        schlieren_model.save()

                for i in [1,2,3,4,5,6,7,8]:
                    for j in ['start time','peak time','peak voltage',]:
                        try:
                            row['xd{} {}'.format(i,j)] = float(row['xd{} {}'.format(i,j)])
                        except Exception:
                            if row['xd{} {}'.format(i,j)] is not None:
                                row['post-shot notes']+=' *XD{} notes: '.format(i)+str(row['xd{} {}'.format(i,j)])
                                shot_model.postNotes = row['post-shot notes']
                                shot_model.save()
                                row['xd{} {}'.format(i,j)] = None
                            else:
                                continue

                    if  row['xd{} peak time'.format(i)] is not None:
                        xrayDetector_model = XrayDetector(shot=shot_model,num=i,start=row['xd{} start time'.format(i)],peak_time=row['xd{} peak time'.format(i)],peak_volt=row['xd{} peak voltage'.format(i)])
                        xrayDetector_model.save()

        print('done')
