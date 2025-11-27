#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 18:02:26 2025

@author: yop1
"""
import tkinter as tk

from tkinter import filedialog, messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import picnik as pnk
import numpy as np
import chardet
import os
import sys
import subprocess


root = tk.Tk()
root.title("picnik")
root.geometry("800x800")

# global variable declaration
one_step = []
fig = None
canvas = None
text_help_1=""
label2=""
xtr=None

ace=None
isoTables=None
aVy= None

g_a=None
compensation=""
ap2=None
Tp2=None
tp2 =None

x_data_var = tk.StringVar()
x_unit_var = tk.StringVar()
y_data_var = tk.StringVar()
y_unit_var = tk.StringVar()


#menu options

main_menu = tk.Menu(root)
root.config(menu=main_menu)

file=tk.Menu(main_menu,tearoff=0)
file.add_command(label="open files",command=lambda:open_files())
file.add_command(label="save files",command=lambda:save_files())
file.add_separator()
file.add_command(label="exit",command=lambda:salir())

graph=tk.Menu(main_menu,tearoff=0)
graph.add_command(label="save graph",command=lambda:save_graph())

help_1=tk.Menu(main_menu,tearoff=0)
help_1.add_command(label="tutorial",command=lambda:tutorial())
help_1.add_command(label="about ",command=lambda:about())

main_menu.add_cascade(label="file",menu=file)
main_menu.add_cascade(label="graph",menu=graph)
main_menu.add_cascade(label="help",menu=help_1)




#Frame for controls label and buttons

control_frame = tk.Frame(root)


control_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=10, pady=10)


frame = tk.Frame(root, bg="lightgray")
frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=2, pady=2)

# Configure rows and columns to grow with window
root.grid_rowconfigure(1, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)


#Labels and buttons are created and assigned a place

label1 = tk.Label(control_frame, text=(
    "Please enter only two or more files.\n"
    "Valid extensions: .csv, .txt\n"
    #"No compressed files (.gz, .bz2, .zip, .xz, .zst, .tar, etc.)"
))
label2 = tk.Label(control_frame, text=text_help_1)

label1.grid(row=0, column=0, columnspan=5, sticky="w", pady=2)
label2.grid(row=0, column=5, columnspan=5, sticky="w", pady=2)

#Creating buttons and hiding all of them except the file open button
button_open_files = tk.Button(control_frame, text="open files", command=lambda: open_files())
button_open_files.grid(row=1, column=0, padx=2, pady=2, sticky="ew")

button_graph1 = tk.Button(control_frame, text="Summary", command=lambda: funcion1())
button_graph1.grid(row=1, column=1, padx=2, pady=2, sticky="ew")
button_graph1.grid_forget()

button_graph2 = tk.Button(control_frame, text="Extra2", command=lambda:funcion2())
button_graph2.grid(row=1, column=2, padx=2, pady=2, sticky="ew")
button_graph2.grid_forget()


button_combo = tk.Button(control_frame, text="ver multi grafica", command=lambda:funcion2())
button_combo.grid(row=1, column=2, padx=2, pady=2, sticky="ew")
button_combo.grid_forget()


button_graph3 = tk.Button(control_frame, text="Conversion", command=lambda:funcion3())
button_graph3.grid(row=1, column=3, padx=2, pady=2, sticky="ew")
button_graph3.grid_forget()

button_graph4 = tk.Button(control_frame, text="Extra4", command=lambda:funcion4())
button_graph4.grid(row=1, column=4, padx=2, pady=2, sticky="ew")
button_graph4.grid_forget()

button_graph5 = tk.Button(control_frame, text="Extra5", command=lambda:funcion5())
button_graph5.grid(row=1, column=5, padx=2, pady=2, sticky="ew")
button_graph5.grid_forget()

button_graph6 = tk.Button(control_frame, text="Extra6", command=lambda:funcion6())
button_graph6.grid(row=1, column=6, padx=2, pady=2, sticky="ew")
button_graph6.grid_forget()

button_graph7 = tk.Button(control_frame, text="Extra7", command=lambda:funcion7())
button_graph7.grid(row=1, column=7, padx=2, pady=2, sticky="ew")
button_graph7.grid_forget()

button_graph8 = tk.Button(control_frame, text="Extra8", command=lambda:funcion8())
button_graph8.grid(row=1, column=8, padx=2, pady=2, sticky="ew")
button_graph8.grid_forget()

save_file = tk.Button(control_frame, text="save_files", command=lambda:save_files())
save_file.grid(row=1, column=1, padx=2, pady=2, sticky="ew")

button_save_graph = tk.Button(control_frame, text="save gráfico", command=lambda: save_graph())
button_save_graph.grid(row=1, column=2, padx=2, pady=2, sticky="ew")


arreglo_x_data = ["time", "temperature"]
arreglo_y_data = ["TG", "DTG","dT/dt"]

#for time in x_data
x_units1 = ["min"]
#for temperature in x_data
x_units2 = ["C","K"]

#for TG en y_data
y_units1 = ["%","mg"]
#for DTG in y_data
y_units2 = ["%/min","mg/min","%/s","mg/s"]
y_units2 = ["%/min","mg/min"]
#for dT/dt in _y_data
#y_units3 = ["K/min","C/min","K/s","C/s"]
y_units3 = ["K/min","C/min"]








combo_x_data = ttk.Combobox(control_frame, textvariable=x_data_var, values=arreglo_x_data, state="readonly")
combo_x_data.grid(row=1,column=9)
combo_x_data.current(0)  #selecciona la primera opción (índice 0)
combo_x_data.grid_forget()  #esconde el combobox

combo_y_data = ttk.Combobox(control_frame, textvariable=y_data_var, values=arreglo_y_data, state="readonly")
combo_y_data.grid(row=1, column=10)
combo_y_data.current(0)
combo_y_data.grid_forget()  # inicialmente oculto

# --- Combobox de unidades X ---
combo_x_units1 = ttk.Combobox(control_frame, textvariable=x_unit_var, values=x_units1, state="readonly")
combo_x_units1.grid(row=1, column=11)
combo_x_units1.current(0)
combo_x_units1.grid_forget()

combo_x_units2 = ttk.Combobox(control_frame, textvariable=x_unit_var, values=x_units2, state="readonly")
combo_x_units2.grid(row=1, column=11)
combo_x_units2.current(0)
combo_x_units2.grid_forget()

# --- Combobox de unidades Y ---
combo_y_units1 = ttk.Combobox(control_frame, textvariable=y_unit_var, values=y_units1, state="readonly")
combo_y_units1.grid(row=1, column=12)
combo_y_units1.current(0)
combo_y_units1.grid_forget()

combo_y_units2 = ttk.Combobox(control_frame, textvariable=y_unit_var, values=y_units2, state="readonly")
combo_y_units2.grid(row=1, column=12)
combo_y_units2.current(0)
combo_y_units2.grid_forget()

combo_y_units3 = ttk.Combobox(control_frame, textvariable=y_unit_var, values=y_units3, state="readonly")
combo_y_units3.grid(row=1, column=12)
combo_y_units3.current(0)
combo_y_units3.grid_forget()







# Function to detect encoding
def detectar_encoding(file, num_bytes=10000):
    with open(file, 'rb') as f:
        raw_data = f.read(num_bytes)
    result = chardet.detect(raw_data)
    return result['encoding'], result['confidence']


#reads the files and compares if the encodings are the same
def open_files():
    global one_step
    one_step.clear()# delete the contents of one_step
    
    try:
            
        files = filedialog.askopenfilenames(
            filetypes=[("valid files", "*.csv *.txt")]
        )
    
        if len(files) > 1:#validation of two more files
            one_step.clear()
            one_step.extend(files)
            print("selected files:")
            for file in one_step:
                print(file)
            
            button_open_files.grid_forget()
            button_graph1.grid(row=1, column=0)      
        
        else:
            print("No file selected.")
            messagebox.showinfo(
                title="Two or more files, please",
                message="Two or more files, please"
            )
            one_step.clear()
        
          
    
    except:
        messagebox.showerror("unexpected error")



#the first graph is created
def funcion1():
    global one_step, fig, canvas,xtr, label2, text_help_1
    global x_data,y_data,x_units,y_units
    
    # Clear the chart frame
    for widget in frame.winfo_children():
        widget.destroy()

    try:

        # Get encoding of all selected files
        codificaciones = []
        for file in one_step:
            encoding, conf = detectar_encoding(file)
            if encoding:
                codificaciones.append(encoding)
            else:
                messagebox.showerror("Error", f"The encoding could not be detected: {file}")
                return
    
        # Check if all encodings are equal
        encoding_set = set(codificaciones)
        if len(encoding_set) == 1:
            encoding_final = encoding_set.pop()
        else:
            messagebox.showerror(
               "Encoding incompatibility",
               "The files have different encodings:\n" + "\n".join(f"{f} => {e}" for f, e in zip(one_step, codificaciones))
            )
            return  # Does not continue if the encodings are different
    
       # Continue reading files and Dataextraction object is created
       
        xtr = pnk.DataExtraction()
        
        fig= xtr.read_files(one_step, encoding=encoding_final)
    
        text_help_1 = ""
        for b in range(len(xtr.Beta)):
            text_help_1 += f'{xtr.Beta[b]:.3f} +/- {xtr.BetaError[b]:.3f} K/min\n'
    
        label2.config(text=text_help_1)
    
        # Insert the figure into the frame using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        button_graph1.grid_forget()
        button_graph2.grid(row=1, column=0)
        button_combo.grid(row=1,column=3)
        combo_x_data.grid(row=1,column=4)
        combo_y_data.grid(row=1,column=5)
        
                # --- Función que se ejecutará cuando se escoja una opción ---
        # --- Funciones de selección ---
        def select_x_data(event):
            valor = x_data_var.get()
            # ocultar todos
            combo_x_units1.grid_forget()
            combo_x_units2.grid_forget()
        
            if valor == "time":
                combo_x_units1.grid(row=1, column=11)
                x_unit_var.set(x_units1[0])
            elif valor == "temperature":
                combo_x_units2.grid(row=1, column=11)
                x_unit_var.set(x_units2[0])
        
        def select_y_data(event):
            valor = y_data_var.get()
            # ocultar todos
            combo_y_units1.grid_forget()
            combo_y_units2.grid_forget()
            combo_y_units3.grid_forget()
        
            if valor == "TG":
                combo_y_units1.grid(row=1, column=12)
                y_unit_var.set(y_units1[0])
            elif valor == "DTG":
                combo_y_units2.grid(row=1, column=12)
                y_unit_var.set(y_units2[0])
            elif valor == "dT/dt":
                combo_y_units3.grid(row=1, column=12)
                y_unit_var.set(y_units3[0])
        
        # --- Vincular eventos ---
        combo_x_data.bind("<<ComboboxSelected>>", select_x_data)
        combo_y_data.bind("<<ComboboxSelected>>", select_y_data)
        
            
        
    except:
        messagebox.showerror("unexpected error")



#the second graph is created
def funcion2():
    global fig,label2,text_help_1,xtr,x_data,y_data,x_units,y_units
    text_help_1=""
    label2.config(text=text_help_1)
    # Clear the chart frame
    for widget in frame.winfo_children():
        widget.destroy()
        
    try:
       
        print("x_data:", x_data_var.get())
        print("x_units:", x_unit_var.get())
        print("y_data:", y_data_var.get())
        print("y_units:", y_unit_var.get())

        fig=xtr.plot_data(x_data=x_data_var.get(),y_data=y_data_var.get(), x_units=x_unit_var.get(), y_units=y_unit_var.get())    
        # Insert the figure into the frame using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        button_graph2.grid_forget()
        button_graph3.grid(row=1, column=0)
        
        

    except:
        messagebox.showerror("unexpected error")


# the third graph is created
def funcion3():
    global fig,label2,text_help_1,xtr
    text_help_1='Activation Energy\nThe "classic" methods, i.e., Fr(, OFW(, KAS( and Vy( remain the same. While the advanced \nmethod of Vyazovkin has suffered some minor modifications. One of them is the possiblity to\n define the parameter $p$, which defines the level of confidence for the error associated to the\n activation energy, being 1 a 100%. Other modifications include the integration method (available \nmethods: trapezoid(default),simpson and romberg). The Romberg method may be a little more\n accurate but takes a lot more of time.  '
    label2.config(text=text_help_1)
    
    # Clear the chart frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    try:
    
       
        # Call Conversion and capture the fig
        fig = xtr.Conversion(
            300 * np.ones(len(xtr.Beta)),
            950 * np.ones(len(xtr.Beta))
        )
    
        xtr.Conversion(300*np.ones(len(xtr.Beta)),
                   950*np.ones(len(xtr.Beta)))
       
        # Insert the figure into the frame using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        button_graph3.grid_forget()
        button_graph4.grid(row=1, column=0)    

    except:
        messagebox.showerror("unexpected error")


# the fourth graph is created
def funcion4():
    global fig,label2,text_help_1,xtr,ace,isoTables,aVy
    text_help_1="Pre-exponential factor\nThe pre-exponential factor is computed by means of the so-called compensation effect, which \nimplies a linear relation between the pre-exponential factor and the activation energy:\n $\ln{A}=a+bE$ \nA linear regression is computed over a set of {$E_{i}$,$\ln{A_{i}}$} to obtain the parameters $a$ and $b$.\nThe values of {$E_{i}$,$\ln{A_{i}}$} are obatined from fitting different models $f(\alpha)_{i}$ (defined in the \npicnik.rxn_models submodule) to the experimental data\nAll this information is returned from the ActivationEnergy.compensation_effect method"
    label2.config(text=text_help_1)
    # Clear the chart frame
    for widget in frame.winfo_children():
        widget.destroy()

    try:
        # Obtain the data and calculate activation energy
        isoTables = xtr.Isoconversion(d_a=0.005)
        ace = pnk.ActivationEnergy(xtr.Beta, xtr.T0, isoTables)
        aVy = ace.aVy((5, 380), var='time', p=0.90)
    
       # Get the figure from Ea_plot()
        fig = ace.Ea_plot()
    
        # Insert the figure into the frame using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
        button_graph4.grid_forget()
        button_graph5.grid(row=1, column=0)    

    except:
        messagebox.showerror("unexpected error")


# the fifth graph is created
def funcion5():
    global fig, canvas,label2,text_help_1,ace,aVy,compensation,isoTables
    text_help_1 = "--"
    label2.config(text=text_help_1)

    # Clear the chart frame
    for widget in frame.winfo_children():
        widget.destroy()

    try:
       
        
        compensation = ace.compensation_effect(
            0,
            aVy[2],
            aVy[3],
            error_m='r_Lin'
        )

        
        fig = Figure(figsize=(12, 9), dpi=100)
        ax = fig.add_subplot(111)
        print("__")
        print(ace.compensation_effect( 0,
         aVy[2],
         aVy[3],
         error_m='r_Lin'))
        print("___")
        
        
        ax.errorbar(
            aVy[0],
            compensation[0],
            yerr=compensation[1],
            fmt='o',
            color='blue'
        )
        ax.set_xlabel(r'$\alpha$')
        ax.set_ylabel(r'$\ln(A_{\alpha})$')
        ax.set_title("Compensation Chart")
        ax.grid(True)

         # Insert the figure into the frame using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        
        button_graph5.grid_forget()
        button_graph6.grid(row=1, column=0)    
        

    except Exception as e:
        import traceback
        label2.config(text=f"Error generating graph:\n{e}")
        print(traceback.format_exc())
            
   
    
# the sixth graph is created
def funcion6():
    global fig,label2,text_help_1,ace,isoTables,aVy,compensation,g_a
    text_help_1 = (
        "As noted by inspection of the plot of $\ln{A}$ vs $\alpha$, the value of $\ln{A}$ (~ 10.6) differs from the progammed one (12), giving thus an unreliable reconstruction, which is why g_r doesn reproduced the simulated data. If one uses the programmed value for $\ln{A}$ and the computed values with the `aVy(` method (g_r2) there is still a discrepancy between the computed data and the real model. Finally, by using the average of the activation energy array (g_r3) we recover the simulated model. The moral is, the `compensation_effect(` (as programmed in picnik) is unreliable and if you wish to recompute numerically $g(\alpha)$, you need to be sure that the process is single step and use the averge activation energy. Isothermal prediction For this example, the conversion as a function of time is given by: $\alpha(t) = 1-\exp{[-A\exp(-\frac{E}{RT})t]} $ We compare the results of the computed predictions with three picnik methods, each based on a different equation: a) Model based prediction:          $t_{\alpha_{i}} = \frac{\sum_{i}g(\alpha_{i})}{A\exp{(-\frac{E}{RT_{0}})}}$   ...(1) b) Isoconversion prediction A:      $t_{\alpha_{i}} = \frac{\int_{t_{\alpha_{0}}}^{t_{\alpha_{i}}}\exp(-\frac{E}{RT(t)})}{\exp{(-\frac{E}{RT_{0}})}}$   ...(2) c) Isoconversion prediction B:      $J[E_{\alpha},T(t)]=J[E_{\alpha},T_{0}]$   ...(3) As it can be seen from the expressions above, the methods do not compute conversion as a funciton of time, but they compute the time required to reach a given conversion The next three cells have the following contents:The first one, defines conversion as a function of time according to the F1 model and creates tima and conversion arrays ti plot. The second one has the three tipes of prediction according to the equations above The third one is a plot of the predictions and the model It is clear that all three equations give accurate isothermal predictions. Althoug we recommend the one of equation (3) as it implies less assumptions about the process"    
    )
    label2.config(text=text_help_1)

    # Clear the chart frame
    for widget in frame.winfo_children():
        widget.destroy()

    try:
            
       # Get data and calculate
      
        compensation = ace.compensation_effect(
            0,
            aVy[2],
            aVy[3],
            error_m='r_Lin'
        )
    
        # Get figure and g(alpha) from reconstruction method
        fig, g_a = ace.reconstruction(
            aVy[2],
            np.exp(compensation[0]),
            xtr.Beta[0]
        )
    
       # Insert the figure into the frame using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
    
        button_graph6.grid_forget()
        button_graph7.grid(row=1, column=0)    
    
    except:
        messagebox.showerror("unexpected error")




def alpha_F1_iso(t,A,E,isoT):
    
    return 1- np.exp(-A*np.exp(-E/(0.0083144626*isoT))*t)



# the seventh graph is created
def funcion7():
    global fig, aVy, g_a,compensation,ace

    text_help_1 = (
        "-----"
    )
    label2.config(text=text_help_1)

    # Clear the chart frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    try:    
    
        isoTables = xtr.Isoconversion(d_a=0.005)
        ace = pnk.ActivationEnergy(xtr.Beta, xtr.T0, isoTables)    
    
        # Create a new figure 
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
    
        time = np.linspace(0, 200, len(aVy[0]))  # Time arrays to compute the theoretical conversion values
        alp = alpha_F1_iso(time, np.exp(12), 75, 575)  # Theoretical conversion
    
        # Predictions
        tim_pred1 = ace.t_isothermal(aVy[2], compensation[0], 575, col=0, g_a=g_a, alpha=aVy[0])  # eq (1)
        tim_pred2 = ace.t_isothermal(aVy[2], compensation[0], 575, col=0, isoconv=True)           # eq (2)
        ap, Tp, tp = ace.modelfree_prediction(aVy[2], B=0, isoT=575, alpha=0.999, bounds=(10, 10))  # eq (3)
        print("tim_pred1:", tim_pred1)
        print("type(tim_pred1):", type(tim_pred1))
        
        ax.plot(time, alp, alpha=0.5, label=r'$\alpha(t) = 1-\exp{[-A\exp(-\frac{E}{RT})t]}$')
        ax.plot(tim_pred1[::13], aVy[0][::13], '<', c='#966B60', label='eq (1)')
        ax.plot(tim_pred2[::7], aVy[0][1:-1:7], '.', c='#169C09', label='eq (2)')
        ax.plot(tp[::8], ap[::8], '*', c='#EB6A49', label='eq (3)')
    
        ax.legend()
        ax.set_xlabel('Time (min)')
        ax.set_ylabel('Conversin α')
        ax.set_title('Comparison of prediction methods')
    
        # Insert the figure into the frame using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
            
        button_graph7.grid_forget()
        button_graph8.grid(row=1, column=0)          

    except:
        messagebox.showerror("unexpected error")
        


# the eighth graph is created
def funcion8():
    global fig, ace,ap2, Tp2, tp2 

    text_help_1 = (
        "-------"
    )
    label2.config(text=text_help_1)

    # Clear the chart frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    try:    
        
        #create a new figure
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
    
        # Prediction
        ap2, Tp2, tp2 = ace.modelfree_prediction(aVy[2], B=10, alpha=0.999, bounds=(10, 10))
    
       
        ax.plot(tp2, ap2, '.', label='Prediction')
        ax.plot(xtr.t[1], xtr.alpha[1], label="'Experimental data' (simulated)")
    
        ax.set_ylabel(r'Conversion ($\alpha$)')
        ax.set_xlabel('Time [min]')
        ax.legend(loc='upper left')
    
        # Insert the figure into the frame using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        
        button_graph8.grid_forget()
        button_open_files.grid(row=1, column=0)    
        


    except:
        messagebox.showerror("unexpected error")



# application name and version
def about():    
    messagebox.showinfo("about", "picnik aplicacion\nVersion 1.0\n https://doi.org/10.1016/j.cpc.2022.108416")
    
    
    
# save file    
def save_files():
    
    try:
        global ace,ap2, Tp2, tp2 
    
        """ Activation energy """
        ace.export_Ea()
        "Kinetic triplet"
        ace.export_kinetic_triplet(aVy[0][1::], aVy[2][1::], compensation[0][1::], g_a, name="kinetic_triplet.csv" )
        "Prediction"
        ace.export_prediction(ap2,Tp2,tp2)
       
    except:
        messagebox.showwarning("save file", "There is no file to save..")



#save graph
def save_graph():
    global fig
    if fig is None:
        messagebox.showwarning("save graph", "No graph to save.")
        return

    file = filedialog.asksaveasfilename(
        #defaultextension=".png",
        filetypes=[("SVG files", "*.svg"),
                   ("PNG files", "*.png")
                   ]
    )
    if file:
        fig.savefig(file, dpi=300, bbox_inches='tight')
        messagebox.showinfo("save graph", f"Chart saved in:\n{file}")
        
        
        
#tutorial
def tutorial():
   
    if sys.platform.startswith('darwin'):  # macOS
        subprocess.call(('open',"tutorial.pdf"))
    elif os.name == 'nt':  # Windows
        os.startfile("tutorial.pdf")
    elif os.name == 'posix':  # Linux
        subprocess.call(('xdg-open',"tutorial.pdf"))


#exit the application
def salir():
    root.destroy()

        

root.mainloop()
