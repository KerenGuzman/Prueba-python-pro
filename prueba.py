import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class Tarea:
    def __init__(self, contenido, descripcion="", completada=False):
        self.contenido = contenido
        self.descripcion = descripcion
        self.completada = completada

    def to_dict(self):
        return {
            "contenido": self.contenido,
            "descripcion": self.descripcion,
            "completada": self.completada
        }

class GestorTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas con Descripción")
        self.tareas = self.cargar_tareas()
        self.tarea_seleccionada = None

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.tarea_entry = tk.Entry(self.frame, width=40)
        self.tarea_entry.pack(side=tk.LEFT, padx=10)

        self.descripcion_entry = tk.Entry(self.frame, width=40)
        self.descripcion_entry.pack(side=tk.LEFT, padx=10)

        self.agregar_btn = tk.Button(self.frame, text="Agregar tarea", command=self.agregar_tarea)
        self.agregar_btn.pack(side=tk.LEFT)

        self.lista_tareas = tk.Listbox(self.root, width=80, height=10)
        self.lista_tareas.pack(pady=10)
        self.lista_tareas.bind('<<ListboxSelect>>', self.seleccionar_tarea)

        self.completar_btn = tk.Button(self.root, text="Completar/Desmarcar tarea", command=self.completar_tarea)
        self.completar_btn.pack(pady=5)

        self.editar_btn = tk.Button(self.root, text="Actualizar tarea", command=self.actualizar_tarea)
        self.editar_btn.pack(pady=5)

        self.eliminar_btn = tk.Button(self.root, text="Eliminar tarea", command=self.eliminar_tarea)
        self.eliminar_btn.pack(pady=5)

        self.mostrar_btn = tk.Button(self.root, text="Mostrar Descripción", command=self.mostrar_descripcion)
        self.mostrar_btn.pack(pady=5)

        self.actualizar_lista()

    def cargar_tareas(self):
        if os.path.exists('tareas.json'):
            with open('tareas.json', 'r') as archivo:
                tareas_dict = json.load(archivo)
                return [Tarea(**tarea) for tarea in tareas_dict]
        return []

    def guardar_tareas(self):
        with open('tareas.json', 'w') as archivo:
            json.dump([tarea.to_dict() for tarea in self.tareas], archivo, indent=4)

    def agregar_tarea(self):
        contenido = self.tarea_entry.get()
        descripcion = self.descripcion_entry.get()
        if contenido:
            self.tareas.append(Tarea(contenido, descripcion))
            self.guardar_tareas()
            self.tarea_entry.delete(0, tk.END)
            self.descripcion_entry.delete(0, tk.END)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una tarea.")

    def seleccionar_tarea(self, event):
        try:
            index = self.lista_tareas.curselection()[0]
            self.tarea_seleccionada = index
            self.tarea_entry.delete(0, tk.END)
            self.tarea_entry.insert(0, self.tareas[index].contenido)
            self.descripcion_entry.delete(0, tk.END)
            self.descripcion_entry.insert(0, self.tareas[index].descripcion)
        except IndexError:
            self.tarea_seleccionada = None

    def completar_tarea(self):
        if self.tarea_seleccionada is not None:
            tarea = self.tareas[self.tarea_seleccionada]
            tarea.completada = not tarea.completada
            self.guardar_tareas()
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una tarea para completar.")

    def actualizar_tarea(self):
        if self.tarea_seleccionada is not None:
            nueva_tarea = self.tarea_entry.get()
            nueva_descripcion = self.descripcion_entry.get()
            if nueva_tarea:
                self.tareas[self.tarea_seleccionada].contenido = nueva_tarea
                self.tareas[self.tarea_seleccionada].descripcion = nueva_descripcion
                self.guardar_tareas()
                self.actualizar_lista()
            else:
                messagebox.showwarning("Advertencia", "Por favor, ingrese una tarea.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una tarea para actualizar.")

    def eliminar_tarea(self):
        if self.tarea_seleccionada is not None:
            self.tareas.pop(self.tarea_seleccionada)
            self.guardar_tareas()
            self.tarea_entry.delete(0, tk.END)
            self.descripcion_entry.delete(0, tk.END)
            self.tarea_seleccionada = None
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una tarea para eliminar.")

    def mostrar_descripcion(self):
        if self.tarea_seleccionada is not None:
            tarea = self.tareas[self.tarea_seleccionada]
            messagebox.showinfo("Descripción de la Tarea", tarea.descripcion)
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una tarea para ver la descripción.")

    def actualizar_lista(self):
        self.lista_tareas.delete(0, tk.END)
        for tarea in self.tareas:
            tarea_texto = f"{tarea.contenido} {'(Completada)' if tarea.completada else ''}"
            self.lista_tareas.insert(tk.END, tarea_texto)

if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()
