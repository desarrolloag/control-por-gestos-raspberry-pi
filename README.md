# ¡Crea un Guardián Inteligente con tu Raspberry Pi! 👋🤖

¡Hola! Este es un proyecto súper genial desarrollado por **AG Electrónica SAPI de CV** donde le daremos superpoderes a una cámara. Usaremos una **Raspberry Pi** (una mini computadora) y una **cámara con Inteligencia Artificial** para que entienda nuestros gestos.

Imagina que puedes controlar las luces de tu cuarto... ¡con solo levantar la mano! O enviar mensajes secretos a otros aparatos... ¡cruzando los brazos! ¡Vamos a construirlo!

---

## 🗺️ **Lo que encontrarás en este súper folder:**

* [¿De qué trata este invento?](#-de-qué-trata-este-invento)
* [Los Superpoderes de Nuestro Proyecto](#-los-superpoderes-de-nuestro-proyecto)
* [Tu Kit de Inventor (Materiales)](#-tu-kit-de-inventor-materiales)
* [La Receta Secreta (Instalación)](#-la-receta-secreta-instalación)
* [Demostraciones Prácticas (del Kit)](#-demostraciones-prácticas-del-kit)
* [Uso Avanzado: Ejemplos de Picamera2](#-uso-avanzado-ejemplos-de-picamera2)
* [¡A Jugar! (Nuestros Scripts Personalizados)](#-a-jugar-nuestros-scripts-personalizados)
* [¿Necesitas Ayuda?](#-necesitas-ayuda)

---

### **🤔 ¿De qué trata este invento?**

Este proyecto tiene dos versiones o "modos":

1.  **Modo Control de Luces Mágico**: Usamos un programa que mira a través de la cámara y, cuando levantas una mano, ¡prende una luz! Si levantas la otra, ¡prende otra luz! Funciona conectando foquitos (LEDs) o relevadores directamente a la Raspberry Pi.

2.  **Modo Mensajes Secretos**: Usamos otro programa que también entiende tus gestos, pero en vez de prender luces, envía "comandos" o mensajes secretos por un cable a otro aparato. Así, podrías controlar un robot, un carrito o lo que se te ocurra.

[cite_start]Lo más genial es que la cámara tiene su propio cerebro (un chip llamado IMX500) que hace todo el trabajo pesado de pensar, así que la Raspberry Pi queda libre y rápida[cite: 12].

### **✨ Los Superpoderes de Nuestro Proyecto**

* **Ojos de Halcón**: Puede ver y seguir a las personas que aparecen frente a la cámara en tiempo real.
* **Entiende tus Gestos**: Sabe cuando...
    * Levantas la mano derecha.
    * Levantas la mano izquierda.
    * Levantas ambas manos.
    * Cruzas los brazos para decir "¡Alto!".
* **Detector de Presencia**: Se da cuenta si hay alguien en el cuarto y puede prender una luz general.

---

### **🛠️ Tu Kit de Inventor (Materiales)**

[cite_start]Para construir este proyecto, necesitas las piezas que vienen en el "Kit Inicial de IA Raspberry Pi® 5 4GB"[cite: 16].
* [cite_start]Una mini computadora **Raspberry Pi 5**[cite: 18].
* [cite_start]El **Módulo de cámara con IA** (¡los ojos del proyecto!)[cite: 22].
* [cite_start]Una **Tarjeta MicroSD** de 64 GB (la memoria)[cite: 30].
* [cite_start]**Fuente de alimentación** USB-C (para darle energía)[cite: 25].
* [cite_start]Un **Disipador de calor** (un ventilador para que no se caliente)[cite: 33].
* [cite_start]Un **Cable micro HDMI a HDMI** (para conectarla a una pantalla)[cite: 39].
* Unos foquitos **LEDs** y cables para hacer las pruebas de luces.

### **🔧 La Receta Secreta (Instalación)**

Antes de usar los programas, hay que preparar nuestra Raspberry Pi.

1.  [cite_start]**Instala el "Cerebro" del Sistema**: Con la herramienta "Raspberry Pi Imager", instala el sistema operativo **Raspberry Pi OS (64-bit)** en tu tarjeta MicroSD[cite: 53].

2.  [cite_start]**Ponlo al Día**: Abre una ventana de "Terminal" y escribe esto para actualizar todo a la última versión[cite: 57].
    ```bash
    sudo apt update && sudo apt full-upgrade -y
    ```

3.  [cite_start]**Instala los "Drivers" de la Cámara**: Ahora, instala el software especial para que la Raspberry Pi pueda hablar con la cámara con IA[cite: 88].
    ```bash
    sudo apt install imx500-all
    ```

4.  [cite_start]**Reinicia**: Para que todos los cambios funcionen, reinicia tu Raspberry Pi[cite: 90].
    ```bash
    sudo reboot
    ```
---

### **🚀 Demostraciones Prácticas (del Kit)**

Antes de usar nuestros scripts, puedes probar las demostraciones que ya vienen incluidas con el software de la cámara para asegurarte de que todo funciona.

#### **Detección de Objetos**
[cite_start]Con este comando, la cámara intentará identificar objetos comunes como bicicletas, perros, camiones, etc., y los marcará con un recuadro en tiempo real[cite: 96, 100].

* **Ejecuta en la terminal:**
    ```bash
    rpicam-hello -t 0 --post-process-file /usr/share/rpi-camera-assets/imx500_mobilenet_ssd.json --viewfinder-width 1920 --viewfinder-height 1080
    ```

#### **Estimación de Pose**
[cite_start]Este comando utiliza la cámara para detectar personas y dibujar un "esqueleto" sobre ellas, identificando sus articulaciones y postura[cite: 102, 105].

* **Ejecuta en la terminal:**
    ```bash
    rpicam-hello -t 0 --post-process-file /usr/share/rpi-camera-assets/imx500_posenet.json --viewfinder-width 1920 --viewfinder-height 1080
    ```
---

### **🎓 Uso Avanzado: Ejemplos de Picamera2**

Si quieres ir más allá y explorar todos los ejemplos de clasificación, segmentación y más, que vienen con la librería `Picamera2`, necesitas preparar un ambiente de desarrollo especial. [cite_start]Esto es para usuarios más avanzados[cite: 107, 108].

1.  [cite_start]**Instalar Dependencias de Python**: Necesitarás herramientas adicionales para el procesamiento de imágenes[cite: 143].
    ```bash
    sudo apt install python3-opencv python3-munkres
    ```

2.  [cite_start]**Crear un Entorno Virtual**: Esto crea una "caja de arena" para instalar librerías sin afectar el sistema principal, lo cual es muy útil para evitar conflictos[cite: 146, 148].
    ```bash
    python3 -m venv picamera2_env
    source picamera2_env/bin/activate
    ```
    (Verás `(picamera2_env)` al inicio de tu terminal. Para salir de este modo, solo escribe `deactivate`).

3.  [cite_start]**Clonar el Repositorio de Picamera2**: Descarga todo el código fuente y los ejemplos de `picamera2` desde GitHub[cite: 169].
    ```bash
    git clone [https://github.com/raspberrypi/picamera2.git](https://github.com/raspberrypi/picamera2.git)
    cd picamera2
    ```

4.  [cite_start]**Instalar Herramientas Adicionales**: Instala el "Model Compression Toolkit" y las utilidades para el sensor IMX500[cite: 174, 190].
    ```bash
    pip install model_compression_toolkit
    sudo apt install imx500-tools
    ```

5.  [cite_start]**Instalar Picamera2**: Ahora que estás en la carpeta `picamera2` y dentro del entorno virtual, instala la librería[cite: 201].
    ```bash
    pip install .
    ```

¡Listo! [cite_start]Ahora puedes ir a la carpeta `examples` dentro de `picamera2` y ejecutar los scripts de demostración que encontrarás ahí[cite: 212].

---

### **🚀 ¡A Jugar! (Cómo Usarlo)**

Ya que tienes todo instalado, ¡es hora de la acción!

#### **Modo 1: Control de Luces Mágico**

Conecta tus foquitos LED a los pines correctos de la Raspberry Pi. Un pin es como un enchufe chiquito.

* Pin GPIO 17: Para la luz de la mano izquierda.
* Pin GPIO 18: Para la luz de la mano derecha.
* Pin GPIO 22: Para la luz de ambas manos.
* Pin GPIO 23: Para la luz que avisa si hay alguien.
* Pin GPIO 24: Para la luz que se activa al cruzar los brazos.

Para empezar, ve a la carpeta `src` en la terminal y ejecuta este comando:
```bash
python3 "Control de luminarias por detección de pose.py"
```
#### **Modo 2: Envío de Comandos Secretos**
Este script envía palabras clave por el puerto serie. Un aparato que esté escuchando puede recibir estos "mensajes secretos" y hacer algo.

Estos son los comandos que envía:

* newpr: "¡Hola, veo a alguien nuevo!". Se envía cuando se detecta al menos una persona.
* manoi: "¡Mano izquierda arriba!". Se envía cuando una persona levanta la mano izquierda.
* manod: "¡Mano derecha arriba!". Se envía cuando una persona levanta la mano derecha.
* manos: "¡Las dos manos arriba!". Se envía cuando una persona levanta ambas manos.
* cruze: "¡Brazos cruzados, alto!". Se envía cuando una persona cruza los brazos.
* noone: "Ya no veo a nadie, adiós.". Se envía cuando no se detectan personas en el cuadro.

Para empezar, ve a la carpeta src en la terminal y ejecuta:
```bash
python3 "Envío de comandos según pose.py"
```
---

### **Parte 5 de 5: Contacto**

### **🙋 ¿Necesitas Ayuda?**
Si tienes dudas, puedes contactar al ingeniero que desarrolló este ejemplo:

* **Ing. Abraham Solano Carrasco**
* **Email**: asolano@agelectronica.mx
* **WhatsApp**: 55 54689360
* **Sitio Web de AG Electrónica**: [agelectronica.com](https://www.agelectronica.com/tarjetas)

