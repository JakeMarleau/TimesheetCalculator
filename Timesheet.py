from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
import datetime
import os
import json


setup_folder = r""


open_windows = []

widgets = []

s_w_h = []
s_w = []


if not setup_folder:
	onb = Tk()
	onb.title('Last Step')
	first_lbl = Label(onb, text="There's one last step that needs to be done before starting up.\n\nOpen this file with a text editor, around line 10 you should see: setup_folder = r\"\"\nPaste a file path in between the brackets, this is where your settings will be saved.\n\nLaunch me again after and you're good to go.")
	first_lbl.grid(pady=15)
	onb.mainloop()

def validate_input(stuff):
    try:
        float(stuff)
        return
    except ValueError:
        messagebox.showwarning('Invalid Entries', 'Please only enter numbers into the field.')
        return 1


def start_up():
    global sec_tot, y, x, master_list, grand_tot, date_format, widgets
    ############## MASTER LIST ORDER ##################
    #  Name : [sec_tot(x, y), minute tot]             #
    ###################################################
    master_list = {}

    def check_window():
        if not s_w:
            s_w.append('1')
            Settings()

    date = datetime.datetime.now()
    date_format = date.strftime("%a, %b %d %Y")

    json_read()

    sec_tot = "0"

    root.title("Timesheet Calculator")
    root.configure(bg=bg)

    y = 1
    x = 2
    pre_setup(y)

    date = Label(root, text=date_format, bg=bg, fg=fg)
    widgets.append(date)
    date.grid(row=0, column=0)

    for n in names:
        master_list[n] = []
        Sections(n)

    settings = Button(root, text="Settings...", command=check_window, width=8)
    widgets.append(settings)
    save = Button(root, text="Save", command=save_day, width=8)
    widgets.append(save)
    gran_tot = Label(root, text="Total:", font=("arial", 14), bg=bg, fg=fg)
    widgets.append(gran_tot)

    if len(names) >= 6:
        x = 17
    settings.grid(row=y + 4, column=0)
    save.grid(row=y + 4, column=2, )
    gran_tot.grid(row=y + 4, column=round(x / 3), columnspan=4, pady=7)

    root.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()


def clear_page():
    for widget in widgets:
        widget.grid_forget()


def save_day():
    if os.path.exists(f"{save_loc}/{date_format}.txt"):
        overwrite = messagebox.askyesno("File Exists", "Overwrite current file?")
        if not overwrite:
            return
    file = open(f"{save_loc}/{date_format}.txt", 'w+')
    with file as f:
        f.write(f'{date_format}')
        for name in names:
            f.write(f'\n{name}: {master_list[name][1]} {total_display}')
    file.close()


def fix_save_loc():
    global save_loc
    save_loc = ''
    for letter in save_loc1:
        if letter == '\\':
            letter = '/'
        save_loc += letter


class mylist(list):
    def __str__(self):
        return json.dumps(self)


def json_read():
    global names, a, b, c, round_active, round_to, increment_display, total_display, save_loc, save_loc1, bg, fg, \
        diff_displays
    i = True
    if os.path.isfile(f'{setup_folder}/setup.json'):
        try:
            with open(f'{setup_folder}/setup.json', 'r') as f:
                data = json.load(f)
                names = data["Names"]
                a = data["Fields"][0]
                b = data["Fields"][1]
                c = data["Fields"][2]
                round_active = data["Round to"][0]
                round_to = data["Round to"][1]
                increment_display = data["Time Display"][0]
                total_display = data["Time Display"][1]
                save_loc = data['Save Location']
                bg = data['Colour'][0]
                fg = data['Colour'][1]
                i = False
        except:
            clean_json()
            print("passed")

    else:
        clean_json()
        print('else')

    if increment_display != total_display:
        diff_displays = True
    else:
        diff_displays = False

    if increment_display == 'hrs':
        a = round(float(a), 2)
        b = round(float(b), 2)
        c = round(float(c), 2)

    if i:
        json_setup()


