import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib      # ve si jala el ejecutable
matplotlib.use('TkAgg')# con estas lineas
import matplotlib.pyplot as plt
import picnik as pnk
import numpy as np
import chardet
import os
import sys
import subprocess
import pandas as pd


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Picnik desktop edition")
        self.geometry("1000x800")

        # 1. variables  de la interfaz
       
        self.fase_actual = tk.IntVar(value=1)
        self.var_usuario = tk.StringVar(value="Admin")
        self.var_dato_extra = tk.StringVar(value="")
        self.var_puntos = tk.IntVar(value=0)
        self.var_tema = tk.StringVar(value="Oscuro")
        self.var_status = tk.StringVar(value="Inicio")

        # 2 variables de apoyo picnik
     
        self.one_step=[]
        self.numero_de_archivos=0
        self.fig=None
        self.xtr=None
        self.Beta=None
        self.T0=None
        self.fix1_conversion=[]
        self.fix2_conversion=[]
        self.fix_aux_conversion=[]
        self.d_a1=0
        self.p1=0
        self.aVy=None
        self.method_used=None 
        self.isoTables=None    
        self.resultado=None   
        self.methods=""
        self.compensation_inicio=0
        self.compensation_error='r_Lin'
        self.ace=None
        self.g_a=None
        self.compensation=None
        self.ap2=None
        self.Tp2=None
        self.tp2=None
        self.canvas=None
        # menu
        self._configurar_menu()

        # estructura frames
        self.frame_contenedor = tk.Frame(self) 
        self.frame_contenedor.pack(fill="both", expand=True)

        self.frame_header = tk.LabelFrame(self.frame_contenedor, pady=10)
        self.frame_header.pack(side="top", fill="x", padx=10, pady=5)

        self.frame_grafico = tk.LabelFrame(self.frame_contenedor)
        self.frame_grafico.pack(side="bottom", fill="both", expand=True, padx=10, pady=5)
        etiqueta = tk.Label(self.frame_grafico, text="Picnik desktop edition",font=("Arial", 34, "bold"))
        etiqueta.pack(expand=True)

        # diccionario
        self.config_fases = {
            1: [("Open Files", self.open_files)],
            2: [("View_graphs", self.view_graphs)],
            3: [("a1", self.g1), ("a2",self.g2),("a3", self.g3),("a4", self.g4),("a5", self.g5),("a6", self.g6),],
            4: [("help image", self.g4), ("enter initial temperatures", self.input_temp_i),("enter final temperatures", self.input_temp_f)],
            5: [("Conversion", self.conversion)],
            6: [("input data", self.input_data_isoconversion),("Iso Table", self.ver_table),("export data", self.export_table),("Isoconversion", self.ver_isoconversion)],
            7: [("input date compensation", self.input_date_compensation), ("ver compensation", self.ver_compensation)],
            8: [("input date reconstruccion", self.fase_4_exportar), ("ver  reconstruccion", self.ver_recontruction)],
            9: [("input aaa", self.fase_4_exportar), ("ver aaa", self.ver_aaa)],
            10: [("input prediction", self.input_prediction), ("ver prediction", self.ver_prediction)],
            11: [("ggg", self.fase_4_graficar), ("hhh", self.fase_4_exportar), ("kkk", self.save_files_finales)],
                     
        }

        self.actualizar_botones()


    def _configurar_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # --- menu files---
        menu_files = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Files", menu=menu_files)
        menu_files.add_command(label="Open Files", command=self.open_files)
        menu_files.add_command(label="Save Files", command=self.funcion_guardar_archivos)
        menu_files.add_separator()
        menu_files.add_command(label="Exit", command=self.salir)

        # --- menu images ---
        menu_images = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Images", menu=menu_images)
        menu_images.add_command(label="Save Image", command=self.funcion_guardar_imagen)

        # ---menu help ---
        menu_help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=menu_help)
        menu_help.add_command(label="About", command=self.funcion_acerca_de)
        menu_help.add_command(label="Tutorial", command=self.funcion_tutorial)

    def actualizar_botones(self):
        # Limpia y crea los botones de acción y de navegación
        for widget in self.frame_header.winfo_children():
            widget.destroy()

        fase = self.fase_actual.get()
        
        # --- button previous (aparece desde la segunda fase) ---
        if fase > 1:
            ttk.Button(self.frame_header, text="<< Previous", 
                       command=self.go_previous).pack(side="left", padx=5)

        # --- button action (del diccionario) ---
        if fase in self.config_fases:
            for texto, comando in self.config_fases[fase]:
                ttk.Button(self.frame_header, text=texto, command=comando).pack(side="left", padx=5)

        # --- button next ---
        if fase < len(self.config_fases):
            ttk.Button(self.frame_header, text="Next >>", 
                       command=self.go_next).pack(side="right", padx=5)
        else:
            # en la ultima fase, el botón de la derecha permite reiniciar
            ttk.Button(self.frame_header, text="Reiniciar Todo", 
                       command=self.reiniciar).pack(side="right", padx=5)

    # --- logica navegacion ---
    
    #ir siguiente
    def go_next(self):
        self.fase_actual.set(self.fase_actual.get() + 1)
        self.actualizar_botones()
    
    #ir anterior
    def go_previous(self):
        self.fase_actual.set(self.fase_actual.get() - 1)
        self.actualizar_botones()
    
    #reiniciar
    def reiniciar(self):
        
        # borramos primero el canvas y luego ponemos la etiqueta , probar haber si funciona correctamente
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        self.fase_actual.set(1)
        self.actualizar_botones()
        self.fig=None
        etiqueta = tk.Label(self.frame_grafico, text="Picnik desktop edition",font=("Arial", 34, "bold"))
        etiqueta.pack(expand=True)
        
        #############################################################################
        # aqui me falta actualizar las variables de clase
        # si es que declaro alguna nueva al final
        # hay que copiar las variables de clase para asegurar 
        # que  estan todas
        #
        self.one_step=[]
        self.numero_de_archivos=0
        self.fig=None
        self.xtr=None
        self.Beta=None
        self.T0=None
        self.fix1_conversion=[]
        self.fix2_conversion=[]
        self.fix_aux_conversion=[]
        self.d_a1=0
        self.p1=0
        self.aVy=None
        self.method_used=None 
        self.isoTables=None    
        self.resultado=None   
        self.methods=""
        self.compensation_inicio=0
        self.compensation_error='r_Lin'
        self.ace=None
        self.g_a=None
        self.compensation=None
        self.ap2=None
        self.Tp2=None
        self.tp2=None
        self.canvas=None
        # 
        # 
        # 
        # 
        # 
        #################################################################################


    #salir de la aplicacion
    def salir(self):
        if messagebox.askyesno("Quit", "Do you want to exit the application?"):
            self.destroy()


    # funciones de apoyo mientras se realiza la aplicacion luego las borro
    
    def menu_placeholder(self): pass
    def fase_3_calcular(self): pass
    def fase_3_ajustar(self): pass
    def fase_4_graficar(self): pass
    def fase_4_exportar(self): pass



    # Function to detect encoding
    def detectar_encoding(self,file, num_bytes=10000):
        with open(file, 'rb') as f:
            raw_data = f.read(num_bytes)
        result = chardet.detect(raw_data)
        return result['encoding'], result['confidence']


    def open_files(self): 
        
        # delete the contents of one_step
        self.one_step.clear()

        try:
                
            files = filedialog.askopenfilenames(
                filetypes=[("valid files", "*.csv *.txt")]
            )
        
            #validation of two more files
            if len(files) > 1:
                self.one_step.clear()
                self.one_step.extend(files)
                print("selected files:")
                for file in self.one_step:
                    print(file)
                
                self.numero_de_archivos= len(files)      
            
            else:
                print("No file selected.")
                messagebox.showinfo(
                    title="Two or more files, please",
                    message="Two or more files, please"
                )
                self.one_step.clear()
            
            
        
        except:
            messagebox.showerror("unexpected error")

    def draw_fig(self):
        for widget in self.frame_grafico.winfo_children():
                    widget.destroy()

        #configuracion cabvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.draw()

        # 3. TOOLBAR (Nota: quitamos 'self.' de toolbar para que no guarde basura)
        toolbar = NavigationToolbar2Tk(self.canvas, self.frame_grafico, pack_toolbar=False)
        toolbar.update()

        # el orden importa para que no se encimen
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # empaquetado manual para asegurar el orden
        # el toolbar abajo y el gráfico arriba
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
                        


    def view_graphs(self):
        
           
            try:
                # Verificación de archivos seleccionados (self.one_step debe estar definida)
                if not hasattr(self, 'one_step') or not self.one_step:
                    messagebox.showwarning("Warning", "No files selected to process.")
                    return

                # --- detección de encodings ---
                codificaciones = []
                for file in self.one_step:
                    encoding, conf = self.detectar_encoding(file)
                    if encoding:
                        codificaciones.append(encoding)
                    else:
                        messagebox.showerror("Error", f"The encoding could not be detected: {file}")
                        return
            
                encoding_set = set(codificaciones)
                if len(encoding_set) == 1:
                    encoding_final = encoding_set.pop()
                else:
                    messagebox.showerror(
                        "Encoding incompatibility",
                        "The files have different encodings:\n" + 
                        "\n".join(f"{f} => {e}" for f, e in zip(self.one_step, codificaciones))
                    )
                    return 

                # --- extracción de datos y generación de fig ---
                # Asumiendo que pnk ya está importado
                self.xtr = pnk.DataExtraction()
                
                self.fig, self.Beta, self.T0  = self.xtr.read_files(self.one_step, encoding=encoding_final)
            
                self.draw_fig()

            except Exception as e:
                # error inesperado
                messagebox.showerror("Unexpected error", f"Details: {str(e)}")




    #------------transition image-------------------------------

    def g1(self):
        try:       
            self.fig=self.xtr.plot_data(x_data='time',y_data='TG', x_units='min', y_units='%')   
            self.draw_fig()

        except Exception as e:
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")
        
    def g2(self):
        try:
            self.fig=self.xtr.plot_data(x_data='time',y_data='DTG', x_units='min', y_units='%/min')   
            self.draw_fig()

        except Exception as e:
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")

    def g3(self):
        try:
           
            self.fig=self.xtr.plot_data(x_data='time',y_data='dT/dt', x_units='min', y_units='K/min')   
            self.draw_fig()

        except Exception as e:
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")       

    def g4(self):
        try:
            self.fig=self.xtr.plot_data(x_data='temperature',y_data='TG', x_units='K', y_units='%')   
            self.draw_fig()

        except Exception as e:
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")

    def g5(self):
        try:            
            self.fig=self.xtr.plot_data(x_data='temperature',y_data='DTG', x_units='K', y_units='%/min')   
            self.draw_fig()

        except Exception as e:
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")

            

    def g6(self):
        try:
            self.fig=self.xtr.plot_data(x_data='temperature',y_data='dT/dt', x_units='K', y_units='K/min')   
            self.draw_fig()

        except Exception as e:            
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")

        



    def input_temp_i(self):
        self.fix2_conversion=[]
        self.fix_temp()
        self.fix1_conversion=self.fix_aux_conversion.copy()
        
    def input_temp_f(self):
        self.fix_temp()
        self.fix2_conversion=self.fix_aux_conversion.copy()
        
        #asegurarse que arreglo 2 sea mayor al arreglo 1
        
        for i in range(self.numero_de_archivos):
            try:
                if self.fix1_conversion[i] >=   self.fix2_conversion[i]:
                    
                    messagebox.showwarning("warning ","The final temperatures must be higher than the initial temperatures.")
                    self.fix2_conversion=self.fix_aux_conversion.copy()
                    break
            except Exception as e:
                messagebox.showwarning("warning ","Please enter initial temperatures and then enter final temperatures")
                break
                
    #fix temperatures
    #arreglo de temperaturas            
    def fix_temp(self):

        while True:

            ventana_formulario = tk.Toplevel(self)
            ventana_formulario.title("Ingreso de datos")
            ventana_formulario.geometry("400x350")
            ventana_formulario.resizable(False, False)

            self.fix_aux_conversion.clear()  # ← importante para no acumular datos viejos
            contador = 1
            
            
            for b in range(len(self.Beta)):
                print(f'{self.Beta[b]:.1f}')


            def agregar():
                nonlocal contador
                valor = entrada.get()           
                if valor == "":         #--------no se avanza si el usuario deja el valor vacio--------
                    return
                elif valor.isdigit()== False:
                    messagebox.showwarning("warning","enter only whole positive numbers")
                    return #se manda una advertencia si el usuario ingresa un dato que no sea un numero entero y no se deja avanzar  

                if contador <= self.numero_de_archivos:
                    self.fix_aux_conversion.append(int(valor))#tenia el error aqui
                    entrada.delete(0, tk.END)
                    etiqueta_arreglo.config(text=f"Arreglo: {self.fix_aux_conversion}")

                    contador += 1

                    if contador <= self.numero_de_archivos:
                        etiqueta_titulo.config(text=f"Ingrese temperatura β={self.Beta [contador-1]:.1f}")

                    else:
                        etiqueta_titulo.config(text="Ingreso completado")
                        entrada.config(state="disabled")
                        boton_agregar.config(state="disabled")
                        boton_aceptar.pack(pady=10)

            def borrar_ultima():
                nonlocal contador
                if self.fix_aux_conversion:
                    self.fix_aux_conversion.pop()
                    contador -= 1

                    etiqueta_arreglo.config(text=f"Arreglo: {self.fix_aux_conversion}")
                    etiqueta_titulo.config(text=f"Ingrese temperatura β={self.Beta [contador-1]:.1f}")

                    entrada.config(state="normal")
                    boton_agregar.config(state="normal")
                    boton_aceptar.pack_forget()

            def aceptar():
                ventana_formulario.destroy()

            # Widgets
            etiqueta_titulo = tk.Label(ventana_formulario, text=f"Ingrese temperatura β={self.Beta [0]:.1f}")
            etiqueta_titulo.pack(pady=10)

            entrada = tk.Entry(ventana_formulario)
            entrada.pack(pady=10)

            boton_agregar = tk.Button(ventana_formulario, text="Agregar", command=agregar)
            boton_agregar.pack(pady=10)

            boton_borrar = tk.Button(ventana_formulario, text="Borrar última", command=borrar_ultima)
            boton_borrar.pack(pady=10)

            etiqueta_arreglo = tk.Label(ventana_formulario, text="Arreglo: []")
            etiqueta_arreglo.pack(pady=10)

            boton_aceptar = tk.Button(ventana_formulario, text="Aceptar", command=aceptar)

            self.wait_window(ventana_formulario)
            
            return self.fix_aux_conversion

    def conversion(self):
        print("----------------------------------")
    
        try:
           
            self.fig=self.xtr.Conversion(self.fix1_conversion,self.fix2_conversion)

            self.draw_fig()

        except Exception as e:
            
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")

    #-----------------------------------------------------------------------------------#

    def input_data_isoconversion(self):

        fuente = ("Helvetica", 12, "bold")
        
        ventana_isoconversion = tk.Toplevel(self)
        ventana_isoconversion.title("Ingreso de datos")
        ventana_isoconversion.geometry("400x450")
        ventana_isoconversion.resizable(False, False)

        # --- Campo 1: d_a ---
        tk.Label(ventana_isoconversion, text="d_a = ").pack(pady=5)
        valor_inicio = tk.DoubleVar(value=0.005)
        spinbox_rango = tk.Spinbox(ventana_isoconversion, from_=0, to=0.99, 
                                increment=0.001, state="readonly", 
                                textvariable=valor_inicio,font=fuente,fg="black")
        spinbox_rango.pack(pady=5)

        # --- Campo 2: Method ---
        tk.Label(ventana_isoconversion, text="Method:").pack(pady=5)
        cinco_metodos = ["aVy", "Vy", "Fr", "KAS", "OFW"]
        combo_methods = ttk.Combobox(ventana_isoconversion, values=cinco_metodos, state="readonly")
        combo_methods.set("aVy") # Valor por defecto
        combo_methods.pack(pady=5)

        # --- Campo 3: sss (Condicional) ---
        etiqueta_titulo2 = tk.Label(ventana_isoconversion, text="p:")
        valor_inicio2 = tk.DoubleVar(value=0.80)
        spinbox_rango2 = tk.Spinbox(ventana_isoconversion, from_=0, to=0.99, 
                                    increment=0.01, state="readonly", 
                                    textvariable=valor_inicio2, font=fuente,fg="black")

        def actualizar_visibilidad(event=None):
            if combo_methods.get() in ["aVy", "Vy"]:
                etiqueta_titulo2.pack(pady=5)
                spinbox_rango2.pack(pady=5)
            else:
                spinbox_rango2.pack_forget()
                etiqueta_titulo2.pack_forget()

        combo_methods.bind("<<ComboboxSelected>>", actualizar_visibilidad)
        actualizar_visibilidad() # Ejecución inicial

        # --- Función para guardar los datos ---
        def guardar_y_cerrar():
            
            #----------------------------------------------------------------------------------
            # Aquí es donde realmente capturamos el valor final antes de cerrar o usar los datos
            self.d_a1 = valor_inicio.get()
            self.p1 = valor_inicio2.get()
            self.methods= combo_methods.get()
            #-----------------------------------------------------------------------------------
            #si declaro aqui tengo problemas si regreso entonces probare de otra forma
            #self.isoTables = self.xtr.Isoconversion(d_a=self.d_a1)    
            print(f"Variables actualizadas: d_a1={self.d_a1}, p1={self.p1}, Metodo={self.methods}")
            ventana_isoconversion.destroy()

        # --- Botón OK ---
        button_algo = tk.Button(ventana_isoconversion, text="Aceptar", command=guardar_y_cerrar)
        button_algo.pack(side=tk.BOTTOM, pady=20)

        
    def ver_table(self):
        
        try:
            # Limpiar el frame
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()

            # 1. Obtener datos y asegurar que self.isoTables sea un DataFrame
            self.isoTables = self.xtr.Isoconversion(d_a=self.d_a1)
            # Si es una tupla, extraemos el array
            datos_array = self.isoTables[0] if isinstance(self.isoTables, tuple) else self.isoTables
            
            # Guardamos como DataFrame (fundamental para exportar luego)
            #resultado = pd.DataFrame(datos_array, columns=["Tiempo_Predicho"])

            # 2. Visualización tipo bloque de texto (como pediste)
            text_area = tk.Text(self.frame_grafico, font=("Consolas", 10), padx=10, pady=10)
            
            # Insertamos el texto formateado como el bloque que mostraste
            text_area.insert(tk.END, str(datos_array)) 
            
            text_area.config(state=tk.DISABLED)
            text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron preparar los datos: {e}")

        self.fig=None


    def export_table(self):
        self.isoTables = self.xtr.Isoconversion(d_a=self.d_a1) # crear una variable con este valor por default
        #print(self.isoTables)
        try:
           
            # Extraemos los componentes de la tupla
            y_values = self.isoTables[0]  # La columna de la izquierda (0.002027...)
            x_values = self.isoTables[1]  # Los datos de las columnas ($\beta$)
            
            # Creamos el DataFrame
            # Nota: Si esto falla, intenta con: df = pd.DataFrame(self.isoTables[1], index=self.isoTables[0])
            df = pd.DataFrame(x_values)
            df.index = y_values
            
            # Definir encabezados
            #df.columns = [
                #"β= 2.50 K/min", 
                #"β= 5.00 K/min", 
                #"β= 10.00 K/min", 
                #"β= 15.00 K/min", 
                #"β= 20.00 K/min"
            #]

        except Exception as e:
            print(f"Error al organizar los datos: {e}")
            # Si falla lo anterior, intentamos una conversión forzada a 2D
            df = pd.concat([pd.DataFrame(i) for i in self.isoTables], axis=1)

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivo CSV", "*.csv")],
            title="Guardar tabla de resultados"
        )

        if filepath:
            df.to_csv(filepath, index=True, encoding='utf-8-sig', sep=';')
            print(f"¡Listo! Guardado en: {filepath}")
    

    def ver_isoconversion(self):

        try:
            
            #----------------------------------------------------------------------------------------------------#
            #-------hasta aqui esta es la unica linea que cambie en el ejemplo va antes de la imagen conversion--#
            #-------en la aplicacion va despues de la imgen de conversion----------------------------------------#
            self.isoTables = self.xtr.Isoconversion(d_a=self.d_a1) # crear una variable con este valor por default
            #----------------------------------------------------------------------------------------------------#
                
            self.ace = pnk.ActivationEnergy(self.Beta, self.T0, self.isoTables)   #falta cambiar esta parte     
           
            if self.methods == "aVy":
                self.method_used = self.ace.aVy((5, 380), var='time', p=self.p1)  #opcion para escojer metodo  de los cinco
            elif self.methods == "Vy":
                self.method_used = self.ace.Vy((5, 380),method='senum-yang')
                #me falta especificar la tupla
            elif self.methods == "Fr":
                self.method_used =self.ace.Fr()
            elif self.methods =="KAS":
                self.method_used = self.ace.KAS()
            elif self.methods =="OFW":
                self.method_used = self.ace.OFW()
            else:
                messagebox.showerror("error","choose a method")

            #-----------------------------
            #probando esta linea
            self.aVy=self.method_used
            #-----------------------------
            #    
            # Get the figure from Ea_plot()
            self.fig = self.ace.Ea_plot()
        
            self.draw_fig()
            #print(self.isoTables)
        except:
            messagebox.showerror("unexpected error")

    
    
    
    
    def input_date_compensation(self):
        fuente = ("Helvetica", 12, "bold")
        
        ventana_compensation = tk.Toplevel(self)
        ventana_compensation.title("Ingreso de datos")
        ventana_compensation.geometry("400x450")
        ventana_compensation.resizable(False, False)

        # --- Campo 1: d_a ---
        opciones_beta = []
        for i in range(self.numero_de_archivos):
            texto = f"Beta {i} = {self.Beta[i]:.1f}"
            opciones_beta.append(texto)
        
        # 2. Usamos StringVar porque el Spinbox ahora contiene texto (Beta 0 = ...)
        valor_texto = tk.StringVar(value=opciones_beta[0])
        
        tk.Label(ventana_compensation, text="Seleccione Beta:").pack(pady=5)
        
        # 3. Spinbox configurado con el array
        spinbox_rango = tk.Spinbox(
            ventana_compensation, 
            values=opciones_beta, 
            state="readonly", 
            textvariable=valor_texto, # Vinculamos la variable
            font=fuente,
            fg="black",
            width=20
        )
        spinbox_rango.pack(pady=5)

        # --- Campo 2: Method ---
        tk.Label(ventana_compensation, text="y = ").pack(pady=5)
        options = ["r_Lin", "r_NL", "mse_NL"]
        combo_options = ttk.Combobox(ventana_compensation, values=options, state="readonly")
        combo_options.set("r_Lin") # Valor por defecto
        combo_options.pack(pady=5)

        def actualizar_visibilidad(event=None):
            pass
        
        combo_options.bind("<<ComboboxSelected>>", actualizar_visibilidad)
        actualizar_visibilidad() # Ejecución inicial


        # --- Función para guardar los datos ---
        def guardar_y_cerrar():
            
            #----------------------------------------------------------------------------------
            # Aquí es donde realmente capturamos el valor final antes de cerrar o usar los datos
            #lo converti a enteros al parecer se capturaba como string
            self.compensation_inicio = opciones_beta.index(valor_texto.get())
            self.compensation_error= combo_options.get()
            #-----------------------------------------------------------------------------------

        
            print(f"Variables actualizadas: B={self.compensation_inicio}, Linear={self.compensation_error}")
            ventana_compensation.destroy()

        # --- Botón OK ---
        button_algo = tk.Button(ventana_compensation, text="Aceptar", command=guardar_y_cerrar)
        button_algo.pack(side=tk.BOTTOM, pady=20)
        
        
        
    # the fifth graph is created
    def ver_compensation(self):
        
        #me falta cambiar el 0 y el error_m    

        try:
            
            self.compensation = self.ace.compensation_effect(
                self.compensation_inicio,
                #----------    revisar el avy que este bien definido   --------
                #  ------    ver de donde viene checar en ventana principal ---
                self.aVy[2],
                self.aVy[3],
                error_m=self.compensation_error
            )
    
            self.fig = Figure(figsize=(12, 9), dpi=100)
            ax = self.fig.add_subplot(111)
            
            print("__")
            print(self.ace.compensation_effect( self.compensation_inicio,
            self.aVy[2],
            self.aVy[3],
            error_m=self.compensation_error))
            print("___")
            
            
            ax.errorbar(
                self.aVy[0],
                self.compensation[0],
                self.compensation[1],     #probar  con esta linea
                #yerr=self.compensation[1],
                fmt='o',
                color='blue'
            )
            ax.set_xlabel(r'$\alpha$')
            ax.set_ylabel(r'$\ln(A_{\alpha})$')
            ax.set_title("Compensation Chart")
            ax.grid(True)

            self.draw_fig()
    
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron preparar los datos: {e}")                
    
    #-----------------------------------------------------------------------------------#
    
    def input_recontruction(self):
       pass

    def ver_recontruction(self):
        try:
        # 1. Limpiar el frame correctamente
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()
    
            # 2. Generar la figura (asegúrate de que self.ace.reconstruction 
            #    devuelva un objeto figure de matplotlib)
            self.fig, self.g_a = self.ace.reconstruction(
                self.aVy[2],
                np.exp(self.compensation[0]),
                self.Beta[0]
            )
    
            self.draw_fig()

        except Exception as e:
            print(f"Error al reconstruir: {e}")
           

    def input_aaa(self):
        pass
    def ver_aaa(self):
        try:
        # 1. Limpiar el frame correctamente
           
            #self.isoTables = self.xtr.Isoconversion(d_a=0.005)
            #self.ace = pnk.ActivationEnergy(self.Beta, self.T0, self.isoTables)    
        
            # Crear una nueva figura y eje
            self.fig = Figure(figsize=(6, 4), dpi=100)
            ax = self.fig.add_subplot(111)
        
            def alpha_F1_iso(t,A,E,isoT):
                return 1- np.exp(-A*np.exp(-E/(0.0083144626*isoT))*t)
            
            time = np.linspace(0,200,len(self.aVy[0]))                                    # Time arrays to comupute the theoretical conversion values
            alp  = alpha_F1_iso(time,np.exp(12),75,575)                               # Theoretical conversion with E = 75 kJ/mol and ln(A/min)=12
            # Predicciones
            tim_pred1 = self.ace.t_isothermal(self.aVy[2], self.compensation[0], 575, col=0,g_a=self.g_a, alpha=self.aVy[0])  # eq (1)
            tim_pred2 = self.ace.t_isothermal(self.aVy[2], self.compensation[0], 575, col=0, isoconv=True)           # eq (2)
            ap, Tp, tp = self.ace.modelfree_prediction(self.aVy[2], B=0, isoT=575, alpha=0.999, bounds=(10, 10))  # eq (3)
            
            ax.plot(time, alp, alpha=0.5, label=r'$\alpha(t) = 1-\exp{[-A\exp(-\frac{E}{RT})t]}$')
            ax.plot(tim_pred1[::13], self.aVy[0][::13], '<', c='#966B60', label='eq (1)')
            ax.plot(tim_pred2[::7], self.aVy[0][1:-1:7], '.', c='#169C09', label='eq (2)')
            ax.plot(tp[::8], ap[::8], '*', c='#EB6A49', label='eq (3)')
            
            # 3. Configurar la leyenda
            ax.legend()
            
            self.draw_fig()
        except Exception as e:
            print(f"Error al reconstruir: {e}")
        
    def input_prediction(self):
        pass
    def ver_prediction(self):
        try:    
           
            # Crear una nueva figura y eje
            self.fig = Figure(figsize=(6, 4), dpi=100)
            ax =self. fig.add_subplot(111)
        
            # Predicción
            self.ap2, self.Tp2, self.tp2 = self.ace.modelfree_prediction(self.aVy[2], B=10, alpha=0.999, bounds=(10, 10))
        
            # Graficar en el eje
            ax.plot(self.tp2, self.ap2, '.', label='Predicción')
            ax.plot(self.xtr.t[1], self.xtr.alpha[1], label="'Datos experimentales' (simulados)")
        
            ax.set_ylabel(r'Conversión ($\alpha$)')
            ax.set_xlabel('Tiempo [min]')
            ax.legend(loc='upper left')
        
            self.draw_fig()

        except:
            messagebox.showerror("error inesperado")

    def save_files_finales(self):
    
        try:
            
            """ Activation energy """
            #modifique export_Ea() en picnik pero sigue sin generarse el archivo
            #regrese el archivo como estaba por que en el ejemplo si genera este .csv
            #en el ultimo ejemplo ya se genero el archivo
            try:
                self.ace.export_Ea()
            except:
                print("no jalo")
            
            "Kinetic triplet"
            self.ace.export_kinetic_triplet(self.aVy[0][1::], self.aVy[2][1::], self.compensation[0][1::], self.g_a, name="kinetic_triplet.csv" )
            "Prediction"
            self.ace.export_prediction(self.ap2,self.Tp2,self.tp2)
            
        except:
            messagebox.showwarning("save file", "There is no file to save..")

    #-----------------------------------------------------------------------------------#

    def funcion_guardar_archivos(self): 
        pass

    def funcion_guardar_imagen(self): 
        
        if self.fig is None:
            messagebox.showwarning("save image", "No image to save.")
            return

        file = filedialog.asksaveasfilename(
            #defaultextension=".png",
            filetypes=[("SVG files", "*.svg"),
                    ("PNG files", "*.png")
                    ]
        )
        if file:
            self.fig.savefig(file, dpi=300, bbox_inches='tight')
            messagebox.showinfo("save image", f"Chart saved in:\n{file}")
            

    def funcion_acerca_de(self): 
         messagebox.showinfo("about", "picnik aplicacion\nVersion 1.0\n https://doi.org/10.1016/j.cpc.2022.108416")
    

    def funcion_tutorial(self): 
        if sys.platform.startswith('darwin'):  # macOS
            subprocess.call(('open',"tutorial.pdf"))
        elif os.name == 'nt':  # Windows
            os.startfile("tutorial.pdf")
        elif os.name == 'posix':  # Linux
            subprocess.call(('xdg-open',"tutorial.pdf"))




if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop().ace.reconstruction