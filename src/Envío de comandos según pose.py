# Desarrollado por AG Electrónica SAPI de CV  
# Este programa utiliza una cámara de inteligencia artificial (AI) y un modelo de red neuronal para detectar y rastrear personas en tiempo real.  
# Además, identifica gestos específicos como manos levantadas, ambas manos levantadas y cruce de brazos. 
# Es un ejemplo de un sistema de control de dispositivos mediante la detección de poses corporales. 
# En esta versión, el sistema envía comandos por puerto serial.
# Contacto: asolano@agelectronica.mx --WhatsApp: 5554689360

#Importaciones y Configuración Inicial
import cv2          #OpenCV, para procesamiento de imágenes.
import argparse     #Para manejar argumentos de línea de comandos.
import sys          #Para interactuar con el sistema, como salir del programa.
import time         #Para manejar tiempos y pausas.
import numpy as np  #Para operaciones numéricas y manejo de arrays.

##############
from gpiozero import LED  #Para controlar LEDs conectados a los pines GPIO de una Raspberry Pi.
##############

import serial 
from picamera2 import CompletedRequest, MappedArray, Picamera2,Preview              #Preview Para manejar la cámara.
from picamera2.devices.imx500 import IMX500, NetworkIntrinsics                      #Modelo de red neuronal para detección de poses.
from picamera2.devices.imx500.postprocess import COCODrawer                         #Para dibujar las detecciones en la imagen.
from picamera2.devices.imx500.postprocess_highernet import postprocess_higherhrnet  #Para procesar la salida de la red neuronal.

# Variables de estado para los eventos seriales
last_serial_event = None  # Último evento enviado por serial
presence_detected = False  # Estado de presencia detectada
last_boxes = None
last_scores = None
last_keypoints = None
#WINDOW_SIZE_H_W = (480, 640)
WINDOW_SIZE_H_W = (1440, 1920)

#Configuración del puerto serial
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
#time.sleep(2)  # Espera 2 segundos para asegurarte de que el puerto esté listo

#GPIO setup

led_derecho = LED(18)       # LED derecho en GPIO18
led_izquierdo = LED(17)     # LED izquierdo en GPIO17
led_ambas_manos = LED(22)   # LED adicional en GPIO22 para ambas manos levantadas
led_presencia = LED(23)     # GPIO para detectar presencia
led_cruce_brazos = LED(24)  # GPIO para detectar cruce de brazos 

led_derecho.off()            # Asegurar que el LED derecho esté apagado al inicio
led_izquierdo.off()          # Asegurar que el LED izquierdo esté apagado al inicio
led_ambas_manos.off()        # Asegurar que el LED para ambas manos levantadas esté apagado al inicio
led_presencia.off()          # Asegurar que el GPIO de presencia esté apagado al inicio
led_cruce_brazos.off()       # Asegurar que el GPIO de cruce de brazos esté apagado al inicio

# Stability parameters
hand_raised_count_right = 0
hand_raised_count_left = 0
both_hands_raised_count = 0
arms_crossed_count = 0
hand_raised_threshold = 3  # Número de cuadros consecutivos para confirmar manos levantadas
both_hands_raised_threshold = 3  # Número de cuadros consecutivos para confirmar ambas manos levantadas

tracked_people = {}  # Diccionario para almacenar personas detectadas
next_id = 1  # ID único para cada persona
# Variable global para el último evento enviado
last_serial_event = None