def json_setup():
    global a, b, c, names
    if not os.path.exists(setup_folder):
        os.mkdir(setup_folder)

    file = open(f'{setup_folder}/setup.json', 'w+')

    with file as f:
        f.write("{\n")
        names = mylist(names)
        f.write(f'\t"Names": {names},')
        f.write(f'\n\t"Fields": ["{a}", "{b}", "{c}"],')
        f.write(f'\n\t"Round to": ["{round_active}", "{round_to}"],')
        f.write(f'\n\t"Time Display": ["{increment_display}", "{total_display}"],')
        f.write(f'\n\t"Save Location": "{save_loc}",')
        f.write(f'\n\t"Colour": ["{bg}", "{fg}"]')
        f.write("\n}")


def clean_json():
    global names, a, b, c, round_active, round_to, increment_display, total_display, save_loc, save_loc1, bg, fg, \
        diff_displays
    bg = '#909090'
    fg = '#000000'
    names = ["Name1", "Name2", "Name3", "Name4"]
    a = 5
    b = 10
    c = 15
    round_active = "True"
    round_to = "0.25"
    increment_display = 'min'
    total_display = 'hrs'
    save_loc1 = os.getcwd()
    fix_save_loc()


def setup(y):
    box_lbl1 = Label(root, text=f" {a} {increment_display} ", bg=bg, fg=fg)
    box_lbl2 = Label(root, text=f" {b} {increment_display} ", bg=bg, fg=fg)
    box_lbl3 = Label(root, text=f" {c} {increment_display} ", bg=bg, fg=fg)

    box_lbl1.grid(row=y, column=0)
    box_lbl2.grid(row=y + 1, column=0)
    box_lbl3.grid(row=y + 2, column=0)


