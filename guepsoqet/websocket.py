# -*- coding: utf-8 -*-
# pip install websockets mysql-connector-python
# Ejecutar con Python 3.7 o superior

import asyncio
import websockets
import mysql.connector
import serial

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sm52_arduino'
}

# Configura el puerto serial según tu configuración de Arduino
arduino_serial = serial.Serial('COM4', 9600, timeout=1)

def update_led_status_in_db(status, color_status, sensor_data=None):
    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Actualizar el estado del LED
    cursor.execute("UPDATE estado_led SET led_status = %s WHERE id_estado_led = 1", (status,))

    # Si se proporcionaron datos del sensor, actualizar el estado del color
    if sensor_data is not None:
        cursor.execute("UPDATE estado_led SET estado_color = %s WHERE id_estado_led = 1", (sensor_data,))

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    cursor.close()
    conn.close()

def get_led_status_from_db():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT led_status, estado_color FROM estado_led WHERE id_estado_led = 1")
        row = cursor.fetchone()
        if row is not None:  
            status = row[0]
            color_status = row[1]
            return status, color_status
        else:
            print("No se encontró ningún resultado en la base de datos.")
            return None, None
    except mysql.connector.Error as e:
        print(f"Error de base de datos: {e}")
        return None, None
    finally:
        cursor.close()
        conn.close()

def read_from_arduino():
    if arduino_serial.in_waiting > 0:
        data = arduino_serial.readline().decode().strip()
        return data
    return None

async def handle_led(websocket, path):
    status, color_status = get_led_status_from_db()
    await websocket.send(str(status)) 

    while True:
       
        sensor_data = read_from_arduino()
        if sensor_data is not None:
            print(f"Datos del sensor: {sensor_data}")
            update_led_status_in_db(status, color_status, sensor_data)

          
            distance = float(sensor_data)

          
            if distance > 1 and distance <= 10:
                await websocket.send('2') 
            elif distance > 11 and distance <=30:
                await websocket.send('3')  
            else:
                await websocket.send('4') 

        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
            if message in ["1", "0"]:
                status = message  # Actualizar el estado local del LED
                update_led_status_in_db(status, color_status)
                arduino_serial.write(message.encode())
                await websocket.send(message)  # Opcional: Confirmar el cambio al cliente
            elif message in ["2", "3", "4"]:
                color_status = message  # Actualizar el estado local del color
                update_led_status_in_db(status, color_status)
                arduino_serial.write(message.encode())
                await websocket.send(message)  # Opcional: Confirmar el cambio al cliente
        except asyncio.TimeoutError:
            # No se recibió ningún mensaje en el tiempo de espera, continuar con la siguiente iteración
            continue
async def start_server():
    async with websockets.serve(handle_led, "localhost", 8765):
        await asyncio.Future()  # Ejecuta el servidor indefinidamente

if __name__ == "__main__":
    asyncio.run(start_server())