#Función para realizar el seguimiento de personas detectadas utilizando un ID único##################
def track_people(boxes, scores, person_count, threshold=0.25):
    """
    Realiza el seguimiento de las personas detectadas utilizando un ID único.
    """
    global tracked_people, next_id

    updated_people = {}
    for i, box in enumerate(boxes):
        if scores[i] >= threshold:
            # Convertir las coordenadas de la caja en un punto central
            x_center = (box[0] + box[2]) / 2
            y_center = (box[1] + box[3]) / 2
            detected = False

            # Comparar con personas ya rastreadas
            for person_id, (px, py) in tracked_people.items():
                if abs(px - x_center) < 50 and abs(py - y_center) < 50:  # Tolerancia
                    updated_people[person_id] = (x_center, y_center)
                    detected = True
                    break

            # Si no se detecta como una persona existente, asignar un nuevo ID
            if not detected:
                updated_people[next_id] = (x_center, y_center)
                next_id += 1

    # Actualizar las personas rastreadas
    tracked_people = updated_people

    return len(tracked_people)

# Función para enviar un mensaje byte a byte
def send_message_byte_by_byte(evento):
    ser.reset_input_buffer()  # Limpiar el buffer de entrada
    ser.reset_output_buffer()  # Limpiar el buffer de salida
    #time.sleep(0.5)  # Pausa para asegurar la limpieza completa

    message_to_send = evento.encode()  # Convertir el mensaje a bytes
    for byte in message_to_send:
        ser.write(byte.to_bytes(1, 'little'))  # Enviar byte a byte
        ser.flush()  # Asegurarse de que se envíe el byte
        #time.sleep(0.1)  # Pausa entre bytes para asegurar la transmisión correcta

    ser.write(b'\n')  # Enviar un salto de línea al final del mensaje
    ser.flush()  # Asegurarse de que el salto de línea se envíe completamente

    #time.sleep(1)  # Pausa entre mensajes para asegurar la recepción completa
    ser.reset_input_buffer()  # Limpiar el buffer de entrada nuevamente
    ser.reset_output_buffer()  # Limpiar el buffer de salida nuevamente

# Función para enviar un evento por serial solo si es diferente al último enviado.
def enviar_evento_serial(evento):
    """
    Envía un evento por el puerto serial solo si es nuevo.
    """
    global last_serial_event
    try:
        if last_serial_event != evento:  # Solo envía si el evento es diferente al último enviado
            if len(evento) == 5:
                send_message_byte_by_byte(evento)
                print(f"Evento enviado por serial: {evento}")
                last_serial_event = evento
    except serial.SerialException as e:
        print(f"Error enviando datos por UART: {e}")
    except Exception as e:
        print(f"Error inesperado enviando datos por UART: {e}")

