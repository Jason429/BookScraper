# This is the gui to start the file grab
import os
import sys
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter.constants import *
import tkinter.messagebox as msgbox
import tkinter.scrolledtext as tkst
from grab import scrape, produce
from collections import namedtuple

# Global window setup

R_HEIGHT = 700
R_WIDTH = 800
R_OFF_X = 100
R_OFF_Y = 10
running_list = []

file_org = namedtuple('FileOrg',
                      ['filename',
                       'Label',
                       'Entry',
                       'Remove',
                       'order_num'])

# Class generator

# Functions

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


def create_frame_in(canvas,csize):
    """This creates the frame in the canvas"""
    frame_in_canvas = tk.Frame(canvas,
                               background="#0000aa",
                               width = csize[0],
                               height = csize[1])
    canvas.create_window((4,4), window=frame_in_canvas, anchor='nw')
    frame_in_canvas.bind("<Configure>", 
                         lambda event,
                         canvas=canvas: onFrameConfigure(canvas))
    return frame_in_canvas


def f_weight_set(obj):
    for i in range(10):
        obj.rowconfigure(i, weight=1)
        obj.columnconfigure(i, weight=1)



def sort_running(item):
    return item.order_num

# Put running_list in frame_on_canvas
def show_running(iter_org):
    for action in iter_org:
        #print(action.order_num)
        c = action.order_num
        action.Label.grid(row = action.order_num, column = 0)
        action.Entry.delete(0, END)
        action.Entry.insert(0, str(action.order_num))
        action.Entry.grid(row = action.order_num, column = 1)
        action.Remove.grid(row = action.order_num, column = 2)


def destroy_show(iter_org):
    for i in iter_org:
        i.Label.destroy()
        i.Entry.destroy()
        i.Remove.destroy()
    frame_in_canvas.destroy()


def remove_file(num):
    
    ## Destroy generate main
    global running_list
    destroy_show(running_list)

    ## Needs to remove item from running_list
    running_list.pop(num -1)
    temp = [x.filename for x in sorted(running_list,key=sort_running)]
    
    
    ## Rebuild generate main from running_list
    global frame_in_canvas
    frame_in_canvas = create_frame_in(canvas, csize)
    running_list = generate_main(temp)
    show_running(running_list)



def refresh_dir(redo=False):
    global running_list
    if len(running_list) != 0:
        destroy_show(running_list)
    global frame_in_canvas
    frame_in_canvas = create_frame_in(canvas, csize)
    if redo is True:
        running_list = t_file_num_init()
    show_running(running_list)
    return running_list


def generate_main(sorted_list):
    """This runs through creating the folder structure using only
a list of filenames.  Sorted_list will be in the order to number."""
    ordered_d = sorted_list
    org_list = []
    count = 0
    for file in ordered_d:
        count += 1
        c = str(count)
        org_list.append(
            file_org(
                file,
                tk.Label(frame_in_canvas,
                         background="#cccccc",
                         text = file,
                         width = 60,
                         height = 1,
                         ),
                tk.Entry(frame_in_canvas,
                         width = 15,
                         text = str(count),
                          ),
                tk.Button(frame_in_canvas,
                          background="#ff9999",
                          text = 'Remove',
                          command = eval(
                              'lambda: remove_file({})'.format(count)),
                          width = 10,
                          height = 1
                          ),
                count
                )
            )
        # print('Count #',count)
    return org_list


def t_file_num_init():
    '''Returns a tuple of files and number'''
    def d_sorter(item):
        return d[item]
    _, _, walk = next(os.walk(rWin.file_directory))
    d = {}
    for i in range(len(walk)):
        d[walk[i]] = i
    ordered_d = sorted(d, key=d_sorter)
    return generate_main(ordered_d)

def f_scrape_site():
    """Grabs scrape_page value and scrapes that site.
    Modifies current_file_list global variable"""
    page = scrape_page.get()
    site = scrape(page, rWin.file_directory)
    for resp in site:
        if resp != '*' :
            resp = '\n' + resp
        msg_bottom.configure(state=tk.NORMAL)
        msg_bottom.insert(tk.INSERT, str(resp))
        msg_bottom.configure(state=tk.DISABLED)
        msg_bottom.see(tk.END)
        rWin.update_idletasks()
    refresh_dir(redo=True)


def sort_files():
    '''Grab numbers and reorder files.'''
    global running_list
    #raise
    for i in running_list:
        try:
            int(i.Entry.get())
        except ValueError:
            msg = "\nNot a number at file {}\n".format(i.filename) + \
                  "Pls fix or refresh.\n"
            msg_bottom.configure(state=tk.NORMAL)
            msg_bottom.insert(tk.INSERT, msg)
            msg_bottom.configure(state=tk.DISABLED)
            msg_bottom.see(tk.END)
            # Clean frame
            return
    def sort(item):
        return int(item.Entry.get())
     
    temp_list = [i.filename for i in sorted(running_list, key=sort) ]
    destroy_show(running_list)
    global frame_in_canvas
    frame_in_canvas = create_frame_in(canvas, csize)
    running_list = generate_main(temp_list)

    show_running(running_list)
    
def generate_file():
    global from_entry, to_entry, running_list
    try:
        first = int(from_entry.get())
        last = int(to_entry.get())
    except:
        msgbox.showerror("Range Error", "Only numbers for range of files.")
        return
    sent_list = [i.filename for i in running_list]
    sent_list = sent_list[first - 1: last]
    file_created = produce(sent_list, rWin.file_directory)
    msgbox.showinfo('SUCCESS',
                    'File {} has been created in your folder'.format(file_created))
    
                        

def f_quit():
    sys.exit()