def pre_setup(y):
    setup(y)
    for i in range(1, (len(names) // 7)):
        new = i * 5
        setup(y + new)


def close():
    for name in open_windows:
        try:
            name.destroy()
        except:
            pass

    root.destroy()


def grand_total(g_tot):
    global gran_tot
    try:
        gran_tot.grid_forget()
    except NameError as e:
        print(e)

    if (g_tot).is_integer():
        gran_tot = Label(root, text=f" Total: {int(float(g_tot))} {total_display} ", font=("arial", 14), bg=bg, fg=fg)
        widgets.append(gran_tot)
    else:
        gran_tot = Label(root, text=f"Total: {g_tot} {total_display}", font=("arial", 14)
                         , bg=bg, fg=fg)
        widgets.append(gran_tot)
    gran_tot.grid(row=y + 4, column=round(x / 3), columnspan=4, pady=7)


def show_settings():
    s_w_h[0].deiconify()
    s_w_h.pop()


class Sections:
    def __init__(self, sec_name):
        global x, y

        def math_time():
            for box in entry1, entry2, entry3:
                if not box.get():
                    box['state'] = NORMAL
                    box.insert(0, 0)
                    box['state'] = DISABLED

            box1_tot = float(entry1.get()) * float(a)
            box2_tot = float(entry2.get()) * float(b)
            box3_tot = float(entry3.get()) * float(c)

            if diff_displays:
                if increment_display == 'min':
                    pre_sec_tot = round((box1_tot + box2_tot + box3_tot) / 60, 2)
                else:
                    pre_sec_tot = round((box1_tot + box2_tot + box3_tot) * 60, 2)
            else:
                pre_sec_tot = round(box1_tot + box2_tot + box3_tot, 2)

            if round_active == "True":
                wholes = pre_sec_tot // float(round_to)
                if (pre_sec_tot % float(float(round_to))) >= float(round_to) / 2:
                    wholes += 1
                sec_tot = float(round_to) * wholes
            else:
                sec_tot = pre_sec_tot

            master_list[sec_name].pop()
            master_list[sec_name].insert(1, sec_tot)

            if (sec_tot).is_integer():
                section_total = Label(root, text=f"  {int(sec_tot)} {total_display}  ", bg=bg, fg=fg)
                widgets.append(section_total)
            else:
                section_total = Label(root, text=f"  {sec_tot} {total_display}  ", bg=bg, fg=fg)
                widgets.append(section_total)
            section_total.grid(row=master_list[sec_name][0][1] + 3, column=master_list[sec_name][0][0]-1, columnspan=3)

            g_tot = 0
            for name in master_list:
                g_tot += master_list[name][1]

            if total_display == 'hrs':
                g_tot = round(g_tot, 2)

            grand_total(g_tot)

        def mod(box, direction):
            box['state'] = NORMAL
            box_value = box.get()
            if box_value == "":
                box_value = 0

            try:
                value = int(box_value)

                if direction == "up":
                    value += 1
                elif direction == "down":
                    value -= 1

                box.delete(0, END)
                box.insert(0, value)
            except:
                print("oops")
            box['state'] = DISABLED
            math_time()

        text = Label(root, text=sec_name, font=("arial", 13), bg=bg, fg=fg)
        widgets.append(text)

        entry1 = Entry(root, justify="center", width=15, bg=bg, fg=fg, borderwidth=0, cursor='arrow')
        widgets.append(entry1)
        entry2 = Entry(root, justify="center", width=15, bg=bg, fg=fg, borderwidth=0, cursor='arrow')
        widgets.append(entry2)
        entry3 = Entry(root, justify="center", width=15, bg=bg, fg=fg, borderwidth=0, cursor='arrow')
        widgets.append(entry3)

        for box in entry1, entry2, entry3:
            box.config(disabledbackground=bg, disabledforeground=fg)
            box['state'] = DISABLED

        plus1 = Button(root, text="+", fg="white", bg="green", command=lambda: mod(entry1, "up"))
        widgets.append(plus1)
        plus2 = Button(root, text="+", fg="white", bg="green", command=lambda: mod(entry2, "up"))
        widgets.append(plus2)
        plus3 = Button(root, text="+", fg="white", bg="green", command=lambda: mod(entry3, "up"))
        widgets.append(plus3)

        minus1 = Button(root, text="-", fg="white", bg="red", command=lambda: mod(entry1, "down"))
        widgets.append(minus1)
        minus2 = Button(root, text="-", fg="white", bg="red", command=lambda: mod(entry2, "down"))
        widgets.append(minus2)
        minus3 = Button(root, text="-", fg="white", bg="red", command=lambda: mod(entry3, "down"))
        widgets.append(minus3)

        section_total = Label(root, text=sec_tot, bg=bg, fg=fg)
        widgets.append(section_total)

        text.grid(row=y - 1, column=x - 1, pady=(5, 0), columnspan=3)

        entry1.grid(row=y, column=x)
        entry2.grid(row=y + 1, column=x)
        entry3.grid(row=y + 2, column=x)

        plus1.grid(row=y, column=x + 1, padx=(0, 4))
        plus2.grid(row=y + 1, column=x + 1, padx=(0, 4))
        plus3.grid(row=y + 2, column=x + 1, padx=(0, 4))

        minus1.grid(row=y, column=x - 1, padx=(1, 0))
        minus2.grid(row=y + 1, column=x - 1, padx=(1, 0))
        minus3.grid(row=y + 2, column=x - 1, padx=(1, 0))

        section_total.grid(row=y + 3, column=x - 1, columnspan=3)
        master_list[sec_name].append((x, y))
        master_list[sec_name].append(0)

        x += 3

        if x > 18:
            x = 2
            y += 5


class Settings:
    def __init__(self):
        settings = Tk()
        open_windows.append(settings)
        settings.title("Settings")
        settings.geometry('400x200')
        settings.winfo_toplevel()

        Grid.rowconfigure(settings, 0, weight=1)
        Grid.columnconfigure(settings, 0, weight=1)

        def close():
            settings.destroy()
            s_w.pop()

        def change_save_loc():
            global save_loc1
            settings.withdraw()
            new_save_loc = filedialog.askdirectory()
            if new_save_loc:
                save_loc1 = new_save_loc
                fix_save_loc()
                json_setup()
            settings.deiconify()

        def change_colour():
            global bg, fg
            settings.withdraw()
            s_w_h.append(settings)
            background = colorchooser.askcolor(title='Choose background colour')
            if background[1] is not None:
                foreground = colorchooser.askcolor(title='Choose foreground colour')
                if foreground[1] is not None:
                    bg = background[1]
                    fg = foreground[1]
                    json_setup()
                    json_read()
                    show_settings()
                    clear_page()
                    start_up()
            try:
                show_settings()
            except:
                print("at least we tried")

        frame = Frame(settings)
        frame.grid(row=0, column=0, sticky='nsew')
        for x in range(2):
            Grid.columnconfigure(frame, x, weight=1)
        for y in range(4):
            Grid.rowconfigure(frame, y, weight=1)

        change_time_incr = Button(frame, text='Change Time Increments', font='Helvetica 11 bold',
                                  command=lambda: [settings.withdraw(), s_w_h.append(settings), TimeIncr()],
                                  bg='light grey')

        change_names = Button(frame, text='Change Name List', font='Helvetica 11 bold',
                              command=lambda: [settings.withdraw(), s_w_h.append(settings), ChangeNames()],
                              bg='light grey')

        tdsb = Button(frame, text='Time Display Settings', font='Helvetica 11 bold',
                      command=lambda: [settings.withdraw(), s_w_h.append(settings), TimeDisplaySettings()],
                      bg='light grey')

        save_location = Button(frame, text='Change Save Location', font='Helvetica 11 bold',
                               command=change_save_loc, bg='light grey')

        exit_button = Button(frame, text='Exit', font='Helvetica 11 bold', bg='black', fg='white', command=close)

        colour_button = Button(frame, text='Theme', font='Helvetica 11 bold', bg=bg, fg=fg,
                               command=change_colour)

        change_time_incr.grid(row=0, column=0, sticky='nsew')

        change_names.grid(row=0, column=1, sticky='nsew')

        tdsb.grid(row=1, column=0, sticky='nsew')

        save_location.grid(row=1, column=1, sticky='nsew')

        colour_button.grid(row=2, column=0, columnspan=2, sticky='nsew')

        exit_button.grid(row=3, column=0, columnspan=2, sticky='nsew')

        settings.protocol("WM_DELETE_WINDOW", close)
        settings.mainloop()


class ChangeNames:
	def __init__(self):
		change_names = Tk()
		open_windows.append(change_names)
		change_names.title("Change Names")
		change_names.geometry("500x400")

		def close():
		    change_names.destroy()
		    show_settings()

		def add_entry():
			entry = Entry(second_frame, justify='center')
			new_names.append(entry)
			entry.grid(row=(len(new_names)-1), padx=175)
			scrolll()


		def remove_entry():
			entry = new_names.pop()
			entry.destroy()

		def save_entries():
		    global names, s_w_h
		    names = []
		    for n in new_names:
		        if n.get():
		            names.append(n.get())
		    json_setup()
		    json_read()
		    change_names.destroy()
		    show_settings()
		    clear_page()
		    start_up()

		new_names = []

		minus_button = Button(change_names, text="-", command=remove_entry)
		name_lbl = Label(change_names, text='Name List')
		plus_button = Button(change_names, text="+", command=add_entry)

		plus_button.pack(side=TOP)
		name_lbl.pack(side=TOP)
		minus_button.pack(side=TOP)

		# Create a Main Frame
		main_frame = Frame(change_names)
		main_frame.pack(fill=BOTH, expand=1)

		# Create a Canvas
		my_canvas = Canvas(main_frame)
		my_canvas.pack(side=LEFT, fill=BOTH, expand=1)


		another_usesless_list = []
		def scrolll():
			if another_usesless_list:
				useless = another_usesless_list.pop()
				useless.destroy()

			# Add Scroll Bar to Canvas
			my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
			another_usesless_list.append(my_scrollbar)
			my_scrollbar.pack(side=RIGHT, fill=Y)

			# Configure the Canvas
			my_canvas.configure(yscrollcommand=my_scrollbar.set)
			my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))


		scrolll()

		# Create another frame inside Canvas
		second_frame = Frame(my_canvas)

		# Add new frame to Window in Canvas
		my_canvas.create_window((0,0), window=second_frame, anchor="nw")


		cancel_button = Button(change_names, text="Cancel", bg=fg, fg=bg,
		                       command=lambda: [change_names.destroy(), show_settings()])
		save_button = Button(change_names, text="Save", command=save_entries, bg=bg, fg=fg)


		cancel_button.pack(side=BOTTOM)
		save_button.pack(side=BOTTOM)

		for name in names:
			entry = Entry(second_frame, justify='center')
			entry.grid(padx=175)
			entry.insert(0, name)
			new_names.append(entry)

		change_names.protocol("WM_DELETE_WINDOW", close)
		change_names.mainloop()


