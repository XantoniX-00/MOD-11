
# app.py
# Aplicación CLI para gestión de artículos de presupuesto

import json
import os

DATA_FILE = "articulos.json"

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(articulos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(articulos, f, indent=4, ensure_ascii=False)

def generar_id(articulos):
    return max([a["id"] for a in articulos], default=0) + 1

def registrar_articulo():
    print("\n--- Registrar nuevo artículo ---")
    nombre = input("Nombre: ").strip()
    categoria = input("Categoría: ").strip()
    descripcion = input("Descripción: ").strip()

    try:
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio unitario: "))
    except ValueError:
        print("❌ Cantidad y precio deben ser numéricos.")
        return

    articulos = cargar_datos()
    articulo = {
        "id": generar_id(articulos),
        "nombre": nombre,
        "categoria": categoria,
        "descripcion": descripcion,
        "cantidad": cantidad,
        "precio": precio
    }

    articulos.append(articulo)
    guardar_datos(articulos)
    print("✅ Artículo registrado correctamente.")

def listar_articulos():
    print("\n--- Lista de artículos ---")
    articulos = cargar_datos()
    if not articulos:
        print("No hay artículos registrados.")
        return

    print(f"{'ID':<5}{'Nombre':<20}{'Categoría':<15}{'Cant':<6}{'Precio':<10}")
    print("-" * 60)
    for a in articulos:
        print(f"{a['id']:<5}{a['nombre']:<20}{a['categoria']:<15}{a['cantidad']:<6}{a['precio']:<10.2f}")

def buscar_articulos():
    print("\n--- Buscar artículos ---")
    criterio = input("Buscar por nombre o categoría: ").lower()
    articulos = cargar_datos()
    resultados = [
        a for a in articulos
        if criterio in a["nombre"].lower() or criterio in a["categoria"].lower()
    ]

    if not resultados:
        print("No se encontraron coincidencias.")
        return

    for a in resultados:
        print(a)

def editar_articulo():
    print("\n--- Editar artículo ---")
    try:
        id_articulo = int(input("ID del artículo: "))
    except ValueError:
        print("ID inválido.")
        return

    articulos = cargar_datos()
    for a in articulos:
        if a["id"] == id_articulo:
            print("Deja vacío para mantener el valor actual.")
            nombre = input(f"Nombre ({a['nombre']}): ").strip()
            categoria = input(f"Categoría ({a['categoria']}): ").strip()
            descripcion = input(f"Descripción ({a['descripcion']}): ").strip()

            if nombre:
                a["nombre"] = nombre
            if categoria:
                a["categoria"] = categoria
            if descripcion:
                a["descripcion"] = descripcion

            try:
                cantidad = input(f"Cantidad ({a['cantidad']}): ").strip()
                precio = input(f"Precio ({a['precio']}): ").strip()
                if cantidad:
                    a["cantidad"] = int(cantidad)
                if precio:
                    a["precio"] = float(precio)
            except ValueError:
                print("Valores numéricos inválidos.")
                return

            guardar_datos(articulos)
            print("✅ Artículo actualizado.")
            return

    print("❌ Artículo no encontrado.")

def eliminar_articulo():
    print("\n--- Eliminar artículo ---")
    try:
        id_articulo = int(input("ID del artículo: "))
    except ValueError:
        print("ID inválido.")
        return

    articulos = cargar_datos()
    nuevos = [a for a in articulos if a["id"] != id_articulo]

    if len(nuevos) == len(articulos):
        print("❌ Artículo no encontrado.")
        return

    guardar_datos(nuevos)
    print("🗑️ Artículo eliminado.")

def menu():
    while True:
        print("""
==============================
Gestión de Presupuesto - CLI
==============================
1. Registrar artículo
2. Listar artículos
3. Buscar artículos
4. Editar artículo
5. Eliminar artículo
6. Salir
""")

        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            registrar_articulo()
        elif opcion == "2":
            listar_articulos()
        elif opcion == "3":
            buscar_articulos()
        elif opcion == "4":
            editar_articulo()
        elif opcion == "5":
            eliminar_articulo()
        elif opcion == "6":
            print("👋 Hasta luego.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