# Main

base = os.path.join(os.getcwd(),'BookScrape')
if not os.path.exists(base):
    try:
        os.makedirs(os.path.join(os.getcwd(),'BookScrape'))
    except:
        print("Couldn't create BookScrape directory.")
        base = os.getcwd()


rWin = tk.Tk()
rWin.title('BookScrape - Simple HTML combiner and link fetcher')
# image = tk.PhotoImage(file=os.path.join(os.getcwd(),'scraper.ico'))
# rWin.tk.call('wm', 'iconphoto', rWin_w, image)
rWin.geometry('{}x{}+{}+{}'.format(R_WIDTH, R_HEIGHT,R_OFF_X, R_OFF_Y))
rWin.current_file_list = {}
rWin.file_directory = base
f_weight_set(rWin)
del base

#Inform current directory

change_file_dir = msgbox.askyesno('Welcome to Book Scraper', \
    "\n\nWe will need to confirm where you your working files are.\n\n" + \
    "Use directory {} ?".format(rWin.file_directory.replace("/","\\")))


if not change_file_dir:
    rWin.file_directory = filedialog.askdirectory(
        initialdir=rWin.file_directory)
print(rWin.file_directory)    

# Create frames
rWin.focus_force()

frame_top = tk.Frame(rWin)
frame_top.grid(row=1, column=0, columnspan=2)
f_weight_set(frame_top)

#frame_debug = tk.Frame(rWin)
#frame_debug.grid(row=2, column=0)
#f_weight_set(frame_debug)

frame_label = tk.Frame(rWin,width=200,background='grey')
f_weight_set(frame_label)
frame_label.grid(row=2, column=0, columnspan=2, sticky='w', padx=20)
dir_label = tk.Label(frame_label,
                     text='File Directory {}'.format(rWin.file_directory))
dir_label.grid(row=0, column=0, sticky='w')

frame_middle = tk.Frame(rWin, height=400)
frame_middle.grid(row=3, column=0, sticky="w")
frame_middle.grid_columnconfigure(0, minsize=580)
f_weight_set(frame_middle)

frame_buttons = tk.Frame(rWin, width=200, height=1000)
frame_buttons.grid(row=3, column=1)
f_weight_set(frame_buttons)

frame_bottom = tk.Frame(rWin)
frame_bottom.grid(row=4, column=0, columnspan=2, sticky='ws')
f_weight_set(frame_bottom)

# define buttons on main screen
#    ----Webpage to scrape (text window + button)
#    ----Files to select (button)
#    ----File Order (button to remove, display name, display order (editable)
#    ----Generate Book (Book Name included)
#    ----Quit


##### TOP #####
scrape_page = tk.Entry(frame_top, width=50, state=NORMAL)
scrape_page.delete(0, END)
scrape_page.insert(0, 'http://www.example.com')
scrape_page.grid(row=0, column=0, padx=5, sticky="w")
scrape_button = tk.Button(frame_top, 
                          text="Scrape site",
                          command=f_scrape_site)
scrape_button.grid(row=0, column=1)
f_weight_set(scrape_page)
f_weight_set(scrape_button)
##### TOP #####

##### MIDDLE #####
csize = (600,600)   # width, height
canvas = tk.Canvas(frame_middle,
                   width = csize[0],
                    height = csize[1],
                   background="#007700")
canvas.grid(row=0, column = 0, stick='nws')



## Create Scrollbar ##
canvas_vsb = tk.Scrollbar(frame_middle, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=canvas_vsb.set)
canvas_vsb.grid(row = 0, column=1, sticky='nsw')

# refresh_dir creates global frame_in_canvas to display

running_list = refresh_dir(redo=True)

# Create Buttons

# Reset all files in directory

refresh_button = tk.Button(frame_buttons, text="Refresh directory",
                           command=lambda: refresh_dir(redo=True))
refresh_button.grid(row=0, column=0, sticky="nw")

# Blank padding

blank_padding1 = tk.Frame(frame_buttons, height=300)
blank_padding1.grid(row=1, column=0)
# Sort numbers

sort_button = tk.Button(frame_buttons, text="Sort",
                        width=20,
                        command= lambda: sort_files())
sort_button.grid(row=2, column=0, sticky="w")

from_label = tk.Label(frame_buttons, text="Starting number")
from_entry = tk.Entry(frame_buttons, width=5)
to_label = tk.Label(frame_buttons, text="Ending number")
to_entry = tk.Entry(frame_buttons, width=5)
create_file = tk.Button(frame_buttons,
                        text="Generate file",
                        command = generate_file)
create_file_note = tk.Label(frame_buttons,
                            text='Note: Creates Final.html file' +
                            ' in BookScrape directory.\n\nImport ' +
                            'that file to '+
                            'Calibre. (or view with a web browser)',
                            width=25,
                            wraplength=150,
                            anchor='w',
                            justify=tk.LEFT)

l = [(from_label, 3),
     (from_entry, 4),
     (to_label, 5),
     (to_entry, 6),
     (create_file, 7),
     (create_file_note, 8)
     ]
for i in l:
    i[0].grid(row = i[1], column=0, sticky='ws')



# Generate file for Calibre




##### MIDDLE #####

##### BOTTOM #####

msg_bottom = tkst.ScrolledText(frame_bottom, width=75,
                               height=3,
                               wrap = tk.WORD, state = tk.DISABLED)
msg_bottom.grid(row=0, column=0, sticky='w')
quit_button = tk.Button(frame_bottom, text="QUIT",
                        padx=10,
                        command=f_quit)
quit_button.grid(row=0, column=1, sticky='w', padx=30)

##### BOTTOM #####


rWin.mainloop()