class TimeIncr:
    def __init__(self):
        tsettings = Tk()
        open_windows.append(tsettings)
        tsettings.title('Time Increments')
        tsettings.geometry('275x125')

        Grid.columnconfigure(tsettings, 0, weight=1)
        Grid.columnconfigure(tsettings, 1, weight=1)

        for y in range(5):
            Grid.rowconfigure(tsettings, y, weight=1)

        def close():
            tsettings.destroy()
            show_settings()


        def save_fields():
            global a, b, c, increment_display
            if validate_input(first_entry.get()) != 1 and validate_input(second_entry.get()) != 1 and \
                    validate_input(third_entry.get()) != 1:
                if hrs_var.get():
                    increment_display = "hrs"
                else:
                    increment_display = 'min'
                a = first_entry.get()
                b = second_entry.get()
                c = third_entry.get()
                pre_setup(y - 3)
                json_setup()
                json_read()
                close()

        def deselect(box, box_var, other, other_var):
            box.deselect()
            box_var.set(False)
            other.select()
            other_var.set(True)

        time_field = Label(tsettings, text="Time Increments")

        first_field = Label(tsettings, text="1st")
        second_field = Label(tsettings, text="2nd")
        third_field = Label(tsettings, text="3rd")

        first_entry = Entry(tsettings, width=10, justify='center')
        second_entry = Entry(tsettings, width=10, justify='center')
        third_entry = Entry(tsettings, width=10, justify='center')

        time_field.grid(row=0, column=0, columnspan=2)

        first_field.grid(row=1, column=0, sticky='e')
        second_field.grid(row=2, column=0, sticky='e')
        third_field.grid(row=3, column=0, sticky='e')

        first_entry.grid(row=1, column=1, sticky='w')
        second_entry.grid(row=2, column=1, sticky='w')
        third_entry.grid(row=3, column=1, sticky='w')

        for name, entry in zip([a, b, c], [first_entry, second_entry, third_entry]):
            try:
                entry.insert(0, int(float(name)))
            except:
                entry.insert(0, name)

        time_display_lbl = Label(tsettings, text='Show totals in:')
        minutes_var = BooleanVar()
        hrs_var = BooleanVar()
        if increment_display == "hrs":
            hrs_var.set(True)
        else:
            minutes_var.set(True)
        minutes = Checkbutton(tsettings, text='min', variable=minutes_var, command=lambda: deselect(hrs, hrs_var,
                                                                                                    minutes,
                                                                                                    minutes_var))
        hrs = Checkbutton(tsettings, text='hrs', variable=hrs_var, command=lambda: deselect(minutes, minutes_var, hrs,
                                                                                            hrs_var))

        time_display_lbl.grid(row=4, column=0, columnspan=2)
        minutes.grid(row=5, column=0)
        hrs.grid(row=5, column=1)

        save_button = Button(tsettings, text='Save', command=save_fields, bg=bg, fg=fg)
        cancel_button = Button(tsettings, text='Cancel', command=close, bg=fg, fg=bg)

        save_button.grid(row=6, column=1, sticky='nsew')
        cancel_button.grid(row=6, column=0, sticky='nsew')

        if increment_display == 'hrs':
            hrs.select()
        else:
            minutes.select()

        tsettings.protocol("WM_DELETE_WINDOW", close)
        tsettings.mainloop()