#Función que procesa la salida de la red neuronal para detectar gestos y presencia##################
def ai_output_tensor_parse(metadata: dict):
    global last_boxes, last_scores, last_keypoints, hand_raised_count_right, hand_raised_count_left, both_hands_raised_count, arms_crossed_count, presence_detected, last_serial_event
    np_outputs = imx500.get_outputs(metadata=metadata, add_batch=True)
    hands_raised_right = False
    hands_raised_left = False
    both_hands_raised = False
    arms_crossed = False
    person_count = 0

    if np_outputs is not None:
        keypoints, scores, boxes = postprocess_higherhrnet(
            outputs=np_outputs,
            img_size=WINDOW_SIZE_H_W,
            img_w_pad=(0, 0),
            img_h_pad=(0, 0),
            detection_threshold=args.detection_threshold,
            network_postprocess=True,
        )

        if scores is not None and len(scores) > 0:
            last_keypoints = np.reshape(np.stack(keypoints, axis=0), (len(scores), 17, 3))
            last_boxes = [np.array(b) for b in boxes]
            last_scores = np.array(scores)

            # Contar personas
            person_count = track_people(last_boxes, last_scores, len(scores))

            # Detectar presencia y enviar evento si cambia
            if person_count > 0 and not presence_detected:
                led_presencia.on()
                enviar_evento_serial("newpr")
                presence_detected = True
            elif person_count == 0 and presence_detected:
                led_presencia.off()
                presence_detected = False
                last_serial_event = None  # Reiniciar último evento
            if person_count == 0:
                enviar_evento_serial("noone") # Enviar "noone" cuando no haya nadie en el cuadro

            for i in range(len(last_keypoints)):
                keypoints = last_keypoints[i]
                wrist_right = keypoints[10]     # Muñeca derecha
                shoulder_right = keypoints[6]   # Hombro derecho
                wrist_left = keypoints[9]       # Muñeca izquierda
                shoulder_left = keypoints[5]    # Hombro izquierdo
                elbow_right = keypoints[7]      # Codo derecho 
                elbow_left = keypoints[8]       # Codo izquierdo

                # Detectar manos levantadas
                if wrist_right[2] > 0.3 and shoulder_right[2] > 0.3 and wrist_right[1] < shoulder_right[1] - 50:
                    hands_raised_right = True
                if wrist_left[2] > 0.3 and shoulder_left[2] > 0.3 and wrist_left[1] < shoulder_left[1] - 50:
                    hands_raised_left = True

                # Detectar ambas manos levantadas
                if hands_raised_right and hands_raised_left:
                    both_hands_raised = True

                # Detectar cruce de brazos
                if wrist_right[2] > 0.30 and wrist_left[2] > 0.30 and elbow_right[2] > 0.30 and elbow_left[2] > 0.30:
                    if abs(wrist_right[0] - wrist_left[0]) < 50 and \
                       ((wrist_right[1] < elbow_left[1] and wrist_left[1] < elbow_right[1]) or
                        (wrist_left[1] < elbow_right[1] and wrist_right[1] < elbow_left[1])):
                        arms_crossed = True
    
    # Control de LEDs y envío de eventos
    if hands_raised_right == True and hands_raised_left == False:
        hand_raised_count_right += 1
        led_derecho.on()         
        enviar_evento_serial("manod")
    else:
        hand_raised_count_right = 0
        # Solo apaga el LED si no hay personas en el cuadro
        if person_count == 0 or arms_crossed == 1:
            led_derecho.off() 
            
    if hands_raised_left == True and hands_raised_right == False:
        hand_raised_count_left += 1
        enviar_evento_serial("manoi")
        led_izquierdo.on() 
    else:
        hand_raised_count_left = 0
        # Solo apaga el LED si no hay personas en el cuadro
        if person_count == 0 or arms_crossed == 1:
            led_izquierdo.off() 

    if both_hands_raised:
        both_hands_raised_count += 1
        if both_hands_raised_count >= both_hands_raised_threshold:  # Confirmar ambas manos levantadas
            led_ambas_manos.on()     
            if last_serial_event != "manos":  # Evitar envío repetido
               enviar_evento_serial("manos")
               last_serial_event = "manos"
    else:
        both_hands_raised_count = 0
        # Solo apaga el LED si no hay personas en el cuadro
        if person_count == 0 or arms_crossed == 1:
            led_ambas_manos.off()

    if arms_crossed:
        arms_crossed_count += 1
        if arms_crossed_count >= 3:  # Confirmar cruce
            led_cruce_brazos.on()
            enviar_evento_serial("cruze")
    else:
        arms_crossed_count = 0
        led_cruce_brazos.off() 

    return last_boxes, last_scores, last_keypoints, person_count, arms_crossed

