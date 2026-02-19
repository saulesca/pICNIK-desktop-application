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
import pandas as pd


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Picnik desktop edition")
        self.geometry("900x600")

        # 1. TUS 5 VARIABLES GLOBALES
        self.fase_actual = tk.IntVar(value=1)
        self.var_usuario = tk.StringVar(value="Admin")
        self.var_dato_extra = tk.StringVar(value="")
        self.var_puntos = tk.IntVar(value=0)
        self.var_tema = tk.StringVar(value="Oscuro")
        self.var_status = tk.StringVar(value="Inicio")


        self.one_step=[]
        self.numero_de_archivos=0
        self.fig=None
        self.xtr=None
        self.fix1_conversion=[]
        self.fix2_conversion=[]
        self.fix_aux_conversion=[]
        self.d_a1=0
        self.p1=0
        self.aVy=None 
        self.isoTables=None    
        self.resultado=None   
        self.methods=""


        # 2. MENÚ (FILES, IMAGES, HELP)
        self._configurar_menu()

        # 3. ESTRUCTURA DE FRAMES
        self.frame_contenedor = tk.Frame(self) 
        self.frame_contenedor.pack(fill="both", expand=True)

        self.frame_header = tk.LabelFrame(self.frame_contenedor, pady=10)
        self.frame_header.pack(side="top", fill="x", padx=10, pady=5)

        self.frame_grafico = tk.LabelFrame(self.frame_contenedor)
        self.frame_grafico.pack(side="bottom", fill="both", expand=True, padx=10, pady=5)
        etiqueta = tk.Label(self.frame_grafico, text="Picnik desktop edition",font=("Arial", 34, "bold"))
        etiqueta.pack(expand=True)

        # 4. DICCIONARIO DE FASES (Escalable)
        self.config_fases = {
            1: [("Open Files", self.open_files)],
            2: [("View_graphs", self.view_graphs)],
            3: [("a1", self.g1), ("a2",self.g2),("a3", self.g3),("a4", self.g4),("a5", self.g5),("a6", self.g6),],
            4: [("help image", self.g4), ("enter initial temperatures", self.input_temp_i),("enter final temperatures", self.input_temp_f)],
            5: [("Conversion", self.conversion)],
            6: [("input data", self.input_data_isoconversion), ("Isoconversion", self.ver_isoconversion)],
            7: [("Iso Table", self.ver_table),("export data", self.export_table)],
            8: [("eee", self.fase_4_graficar), ("fff", self.fase_4_exportar)],
            
            
        }

        self.actualizar_botones()

    def _configurar_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # --- MENÚ FILES ---
        menu_files = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Files", menu=menu_files)
        menu_files.add_command(label="Open Files", command=self.open_files)
        menu_files.add_command(label="Save Files", command=self.funcion_guardar_archivos)
        menu_files.add_separator()
        menu_files.add_command(label="Exit", command=self.salir)

        # --- MENÚ IMAGES ---
        menu_images = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Images", menu=menu_images)
        menu_images.add_command(label="Save Image", command=self.funcion_guardar_imagen)

        # --- MENÚ HELP ---
        menu_help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=menu_help)
        menu_help.add_command(label="About", command=self.funcion_acerca_de)
        menu_help.add_command(label="Tutorial", command=self.funcion_tutorial)

    def actualizar_botones(self):
        """Limpia y crea los botones de acción y de navegación"""
        for widget in self.frame_header.winfo_children():
            widget.destroy()

        fase = self.fase_actual.get()
        
        # --- BOTÓN PARA REGRESAR (Aparece a partir de la Fase 2) ---
        if fase > 1:
            ttk.Button(self.frame_header, text="<< Anterior", 
                       command=self.ir_anterior).pack(side="left", padx=5)

        # --- BOTONES DE ACCIÓN (Del diccionario) ---
        if fase in self.config_fases:
            for texto, comando in self.config_fases[fase]:
                ttk.Button(self.frame_header, text=texto, command=comando).pack(side="left", padx=5)

        # --- BOTÓN PARA AVANZAR ---
        if fase < len(self.config_fases):
            ttk.Button(self.frame_header, text="Siguiente Fase >>", 
                       command=self.ir_siguiente).pack(side="right", padx=5)
        else:
            # En la última fase, el botón de la derecha permite reiniciar
            ttk.Button(self.frame_header, text="Reiniciar Todo", 
                       command=self.reiniciar).pack(side="right", padx=5)

    # --- LÓGICA DE NAVEGACIÓN ---
    def ir_siguiente(self):
        self.fase_actual.set(self.fase_actual.get() + 1)
        self.actualizar_botones()

    def ir_anterior(self):
        self.fase_actual.set(self.fase_actual.get() - 1)
        self.actualizar_botones()

    def reiniciar(self):
        self.fase_actual.set(1)
        self.actualizar_botones()



    def salir(self):
        if messagebox.askyesno("Quit", "Do you want to exit the application?"):
            self.destroy()






    # --- TUS FUNCIONES (RELLENAR DESPUÉS) ---
    def menu_placeholder(self): pass



    
    def fase_3_calcular(self): pass
    def fase_3_ajustar(self): pass
    
    def fase_4_graficar(self): pass
    def fase_4_exportar(self): pass



      # --- MÉTODOS GENÉRICOS PARA EL MENÚ (RENOMBRAR AQUÍ) ---


    # Function to detect encoding
    def detectar_encoding(self,file, num_bytes=10000):
        with open(file, 'rb') as f:
            raw_data = f.read(num_bytes)
        result = chardet.detect(raw_data)
        return result['encoding'], result['confidence']


    def open_files(self): 
    
        self.one_step.clear()# delete the contents of one_step
        
        try:
                
            files = filedialog.askopenfilenames(
                filetypes=[("valid files", "*.csv *.txt")]
            )
        
            if len(files) > 1:#validation of two more files
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


    
    def view_graphs(self):
    
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        try:
            # Verificación de archivos seleccionados (self.one_step debe estar definida)
            if not hasattr(self, 'one_step') or not self.one_step:
                messagebox.showwarning("Warning", "No files selected to process.")
                return

            # --- Lógica de detección de encodings ---
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

            # --- Extracción de datos y generación de FIG ---
            # Asumiendo que pnk ya está importado
            self.xtr = pnk.DataExtraction()
            
            self.fig = self.xtr.read_files(self.one_step, encoding=encoding_final)
            #self.fig.subplots_adjust(left=0.05, right=0.95)
            # 2. Insertar la figura en el frame de abajo (self.frame_grafico)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True )
            
        except Exception as e:
            # Es mejor mostrar el error real 'e' para saber qué falló
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")



    #------------transition graphs-------------------------------

    def g1(self):
        try:
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()

                self.fig=self.xtr.plot_data(x_data='time',y_data='TG', x_units='min', y_units='%')   

                self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=(20, 10))
        except Exception as e:
            
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")

    def g2(self):
        try:
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()

                self.fig=self.xtr.plot_data(x_data='time',y_data='DTG', x_units='min', y_units='%/min')   

                self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=(20, 10))
        except Exception as e:
            
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")

    def g3(self):
        try:
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()

                self.fig=self.xtr.plot_data(x_data='time',y_data='dT/dt', x_units='min', y_units='K/min')   

                self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=(20, 10))
        except Exception as e:
            
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")

    def g4(self):
        try:
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()

                self.fig=self.xtr.plot_data(x_data='temperature',y_data='TG', x_units='K', y_units='%')   

                self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=(20, 10))
        except Exception as e:
            
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")

    def g5(self):
        try:
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()

                self.fig=self.xtr.plot_data(x_data='temperature',y_data='DTG', x_units='K', y_units='%/min')   

                self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=(20, 10))
        except Exception as e:
            
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")

    def g6(self):
        try:
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()

                self.fig=self.xtr.plot_data(x_data='temperature',y_data='dT/dt', x_units='K', y_units='K/min')   

                self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=(20, 10))
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
            
            
            for b in range(len(self.xtr.Beta)):
                print(f'{self.xtr.Beta[b]:.1f}')


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
                        etiqueta_titulo.config(text=f"Ingrese temperatura β={self.xtr.Beta [contador-1]:.1f}")

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
                    etiqueta_titulo.config(text=f"Ingrese temperatura β={self.xtr.Beta [contador-1]:.1f}")

                    entrada.config(state="normal")
                    boton_agregar.config(state="normal")
                    boton_aceptar.pack_forget()

            def aceptar():
                ventana_formulario.destroy()

            # Widgets
            etiqueta_titulo = tk.Label(ventana_formulario, text=f"Ingrese temperatura β={self.xtr.Beta [0]:.1f}")
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
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()

                self.fig=self.xtr.Conversion(self.fix1_conversion,self.fix2_conversion)

                self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=(20, 10))
        except Exception as e:
            
            messagebox.showerror("Unexpected error", f"Details: {str(e)}")


         
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
                                increment=0.005, state="readonly", 
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

        
            print(f"Variables actualizadas: d_a1={self.d_a1}, p1={self.p1}, Metodo={self.methods}")
            ventana_isoconversion.destroy()

        # --- Botón OK ---
        button_algo = tk.Button(ventana_isoconversion, text="Aceptar", command=guardar_y_cerrar)
        button_algo.pack(side=tk.BOTTOM, pady=20)


      

    def ver_isoconversion(self):

        print("-----------------------------------------------------------")
        
        if self.methods == "aVy":
            pass
        elif self.methods == "Vy":
            pass
        elif self.methods == "Fr":
            pass
        elif self.methods =="KAS":
            pass
        elif self.methods =="OFW":
            pass
        else:
            messagebox.showerror("error","choose a method")

        try:
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()
           
            self.isoTables = self.xtr.Isoconversion(d_a=self.d_a1) # crear una variable con este valor por default
           
            ace = pnk.ActivationEnergy(self.xtr.Beta, self.xtr.T0, self.isoTables)   #falta cambiar esta parte
            
            self.aVy = ace.aVy((5, 380), var='time', p=self.p1)  #opcion para escojer metodo  de los cinco
        
        # Get the figure from Ea_plot()
            self.fig = ace.Ea_plot()
        
            # Insert the figure into the frame using FigureCanvasTkAgg
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=(20, 10))
          
            #print(self.isoTables)
        except:
            messagebox.showerror("unexpected error")

        
    def ver_table(self):
        
        try:
            # Limpiar el frame
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()

            # 1. Obtener datos y asegurar que self.isoTables sea un DataFrame
            resultado = self.xtr.Isoconversion(d_a=self.d_a1)
            self.resultado=resultado
            # Si es una tupla, extraemos el array
            datos_array = resultado[0] if isinstance(resultado, tuple) else resultado
            
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


    def export_table(self):
        print(self.isoTables)
        try:
            # Según el error shape=(3, 200, 5), tienes 3 bloques de datos.
            # Basado en tu primer mensaje, intentaremos reconstruir la tabla:
            
            # Extraemos los componentes de la tupla
            y_values = self.isoTables[0]  # La columna de la izquierda (0.002027...)
            x_values = self.isoTables[1]  # Los datos de las columnas ($\beta$)
            
            # Creamos el DataFrame
            # Nota: Si esto falla, intenta con: df = pd.DataFrame(self.isoTables[1], index=self.isoTables[0])
            df = pd.DataFrame(x_values)
            df.index = y_values
            
            # Definir encabezados basados en tu ejemplo
            df.columns = [
                "$\beta=$ 2.50 K/min", 
                "$\beta=$ 5.00 K/min", 
                "$\beta=$ 10.00 K/min", 
                "$\beta=$ 15.00 K/min", 
                "$\beta=$ 20.00 K/min"
            ]

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
    app.mainloop()
