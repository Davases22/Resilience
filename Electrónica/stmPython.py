import serial
import tkinter as tk

# Configuración del puerto serie
port = 'COM10'  # Reemplaza 'COMx' con el puerto serie donde está conectada tu STM32F4
baudrate = 9600  # Velocidad de baudios
terminar = '0'

# Abre el puerto serie
ser = serial.Serial(port, baudrate)


def update_values():

    angles = [slider.get() for slider in sliders]
    vel = [(entry.get()) for entry in entries]
    print("Ángulos:", angles)
    print("Velocidades:", vel)


    try:
    # Envía datos a la STM32F4
        ser.write(str(angles[0]).encode())
        ser.write((',').encode())
        ser.write((vel[0]).encode())
        ser.write((',').encode())
        ser.write(str(angles[1]).encode())
        ser.write((',').encode())
        ser.write((vel[1]).encode())
        ser.write((',').encode())
        ser.write(str(angles[2]).encode())
        ser.write((',').encode())
        ser.write((vel[2]).encode())
        ser.write((',').encode())
        ser.write(str(angles[3]).encode())
        ser.write((',').encode())
        ser.write((vel[3]).encode())
        ser.write((',').encode())
        ser.write(str(angles[4]).encode())
        ser.write((',').encode())
        ser.write((vel[4]).encode())
        ser.write((',').encode())
        ser.write(str(angles[5]).encode())
        ser.write((',').encode())
        ser.write((vel[5]).encode())
        ser.write((',').encode())
        ser.write(str(angles[6]).encode())
        ser.write((',').encode())
        ser.write((vel[6]).encode())
        ser.write(('N').encode())
        
        

    except serial.SerialException as e:
        print("Error al comunicarse con la STM32F4:", e)


def update_pololu_values():

    RPM = [pololu_sliders[i].get() for i in range(3)]
    print("Ángulos de Pololu:", RPM)

    
    try:
        # Envía datos a la STM32F4
        '''
        for i in range(len(RPM)):
            ser.write(str(RPM[i]).encode())
            ser.write((',').encode())
        ser.write(('P').encode())
        '''
        ser.write(str(RPM[0]).encode())
        ser.write((',').encode())
        ser.write(str(RPM[1]).encode())
        ser.write((',').encode())
        ser.write(str(RPM[2]).encode())
        ser.write(('P').encode())


    except serial.SerialException as e:
        print("Error al comunicarse con la STM32F4:", e)


def Recibir_Com():
    ser.write(b'E')
    #data1 = ser.readline().decode().strip()
    #print(data1)
    #data = "12.0,35.4,14.9"
    data = ser.readline().decode().strip()
    print(data)
        
    # Si hay datos válidos
    if data:
        # Dividir los datos en números individuales
        velPololu = data.split(',')
        
        # Convertir los números a flotantes
        velPololu = [float(num) for num in velPololu]
        
        # Actualizar los cuadros de entrada en el segundo frame con los valores recibidos
        for i in range(len(velPololu)):
            pololu_entries[i].delete(0, tk.END)  # Borrar el contenido actual del cuadro de entrada
            pololu_entries[i].insert(0, str(velPololu[i]))  # Insertar el nuevo valor en el cuadro de entrada


        # Imprimir los números
        print("Números leídos:", velPololu)



root = tk.Tk()
root.title("Control de brazo")

sliders = []
entries = []

initial_angles = [90, 90, 90, 90, 90, 90, 90]
initial_vel = [20, 20, 20, 20, 20, 20, 20]

pololu_sliders = []
pololu_entries = []

initial_RPM = [20, 20, 20]
initial_vel_P = [0, 0, 0]


for i in range(7):

    slider_frame = tk.Frame(root)
    slider_frame.pack(pady=5)
    label = tk.Label(slider_frame, text=f"Junta {i}:")
    label.pack(side=tk.LEFT)
    slider = tk.Scale(slider_frame, from_=-180, to=180, orient=tk.HORIZONTAL, length=200)
    slider.set(initial_angles[i])  # Establecer el valor inicial del slider
    slider.pack(side=tk.LEFT)
    sliders.append(slider)

    entry = tk.Entry(slider_frame, width=5)
    entry.pack(side=tk.RIGHT)
    entry.insert(0, str(initial_vel[i]))  # Establece el valor inicial del cuadro de entrada
    entries.append(entry)


# SEGUNDO FRAME
for i in range(3):

    slider_frame = tk.Frame(root)
    slider_frame.pack(pady=5)
    label_text = f"Pololu {i + 1}:"
    label = tk.Label(slider_frame, text=label_text)
    label.pack(side=tk.LEFT)
    slider = tk.Scale(slider_frame, from_=-120, to=120, orient=tk.HORIZONTAL, length=200)
    slider.set(initial_RPM[i])  # Establecer el valor inicial del slider
    slider.pack(side=tk.LEFT)
    pololu_sliders.append(slider)

    entry = tk.Entry(slider_frame, width=5)
    entry.pack(side=tk.LEFT)
    entry.insert(0, str(initial_vel_P[i]))  # Establece el valor inicial del cuadro de entrada
    pololu_entries.append(entry)





    

update_button = tk.Button(root, text="Angulos Nema", command=update_values)
update_button.pack(pady=10)

update_button_Pololu = tk.Button(root, text="Pololu RPM", command=update_pololu_values)
update_button_Pololu.pack(pady=10)

update_button_Pololu = tk.Button(root, text="Lectura Encoders", command=Recibir_Com)
update_button_Pololu.pack(pady=10)

root.mainloop()

# Cierra el puerto serie
ser.close()