class TimeDisplaySettings:
    def __init__(self):
        tds = Tk()
        open_windows.append(tds)
        tds.title("Time Display Settings")
        tds.geometry('300x150')

        json_read()

        for x in range(2):
            Grid.columnconfigure(tds, x, weight=1)
        for y in range(5):
            Grid.rowconfigure(tds, y, weight=1)

        def close():
            tds.destroy()
            show_settings()

        def save_entries():
            global total_display, round_active, round_to
            if hrs_var.get():
                total_display = "hrs"
            else:
                total_display = 'min'
            round_active = round_var.get()
            if not round_entry.get():
                round_to = 0.25
            elif validate_input(round_entry.get()) != 1:
                round_to = round_entry.get()
                json_setup()
                json_read()
                pre_setup(1)
                close()

        def check_round():
            if round_var.get():
                round_enabled.configure(fg='grey')
                round_totals.configure(fg='grey')
                round_entry.configure(fg='grey', state=DISABLED)
                round_var.set(False)
            else:
                round_enabled.configure(fg='black')
                round_totals.configure(fg='black')
                round_entry.configure(fg='black', state=NORMAL)
                round_var.set(True)
            round_enabled.grid(row=2, column=0, columnspan=2)

        def deselect(box, box_var, other, other_var):
            box.deselect()
            box_var.set(False)
            other.select()
            other_var.set(True)

        time_display_lbl = Label(tds, text='Show total times in:')
        minutes_var = BooleanVar()
        hrs_var = BooleanVar()
        if total_display == "hrs":
            hrs_var.set(True)
        else:
            minutes_var.set(True)

        minutes = Checkbutton(tds, text='min', variable=minutes_var, command=lambda: deselect(hrs, hrs_var, minutes,
                                                                                              minutes_var))
        hrs = Checkbutton(tds, text='hrs', variable=hrs_var, command=lambda: deselect(minutes, minutes_var, hrs,
                                                                                      hrs_var))

        round_var = BooleanVar()
        round_enabled = Checkbutton(tds, text='Round Totals', variable=round_var, command=check_round)
        round_totals = Label(tds, text='Round totals to:')
        round_entry = Entry(tds, justify='center')

        cancel_button = Button(tds, text='Cancel', command=close, bg=fg, fg=bg)
        save_button = Button(tds, text='Save', command=save_entries, bg=bg, fg=fg)

        time_display_lbl.grid(row=0, column=0, columnspan=2)
        minutes.grid(row=1, column=0)
        hrs.grid(row=1, column=1)

        if total_display == 'hrs':
            hrs.select()
        else:
            minutes.select()

        round_enabled.grid(row=2, column=0, columnspan=2)
        round_totals.grid(row=3, column=0)
        round_entry.grid(row=3, column=1, pady=5)

        if round_active == "True":
            round_entry.insert(0, round_to)
            round_enabled.select()
            check_round()
        else:
            round_enabled.configure(fg='grey')
            round_totals.configure(fg='grey')
            round_entry.configure(fg='grey', state=DISABLED)

        cancel_button.grid(row=4, column=0, sticky='nsew')
        save_button.grid(row=4, column=1, sticky='nsew')

        tds.protocol("WM_DELETE_WINDOW", close)
        tds.mainloop()


if __name__ == "__main__":
    root = Tk()
    start_up()
