from tkinter import *
from tkinter import messagebox
import tkinter as tk
import csv
import os
import numpy as np
root = Tk()
root.resizable(False, False) 
root.title("config")
index = 1

def load_planets():
    global index
    filepath = os.path.join(os.path.dirname(__file__), "planets.csv")
    #print(os.path.join(os.path.dirname(__file__), "planets.csv"))
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if row:
                        #print(row)
                        planet_lst.insert(tk.END, f"{row[0]}. a: {row[1]}, e: {row[2]}, m: {row[3]}")
                        index = max(index, int(row[0]) + 1)
        except Exception as err:
            #print(err)
            messagebox.showerror("Error", f"Failed to load: {err}.")

def add_planet():
    global index
    a = input_a.get()
    e = input_e.get()
    m = input_m.get()
    #print(a,e,m)
    if not a or not e or not m:
        messagebox.showerror("Error", "All fields must be filled in.")
        return
    if not a.replace(".","",1).isdecimal():
        messagebox.showerror("Error", "Semi-major axis must be a valid number.")
        return
    if not e.replace(".","", 1).isnumeric():
        messagebox.showerror("Error", "Eccentricity must be a valid number.")
        return
    else:
        if np.float64(e) >= 1:
            messagebox.showerror("Error", "Eccentricity must be less than 1.")
            return
    if not e.replace(".","", 1).isnumeric():
        messagebox.showerror("Error", "Mass must be a valid number.")
        return
    planet_lst.insert(tk.END, f"{index}. a: {np.float64(a)}, e: {np.float64(e)}, m: {np.float64(m)}")
    input_a.delete(0, tk.END)
    input_e.delete(0, tk.END)
    input_m.delete(0, tk.END)
    #print(index)
    index += 1

def remove_planet():
    global index
    selected = planet_lst.curselection()
    if not selected:
        messagebox.showerror("Error", "No planet(s) selected.")
        return
    for i in range(len(selected)-1, -1, -1):
        planet_lst.delete(selected[i])
    #recalculation of indices:
    index = 1
    for item in planet_lst.get(0, tk.END):
        parts = item.split(". ")
        planet_lst.delete(0)
        planet_lst.insert(tk.END, f"{index}. {parts[1]}")
        index += 1

def save_planets():
    if not planet_lst.get(0, tk.END):
        messagebox.showerror("Error", "No planets to save.")
        return
    filepath = os.path.join(os.path.dirname(__file__), "planets.csv")
    try:
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Index", "a (AU)", "e", "m (kg)"])
            for item in planet_lst.get(0, tk.END):
                parts = item.split(", ")
                index_val = parts[0].split(". ")[0]
                a = parts[0].split(": ")[1]
                e = parts[1].split(": ")[1]
                m = parts[2].split(": ")[1]
                writer.writerow([index_val, a, e, m])
        messagebox.showinfo("Success", f"Planets saved to {filepath}.")
    except Exception as err:
        messagebox.showerror("Error", f"Failed to save: {err}.")

def clear_planets():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all saved bodies?"):
        filepath = os.path.join(os.path.dirname(__file__), "planets.csv")
        #print(os.path.join(os.path.dirname(__file__), "planets.csv"))
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            messagebox.showinfo("Success", "Saved bodies cleared.")
        except Exception as err:
            messagebox.showerror("Error", f"Failed to clear: {err}.")
            #print(err)

def run_simulation():
    filepath = os.path.join(os.path.dirname(__file__), "planetsworking.csv")
    try:
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Index", "a (AU)", "e", "m (kg)"])
            for item in planet_lst.get(0, tk.END):
                parts = item.split(", ")
                index_val = parts[0].split(". ")[0]
                a = parts[0].split(": ")[1]
                e = parts[1].split(": ")[1]
                m = parts[2].split(": ")[1]
                writer.writerow([index_val, a, e, m])
        with open(os.path.join(os.path.dirname(__file__), "parameters.txt"), "w") as f:
            f.write(f"{input_size.get()}\n{input_time.get()}\n")
    except Exception as err:
        #print(err)
        messagebox.showerror("Error", f"Failed to save: {err}.")
    os.system("python orbit_traces.py")

def reset_entries():
    if messagebox.askyesno("Confirm", "Are you sure you want to reset all fields to defaults?"):
        input_size.delete(0, tk.END)
        input_size.insert(0, "150")
        input_time.delete(0, tk.END)
        input_time.insert(0, "10")
        planet_lst.delete(0, tk.END)
        input_a.delete(0, tk.END)
        input_e.delete(0, tk.END)
        input_m.delete(0, tk.END)

