import sched, datetime, time, os
import threading
import json
#import glob
import tkinter as tk

from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from datetime import datetime, time, timedelta
from os import listdir
from shutil import copy2



class Ui:
    def __init__(self, master):
        self.master = master
        self.master.title('Schedule-a-Clone')

        self.main_frame = tk.Frame(self.master, width=1200, height=650, bg='gray29')
        self.main_frame.grid()

        self.txt_frame = tk.Frame(self.main_frame, bg='gray29', width=600, height=375, pady=25, padx=20)
        self.mcr_frame = tk.Frame(self.main_frame, bg='gray29', width=600, height=375, pady=25, padx=20)
        
        # text and mcr main label frames
        self.txt_main_lab_frame = tk.Frame(self.txt_frame, bg='gray29')
        self.mcr_main_lab_frame = tk.Frame(self.mcr_frame, bg='gray29')

        # text and mcr button/entry frames
        self.txt_orig_frame = tk.Frame(self.txt_frame, bg='gray29')
        self.txt_dest_frame = tk.Frame(self.txt_frame, bg='gray29')

        self.mcr_orig_frame = tk.Frame(self.mcr_frame, bg='gray29')
        self.mcr_dest_frame = tk.Frame(self.mcr_frame, bg='gray29')

        self.txt_active_frame = tk.Frame(self.txt_frame, bg='gray29', pady=10)
        self.mcr_active_frame = tk.Frame(self.mcr_frame, bg='gray29', pady=10)

        self.txt_int_frame = tk.Frame(self.txt_active_frame, bg='gray29', pady=10)
        self.mcr_int_frame = tk.Frame(self.mcr_active_frame, bg='gray29', pady=10)

        # text and mcr entries
        self.txt_orig_ent = tk.Text(self.txt_orig_frame, width=60, height=2, bg='gray16', fg='yellow')
        self.txt_dest_ent = tk.Text(self.txt_dest_frame, width=60, height=2, bg='gray16', fg='yellow')
        self.mcr_orig_ent = tk.Text(self.mcr_orig_frame, width=60, height=2, bg='gray16', fg='yellow')
        self.mcr_dest_ent = tk.Text(self.mcr_dest_frame, width=60, height=2, bg='gray16', fg='yellow')
        
        # text and mcr labels
        self.txt_main_label = tk.Label(self.txt_main_lab_frame, text='.txt',
                                           justify='center', bg='gray29', fg='honeydew3', font='helvetica 20')
        self.mcr_main_label = tk.Label(self.mcr_main_lab_frame, text='MCRList',
                                           justify='center', bg='gray29', fg='honeydew3', font='helvetica 20')

        # text and mcr buttons (dest and origin)
        self.txt_dest_button = tk.Button(self.txt_dest_frame, text='Destination', width=10, height=2,
                                             bg='gray45', fg='honeydew2', relief='flat',
                                             font='helvetica 9', command=self.txt_dest_path)
        self.txt_orig_button = tk.Button(self.txt_orig_frame, text='Origin', width=10, height=2,
                                             bg='gray37', fg='honeydew2', relief='flat',
                                             font='helvetica 9', command=self.txt_orig_path)
        self.mcr_orig_button = tk.Button(self.mcr_orig_frame, text='Origin', width=10, height=2,
                                             bg='gray45', fg='honeydew2', relief='flat',
                                             font='helvetica 9', command=self.mcr_orig_path)
        self.mcr_dest_button = tk.Button(self.mcr_dest_frame, text='Destination', width=10, height=2,
                                             bg='gray37', fg='honeydew2', relief='flat',
                                             font='helvetica 9', command=self.mcr_dest_path)

        # text and mcr buttons (active/inactive)
        self.txt_active_button = tk.Button(self.txt_active_frame, text='Inactive', command=self.tog_text_txt, width=25,
                                             bg='gray45', fg='honeydew2', relief='flat', pady=5, padx=5,
                                               font='helvetica 14')
        self.mcr_active_button = tk.Button(self.mcr_active_frame, text='Inactive', command=self.tog_text_mcr, width=25,
                                             bg='gray45', fg='honeydew2', relief='flat', pady=5, padx=5,
                                               font='helvetica 14')

        # text and mcr log text
        self.txt_log_box = tk.Text(self.txt_frame, width=70, bg='gray16', fg='yellow')
        self.mcr_log_box = tk.Text(self.mcr_frame, width=70, bg='gray16', fg='yellow')

        # Read from info.json and populates origin paths, destination paths, interval choice, and log boxes
        self.read_info()                                              # read json file
        self.from_dir = self.data['txt_origin']
        self.to_dir = self.data['txt_dest']
        self.from_dir_mult = self.data['mcr_origin']
        self.to_dir_mult = self.data['mcr_dest']
        self.def_txt_int_opt = self.data['txt_interval']
        self.def_mcr_int_opt = self.data['mcr_interval']

        ## Print relevent info to respective log boxes
        self.print_text_txt('ORIG: {}'.format(self.from_dir))
        self.print_text_txt('DEST: {}'.format(self.to_dir))
        self.print_text_mcr('ORIG: {}'.format(self.from_dir_mult))
        self.print_text_mcr('DEST: {}'.format(self.to_dir_mult))

        ## Insert relevent path info into origin/destination boxes
        self.txt_orig_ent.insert('end', self.from_dir)
        self.mcr_orig_ent.insert('end', self.from_dir_mult)
        self.txt_dest_ent.insert('end', self.to_dir)
        self.mcr_dest_ent.insert('end', self.to_dir_mult)

        # interval drop-down choices
        choices = {0:'00:00', 1:'01:00', 2:'02:00', 3:'03:00', 4:'04:00',
                            5:'05:00', 6:'06:00', 7:'07:00', 8:'08:00', 9:'09:00',
                            10:'10:00', 11:'11:00', 12:'12:00', 13:'13:00', 14:'14:00',
                            15:'15:00', 16:'16:00', 17:'17:00', 18:'18:00', 19:'19:00',
                            20:'20:00', 21:'21:00', 22:'22:00', 23:'23:00',
                            24:'Every minute', 25:'Every 5 minutes', 26:'Every 30 minutes',
                            27:'Every hour', 28:'Every 6 hours', 29:'Every 12 hours',
                            30:'Every 24 hours'}
        optvartxt = tk.StringVar()
        self.optvarmcr = tk.StringVar()
        optvartxt.set(self.def_txt_int_opt)
        self.optvarmcr.set(self.def_mcr_int_opt)
        self.txt_int = tk.OptionMenu(self.txt_int_frame, optvartxt, *choices.values(), command=self.txt_int_work)
        self.mcr_int = tk.OptionMenu(self.mcr_int_frame, self.optvarmcr, *choices.values(), command=self.mcr_int_work)

        # text and mcr frames grid
        self.txt_frame.grid(row=0, column=0)
        self.mcr_frame.grid(row=0, column=1)

        self.txt_main_lab_frame.grid(row=0, column=0, columnspan=2)
        self.mcr_main_lab_frame.grid(row=0, column=0, columnspan=2)

        self.txt_orig_frame.grid(row=1, column=0)
        self.mcr_orig_frame.grid(row=1, column=0)

        self.txt_dest_frame.grid(row=2, column=0)
        self.mcr_dest_frame.grid(row=2, column=0)

        self.txt_active_frame.grid(row=3, column=0)
        self.mcr_active_frame.grid(row=3, column=0)

        self.txt_int_frame.grid(row=0, column=1)
        self.mcr_int_frame.grid(row=0, column=1)
        
        # text grid
        self.txt_main_label.grid(row=0, column=0, columnspan=2)
        self.txt_orig_button.grid(row=0, column=0)
        self.txt_orig_ent.grid(row=0, column=1)
        self.txt_dest_button.grid(row=0, column=0)
        self.txt_dest_ent.grid(row=0, column=1)
        self.txt_active_button.grid(row=0, column=0)
        self.txt_int.grid(row=0, column=1, sticky='e')
        self.txt_log_box.grid(row=4, column=0, columnspan=2)

        # mcr grid
        self.mcr_main_label.grid(row=0, column=0, columnspan=2)
        self.mcr_orig_button.grid(row=0, column=0)
        self.mcr_orig_ent.grid(row=0, column=1)
        self.mcr_dest_button.grid(row=0, column=0)
        self.mcr_dest_ent.grid(row=0, column=1)
        self.mcr_active_button.grid(row=0, column=0)
        self.mcr_int.grid(row=0, column=1)
        self.mcr_log_box.grid(row=4, column=0, columnspan=2)

        #self.get_files()
        #self.get_file()
    
    def txt_dest_path(self):
        ent = askdirectory(title='Get where you want to put it')
        with open('info.json', 'w') as f:
            self.data['txt_dest'] = ent
            json.dump(self.data, f)
            self.txt_dest_ent.delete(1.0, 'end')
            self.txt_dest_ent.insert('end', self.data['txt_dest'])
            self.print_text_txt('DEST updated to: {}'.format(self.data['txt_dest']))

    def txt_orig_path(self):
        ent = askdirectory(title='Get where it comes from')
        with open('info.json', 'w') as f:
            self.data['txt_origin'] = ent
            json.dump(self.data, f)
            self.txt_orig_ent.delete(1.0, 'end')
            self.txt_orig_ent.insert('end', self.data['txt_origin'])
            self.print_text_txt('ORIG updated to: {}'.format(self.data['txt_origin']))
        
    def mcr_orig_path(self):
        ent = askdirectory(title='Get where it comes from ')
        with open('info.json', 'w') as f:
            self.data['mcr_orig'] = ent
            json.dump(self.data, f)
            self.mcr_orig_ent.delete(1.0, 'end')
            self.mcr_orig_ent.insert('end', self.data['mcr_orig'])
            self.print_text_mcr('ORIG updated to: {}'.format(self.data['mcr_orig']))
            
    def mcr_dest_path(self):
        ent = askdirectory(title='Get where you want to put it')
        with open('info.json', 'w') as f:
            self.data['mcr_dest'] = ent
            json.dump(self.data, f)
            self.mcr_dest_ent.delete(1.0, 'end')
            self.mcr_dest_ent.insert('end', self.data['mcr_dest'])
            self.print_text_mcr('DEST updated to: {}'.format(self.data['mcr_dest']))
        
    def txt_int_work(self, optvartxt):
        with open('info.json', 'w') as f:
            self.data['txt_interval'] = optvartxt
            json.dump(self.data, f)
        self.print_text_txt('Interval updated to: {}'.format(self.data['txt_interval']))

    def mcr_int_work(self, optvarmcr):
        with open('info.json', 'w') as f:
            self.data['mcr_interval'] = optvarmcr
            json.dump(self.data, f)
        self.print_text_mcr('Interval updated to: {}'.format(self.data['mcr_interval']))
            
    def tog_text_txt(self):
        if self.txt_active_button['text'] == 'Inactive':
            self.txt_active_button['text'] = 'Active'
            self.txt_active_button['fg'] = 'red'
            txt = 'Set to active'
        else:
            self.txt_active_button['text'] = 'Inactive'
            self.txt_active_button['fg'] = 'honeydew2'
            txt = 'Set to inactive'
        self.print_text_txt(txt)

    def tog_text_mcr(self):
        if self.mcr_active_button['text'] == 'Inactive':
            self.mcr_active_button['text'] = 'Active'
            self.mcr_active_button['fg'] = 'red'
            txt = 'Set to active'
        else:
            self.mcr_active_button['text'] = 'Inactive'
            self.mcr_active_button['fg'] = 'honeydew2'  
            txt = 'Set to inactive'
        self.print_text_mcr(txt)

    def print_text_txt(self, txt):
        time = datetime.now().strftime('%m.%d.%Y %H:%M:%S')
        self.txt_log_box.insert('1.0', '{} {}\n'.format(time, txt))

    def print_text_mcr(self, txt):
        time = datetime.now()
        self.mcr_log_box.insert('1.0', '{} {}\n'.format(time, txt))

    def read_info(self):
        with open('info.json', 'r') as f:
            self.data = json.load(f)
        return self.data

    
