import tkinter as tk
import threading
from scrape import scrape_sub, scrape_sub_links

root = tk.Tk()
root.resizable(0, 0)
root['bg'] = '#383D3B'
root.title('The Ultimate Subreddit Link Scraper')

widgets = {}

def MakeLabel(wroot, name, text, rown):
	widgets[name] = tk.Label(
		wroot, text=text, font='Courier 12 bold', 
		bg='#383D3B', fg='#EEE5E9')
	widgets[name].grid(row=rown, column=0, sticky=tk.W, padx=12, columnspan=3)

def MakeEntry(wroot, name, width, rown):
	widgets[name] = tk.Entry(wroot, width=width, 
		font='Courier 12',
		bg='#414749', fg='#EEE5E9',
		disabledbackground='#383D3B')
	widgets[name].grid(row=rown, column=0, sticky=tk.W, padx=12, columnspan=3)

rown = 0

root.grid_rowconfigure(0, minsize=8)
rown += 1

MakeLabel(root, 'label_subreddit', 'Subreddit', rown)
rown += 1

MakeEntry(root, 'box_subreddit', 32, rown)
rown += 1

MakeLabel(root, 'label_category', 'Category', rown)
rown += 1

category_var = tk.StringVar(root)
widgets['dropdown_category'] = tk.OptionMenu(
	root, category_var, "top", "hot", "controversial", "gilded")
widgets['dropdown_category'].configure(
	highlightthickness=0,
	font='Courier 12',
	bg='#414749', fg='#EEE5E9',
	activebackground='#8E8E8E')
widgets['dropdown_category']['menu'].config(
	font='Courier 9',
	bg='#8E8E8E', fg='#EEE5E9',
	activeborderwidth=0)
widgets['dropdown_category'].grid(
	row=rown, column=0, 
	columnspan=3, sticky=tk.W, padx=12)
rown += 1

MakeLabel(root, 'label_limit', 'Limit', rown)
rown += 1

MakeEntry(root, 'box_limit', 4, rown)
rown += 1

MakeLabel(root, 'label_main_regex', 'Submission Title Regex', rown)
rown += 1

MakeEntry(root, 'box_main_regex', 32, rown)
rown += 1

MakeLabel(root, 'label_type_regex', 'File Type Regex', rown)
rown += 1

MakeEntry(root, 'box_type_regex', 32, rown)
rown += 1

widgets['button_scrape'] = tk.Button(root, text='SCRAPE',
	font='Courier 12 bold',
	bg='#414749', fg='#EEE5E9',
	activebackground='#8E8E8E')
widgets['button_scrape'].grid(row=rown, column=0, pady=10)

radio_var = tk.IntVar()
radio_var.set(0)

# TODO(pixlark): Any way to send the argument through the radiobutton?
def disable_box_type_regex():
	widgets['box_type_regex'].configure(state=tk.DISABLED)

def enable_box_type_regex():
	widgets['box_type_regex'].configure(state=tk.NORMAL)

widgets['radio_down'] = tk.Radiobutton(
	root, text='Down',
	variable=radio_var,
	value=0,
	font='Courier 12 bold',
	bg='#414749', fg='#EEE5E9',
	activebackground='#8E8E8E',
	selectcolor='#8E8E8E',
	indicatoron=0,
	command=enable_box_type_regex)
widgets['radio_down'].grid(row=rown, column=1, pady=10, sticky=tk.E)

widgets['radio_link'] = tk.Radiobutton(
	root, text='Link',
	variable=radio_var,
	value=1,
	font='Courier 12 bold',
	bg='#414749', fg='#EEE5E9',
	activebackground='#8E8E8E',
	selectcolor='#8E8E8E',
	indicatoron=0,
	command=disable_box_type_regex)
widgets['radio_link'].grid(row=rown, column=2, pady=10, sticky=tk.W)
rown += 1

def wait_for_thread_completion(wthread):
	if not wthread.isAlive():
		root.title('The Ultimate Subreddit Link Scraper')
		return
	root.after(1000, wait_for_thread_completion, wthread)

def button_scrape_pressed():
	main_regex = widgets['box_main_regex'].get()
	if main_regex == '':
		main_regex = None
	scrape_thread = None
	if radio_var.get() == 0:
		scrape_thread = threading.Thread(
			target=scrape_sub,
			args=(
				widgets['box_subreddit'].get(),
				category_var.get(),
				int(widgets['box_limit'].get()),
				main_regex,
				widgets['box_type_regex'].get()))
	else:
		scrape_thread = threading.Thread(
			target=scrape_sub_links,
			args=(
				widgets['box_subreddit'].get(),
				category_var.get(),
				int(widgets['box_limit'].get()),
				main_regex))
	scrape_thread.start()
	root.title('Scraping...')
	wait_for_thread_completion(scrape_thread)

widgets['button_scrape']['command'] = button_scrape_pressed

root.mainloop()