# UI starts from here VVV
frm5 = tk.Frame(root)
frm6 = tk.Frame(frm5)
frm6.pack(side=tk.LEFT)
frm7 = tk.Frame(frm5)
frm7.pack(side=tk.LEFT)

input_size_label = tk.Label(frm6, text="sizescale: ").grid(column=0, row=1, sticky="nsew")
input_size = tk.Entry(frm6)
input_size.grid(column=1, row=1, sticky="nsew")
input_size_legend = tk.Label(frm6, text="pixels = 1 simulated AU").grid(column=2, row=1, sticky="nsew")
input_time_label = tk.Label(frm7, text="timescale: ").grid(column=0, row=1, sticky="nsew")
input_time = tk.Entry(frm7)
input_time.grid(column=1, row=1, sticky="nsew")
input_time_legend = tk.Label(frm7, text="seconds = 1 simulated year").grid(column=2, row=1, sticky="nsew")
for i in range(3):
    frm6.columnconfigure(i, weight=1)
    frm7.columnconfigure(i, weight=1)
frm6.rowconfigure(1, weight=1)
frm7.rowconfigure(1, weight=1)
input_size.config(width=20)
input_time.config(width=20)
frm6.pack(side=tk.LEFT, padx=0)
frm7.pack(side=tk.LEFT, padx=100)
frm5.pack(side=tk.TOP,padx=5,pady=0,anchor="w",expand=True,fill="both")

frm4 = tk.Frame(root,bg="lightblue")
quitbtn = tk.Button(frm4, text="Quit", command=root.destroy).pack(side="right")
runbtn = tk.Button(frm4, text="Run simulation", command=run_simulation).pack(side="left")
frm4.pack(side=tk.BOTTOM,padx=5,pady=5,anchor="e",expand=True)

frm3 = tk.Frame(root,bg="lightblue")
savebtn = tk.Button(frm3, text="Save custom bodies", command=save_planets).pack(side="left")
clearbtn = tk.Button(frm3, text="Clear custom bodies", command=clear_planets).pack(side="left")
frm3.pack(side=tk.BOTTOM,padx=5,pady=5,anchor="w",expand=True)

frm8 = tk.Frame(root,bg="lightblue")
resetbtn = tk.Button(frm8, text="Reset to defaults", command=reset_entries).pack(side="right")
frm8.pack(side=tk.BOTTOM,padx=5,pady=5,anchor="w",expand=True)

frm2 = tk.Frame(root,bg="lightblue")
planet_lst = tk.Listbox(frm2,selectmode=tk.MULTIPLE)
planet_lst.grid(column=0, row=0, sticky="nsew")
frm2.rowconfigure(0, weight=1)
frm2.columnconfigure(0,weight=1)
frm2.pack(side=tk.BOTTOM,padx=5,pady=5,anchor="nw",expand=True,fill="both")


frame_modify = tk.Frame(root, bg="lightblue")
input_a_label = tk.Label(frame_modify, text="semi-major axis (a/AU): ").grid(column=0, row=1, sticky="nsew")
input_a = tk.Entry(frame_modify)
input_a.grid(column=1, row=1, sticky="nsew")
input_e_label = tk.Label(frame_modify, text="eccentricity (e): ").grid(column=2, row=1, sticky="nsew")
input_e = tk.Entry(frame_modify)
input_e.grid(column=3, row=1, sticky="nsew")
input_m_label = tk.Label(frame_modify, text="mass (m/kg): ").grid(column=4, row=1, sticky="nsew")
input_m = tk.Entry(frame_modify)
input_m.grid(column=5, row=1, sticky="nsew")
button_add = tk.Button(frame_modify, text="Add planet", command=add_planet).grid(column=6, row=1, sticky="nsew")
button_remove = tk.Button(frame_modify, text="Remove selected planet(s)", command=remove_planet).grid(column=7, row=1, sticky="nsew")
for i in range(8):
    frame_modify.columnconfigure(i, weight=1)
frame_modify.rowconfigure(1, weight=1)
frame_modify.pack(side=tk.BOTTOM, padx=5, pady=5, ipadx=5, expand=True, fill="both")

frame_modify_display = tk.Frame(root)
display_label = tk.Label(frame_modify_display,text="Modify custom bodies: ",font=("Noto Sans", 12)).grid()
frame_modify_display.pack(side=tk.BOTTOM,padx=5,pady=5,expand=True,anchor="w")

load_planets()
input_size.insert(0, "150")
input_time.insert(0, "10")
root.mainloop()