# Función que dibuja las detecciones y mensajes en la imagen de la cámara ############################
def ai_output_tensor_draw(request: CompletedRequest, boxes, scores, keypoints, person_count, arms_crossed, stream='main'):
    """Dibujar detecciones y mensajes en la cámara."""
    global last_message
    with MappedArray(request, stream) as m:
        if boxes is not None and len(boxes) > 0:
            drawer.annotate_image(
                m.array, boxes, scores,
                np.zeros(scores.shape), keypoints,
                args.detection_threshold, args.detection_threshold,
                request.get_metadata(), picam2, stream
            )

        # Dibujar mensajes según las condiciones
        if person_count > 0:
            if both_hands_raised_count >= both_hands_raised_threshold:
                message = "Ambas Manos Levantadas"
            elif hand_raised_count_right >= hand_raised_threshold:
                message = "Mano Derecha Levantada"
            elif hand_raised_count_left >= hand_raised_threshold:
                message = "Mano Izquierda Levantada"
            elif arms_crossed:
                message = "Brazos Cruzados Detectados"  # Mensaje para el cruce de brazos
            elif hand_raised_count_right == 0 and hand_raised_count_left == 0:
                message = "Esperando Accion"
            else:
                message = ""
            #drawer.text((50, 50), message, (255, 255, 255), 20)
            
     # Dibujar mensaje
            for i, line in enumerate(message.split("\n")):
                cv2.putText(
                    m.array,
                    line,
                    (10, 30 + i * 30),  # Línea siguiente
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                )     
                      
            # Mostrar número de personas
            # Draw person count in the bottom-right corner
        text = f"Personas: {person_count}"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = m.array.shape[1] - text_size[0] - 10  # 10 px padding from the right
        text_y = m.array.shape[0] - 10  # 10 px padding from the bottom
        cv2.putText(
            m.array,
            text,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            )
#Función de callback para analizar y dibujar detecciones en cada frame #############################
def picamera2_pre_callback(request: CompletedRequest):
    """Analyze and draw detections on the camera output."""
    boxes, scores, keypoints, person_count, arms_crossed = ai_output_tensor_parse(request.get_metadata())
    ai_output_tensor_draw(request, boxes, scores, keypoints, person_count, arms_crossed)
#Función que obtiene los argumentos de línea de comandos############################################    
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, help="Path of the model",default="/usr/share/imx500-models/imx500_network_higherhrnet_coco.rpk")
    parser.add_argument("--fps", type=int, help="Frames per second")
    parser.add_argument("--detection-threshold", type=float, default=0.3,help="Post-process detection threshold")
    parser.add_argument("--labels", type=str, help="Path to the labels file")
    parser.add_argument("--print-intrinsics", action="store_true",help="Print JSON network_intrinsics then exit")
    return parser.parse_args()
#Configura el dibujador para las detecciones########################################################  
def get_drawer():
    categories = intrinsics.labels
    categories = [c for c in categories if c and c != "-"]
    return COCODrawer(categories, imx500, needs_rescale_coords=False)            
####################################################################################################
if __name__ == "__main__":
    args = get_args()
    imx500 = IMX500(args.model)
    intrinsics = imx500.network_intrinsics
    
    if not intrinsics:
        intrinsics = NetworkIntrinsics()
        intrinsics.task = "pose estimation"
    elif intrinsics.task != "pose estimation":
        print("Network is not a pose estimation task", file=sys.stderr)
        exit()

    for key, value in vars(args).items():
        if key == 'labels' and value is not None:
            with open(value, 'r') as f:
                intrinsics.labels = f.read().splitlines()
        elif hasattr(intrinsics, key) and value is not None:
            setattr(intrinsics, key, value)

    if args.print_intrinsics:
        print(intrinsics)
        exit()

    drawer = get_drawer()
    #################################################################################################
    #Configura y inicia la cámara.
    picam2 = Picamera2(imx500.camera_num)
    #config = picam2.create_preview_configuration(main={"size": (640, 480)},
    config = picam2.create_preview_configuration(main={"size": (1920, 1440)},
        controls={'FrameRate': intrinsics.inference_rate}, buffer_count=12
    )
    picam2.configure(config)
    #picam2.start_preview(Preview.QTGL, x=0, y=0, width=1920, height=1080)
    picam2.start_preview(Preview.QTGL, x=0, y=0, width=1920, height=1440)
    ##################################################################################################
    #Inicia la cámara y asigna la función de callback.
    imx500.show_network_fw_progress_bar()
    picam2.start(config, show_preview=True)
    imx500.set_auto_aspect_ratio()
    picam2.pre_callback = picamera2_pre_callback
    ##################################################################################################
    #Bucle principal que mantiene el programa en ejecución hasta que se interrumpe con Ctrl+C.
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
#QtGIPreview
