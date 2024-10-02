import tkinter as tk
from tkinter import colorchooser

# Crear ventana principal
root = tk.Tk()
root.title("Matriz de LEDs 7x7")

# Dimensiones de la matriz
MATRIX_SIZE = 7

# Matriz de botones y colores de los LEDs
led_matrix = [[None for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
led_colors = [[(0, 0, 0) for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]  # Colores RGB, inicialmente apagado

# Color actual (predeterminado)
current_color = (255, 255, 255)  # Blanco por defecto

# Variable global para controlar la animación
is_playing = False

# FUNCIONES #

# Función para seleccionar el color
def choose_color():
    global current_color
    color = colorchooser.askcolor()[0]  # Devolvemos el color en formato RGB
    if color:
        current_color = tuple(map(int, color))  # Actualizar el color seleccionado
        color_display.config(bg=rgb_to_hex(current_color))  # Actualizar el color mostrado

# Función para aplicar el color actual a una casilla (LED)
def apply_color(x, y):
    global led_colors
    led_colors[x][y] = current_color  # Actualizar el color en la matriz de colores
    led_matrix[x][y].config(bg=rgb_to_hex(current_color))  # Actualizar el color del botón

# Función para convertir RGB a hex
def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % (int(rgb[0]), int(rgb[1]), int(rgb[2]))

# Crear la matriz de botones (LEDs)
for i in range(MATRIX_SIZE):
    for j in range(MATRIX_SIZE):
        btn = tk.Button(root, width=4, height=2, bg="black",
                        command=lambda x=i, y=j: apply_color(x, y))  # Aplica el color actual
        btn.grid(row=i, column=j, padx=5, pady=5)
        led_matrix[i][j] = btn

# Botón para seleccionar el color (a la derecha de la matriz)
color_picker_btn = tk.Button(root, text="Elegir Color", command=choose_color)
color_picker_btn.grid(row=0, column=MATRIX_SIZE + 1, padx=20)

# Mostrar el color seleccionado actualmente
color_display = tk.Label(root, text="Color Actual", bg=rgb_to_hex(current_color), width=10, height=2)
color_display.grid(row=1, column=MATRIX_SIZE + 1, padx=20, pady=10)

# Lista de steps para la animación
steps = []

# Función para añadir el step actual a la lista de animaciones
def add_step():
    global steps
    global led_colors
    
    if is_playing:
        return
    
    # Crear un nuevo paso
    step = []
    step.clear()

    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            # Solo guardamos los LEDs que tienen un color distinto de negro
            if led_colors[i][j] != (0, 0, 0):
                step.append({
                    "x": i, "y": j, "z": 0,  # Z por ahora siempre es 0
                    "color": led_colors[i][j]  # Color RGB
                })
                
    steps.append(step)
    print(f"Step añadido: {steps}")
    
# Función para obtener las coordenadas x e y del último step en el array steps
def get_last_led_coordinates():
    global steps
    if steps:
        last_step = steps[-1]
        if last_step:
            last_led = last_step[-1]
            return (last_led["x"], last_led["y"])
    print("No hay steps o LEDs en la lista.")
    return None

#Funcion para eliminar el ultimo step añadido
def clear_last_step():
    global steps
    global led_colors
    global led_matrix
    stop_animation()  # Detener la animación si está en ejecución
    if steps:
        coordinates = get_last_led_coordinates()
        print("Coordenadas del último step:", coordinates)
        removed_step = steps.pop()
        print(f"Último step eliminado: {removed_step}")
        
        led_colors[coordinates[0]][coordinates[1]] = (0, 0, 0)
        led_matrix[coordinates[0]][coordinates[1]].config(bg=rgb_to_hex((0, 0, 0)))  # Actualizar el color del botón
    else:
        print("No hay steps para eliminar.")
        
# Función para vaciar la lista de steps
def clear_steps():
    global steps
    global led_colors
    global is_playing
    global led_matrix
    
    steps.clear()  # Vaciar la lista de steps de manera segura
    print("Lista de steps vaciada:", steps)  # Confirmar que la lista está vacía
    stop_animation()  # Detener la animación si está en ejecución

    # Limpiar la matriz de LEDs
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            led_colors[i][j] = (0,0,0)
            led_matrix[i][j].config(bg="black")

# Función para aplicar un step
def apply_step(step):
    global steps
    global led_matrix
    # Primero, reseteamos todos los LEDs a negro
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            led_matrix[i][j].config(bg="black")

    # Ahora aplicamos el step actual
    for led in step:
        x, y, color = led['x'], led['y'], led['color']
        led_matrix[x][y].config(bg=rgb_to_hex(color))  # Aplicar color al LED

# Función para reproducir la animación
def play_animation(step_index=0):
    global steps
    global is_playing
    if not is_playing or not steps:
        return  # Detener si no hay steps o si no se está reproduciendo
    
    # Aplicar el step actual
    step = steps[step_index]
    apply_step(step)

    # Avanzar al siguiente step, con loop
    next_step_index = (step_index + 1) % len(steps)

    # Obtener velocidad de la animación
    try:
        speed = int(speed_entry.get())
    except ValueError:
        speed = 200  # Valor predeterminado en caso de error

    # Usar after para llamar de nuevo a la función después de la velocidad seleccionada
    root.after(speed, play_animation, next_step_index)

# Función para iniciar la reproducción de la animación
def start_animation():
    global is_playing
    is_playing = True
    # Limpiar la matriz de LEDs
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            led_matrix[i][j].config(bg="black")
    play_animation()

# Función para detener la animación
def stop_animation():
    global is_playing
    is_playing = False
    # imprimimos en la pantalla el ultimo step de la lista
    if steps:
        apply_step(steps[-1])

def show_steps_list():
    print(steps)

# Función para manejar el evento de la tecla espacio
def handle_space(event):
    add_step()
    
def handle_backspace(event):
    clear_last_step()

def handle_esc(event):
    clear_steps()

# Función para iniciar o detener la animación al presionar Enter
def toggle_animation(event):
    global is_playing
    if is_playing:
        stop_animation()
    else:
        start_animation()

# Asociar el evento de la tecla espacio y Enter con las funciones correspondientes
root.bind("<space>", handle_space)
root.bind("<Return>", toggle_animation)  # Enter key to start/stop animation
root.bind("<BackSpace>", handle_backspace)  # Backspace key to clear last step
root.bind("<Escape>", handle_esc)  # Escape key to clear all steps

# Botón para añadir step (abajo de la matriz)
add_step_btn = tk.Button(root, text="Añadir Step", command=add_step)
add_step_btn.grid(row=MATRIX_SIZE + 1, column=0, columnspan=MATRIX_SIZE, pady=10)

# Botón para vaciar la lista de steps
clear_steps_btn = tk.Button(root, text="Vaciar Steps", command=clear_steps)
clear_steps_btn.grid(row=MATRIX_SIZE + 2, column=0, columnspan=MATRIX_SIZE, pady=5)

# Campo para ajustar la velocidad de la animación
tk.Label(root, text="Velocidad (ms)").grid(row=MATRIX_SIZE + 3, column=0, columnspan=MATRIX_SIZE, pady=5)
speed_entry = tk.Entry(root)
speed_entry.insert(0, "200")  # Valor predeterminado de 200 ms
speed_entry.grid(row=MATRIX_SIZE + 4, column=0, columnspan=MATRIX_SIZE, pady=5)

# Botón para reproducir la animación
play_button = tk.Button(root, text="Reproducir Animación", command=start_animation)
play_button.grid(row=MATRIX_SIZE + 5, column=0, columnspan=MATRIX_SIZE, pady=5)

# Botón para detener la animación
stop_button = tk.Button(root, text="Detener Animación", command=stop_animation)
stop_button.grid(row=MATRIX_SIZE + 6, column=0, columnspan=MATRIX_SIZE, pady=5)

# Botón para mostrar la lista de steps
show_button = tk.Button(root, text="Mostrar Steps", command=show_steps_list)
show_button.grid(row=MATRIX_SIZE + 7, column=0, columnspan=MATRIX_SIZE, pady=5)

# Botón para mostrar la lista de steps
show_button = tk.Button(root, text="Borrar ultimo step", command=clear_last_step)
show_button.grid(row=MATRIX_SIZE + 8, column=0, columnspan=MATRIX_SIZE, pady=5)

# Iniciar la interfaz
root.mainloop()