#class Clone():
    #def __init__(self):
        # TODO create configurable paths stored in a JSON file
        #self.from_dir = 'C:/Users/khoward/code/appdev/filecopy/from/'
        #self.from_dir_mult = 'C:/Users/khoward/code/appdev/filecopy/from2/'
        #self.to_dir = 'C:/Users/khoward/code/appdev/filecopy/to/'
        #self.to_dir_mult = 'C:/Users/khoward/code/appdev/filecopy/to2/'
        #self.time_format = '%H:%M:%S'
        
    def schedule(self):
        scheduler = sched.scheduler(time.time, time.sleep)
        pass

    def name_to_date_txt(self, fn):
        d = fn[11:13]
        m = fn[14:16]
        y = fn[17:21]
        date = datetime(int(y), int(m), int(d))

        return date

    def copy_if_past(self, d):
        ''' For use only with the generated .txt files from Cinegy. This should exclude the most recent,
         living file. '''
        if d[1] < (datetime.now() - timedelta(days=1)):  # less than the present moment minus 24 hrs
            self.copy_file(d[0])
            self.print_text_txt('Copied: {} to DEST'.format(d[0]))
        else:
            self.print_text_txt('Did not copy:{}'.format(d[0]))
        
    def name_to_date_mcr(self, fn):
        pass

    def get_file(self):
        ''' For use with .txt files '''
        files = [self.from_dir + f for f in listdir(self.from_dir)]   # grab contents of origin folder
        files.sort(key=os.path.getmtime)
        
        fnames = [f[-25:] for f in files]
        
        dnames = [d for d in listdir(self.to_dir)]  # grab contents of destination directory
        #dnames.sort(key=os.path.getmtime)
        
        actfiles = [a for a in fnames if a not in dnames]
        actfiles.sort()
        fns = [self.name_to_date_txt(f[-25:]) for f in files]
        fns.sort()
        d_file = zip(fnames, fns)                      # filename/date tuples in a list filename=d_file[0] date=d_file[1]
        #d_file = zip(actfiles, fns)          # TODO need to get this to work to stop copying entire dir

        #[print(a) for a in actfiles]
        #[print(a) for a in fns]
        #[print(a) for a in d_file]
        
        for d in d_file:
            self.copy_if_past(d)

    def get_files(self):
        ''' Compare the origin and destination directories, copies whatever isn't in
            the destination but is in the origin to the destination'''
        o_files = [f for f in listdir(self.from_dir_mult)]
        d_files = [f for f in listdir(self.to_dir_mult)]

        #[self.copy_files(o) for o in o_files if o not in d_files]
        for i in o_files:
            if i not in d_files:
                self.copy_files(i)
                print('Copied:{}'.format(i))
            else:
                print('Did not copy: {}'.format(i))

    def copy_file(self, orig):     
        old = '{}{}'.format(self.from_dir, orig)
        new = '{}{}'.format(self.to_dir, orig)
        
        copy2(old, new)

    def copy_files(self, orig):
        old = '{}{}'.format(self.from_dir_mult, orig)
        new = '{}{}'.format(self.to_dir_mult, orig)
        
        copy2(old, new)


#a = Clone()
#a.get_files()
#a.get_file()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1200x625')
    main_win = Ui(root)
    root.mainloop()
