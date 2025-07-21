# ¡Crea un Guardián Inteligente con tu Raspberry Pi! 👋🤖

¡Hola! Este es un proyecto súper genial desarrollado por **AG Electrónica SAPI de CV** donde le daremos superpoderes a una cámara. Usaremos una **Raspberry Pi** (una mini computadora) y una **cámara con Inteligencia Artificial** para que entienda nuestros gestos.

Imagina que puedes controlar las luces de tu cuarto... ¡con solo levantar la mano! O enviar mensajes secretos a otros aparatos... ¡cruzando los brazos! ¡Vamos a construirlo!

---

## 🗺️ **Lo que encontrarás en este súper folder:**

* [¿De qué trata este invento?](#-de-qué-trata-este-invento)
* [Los Superpoderes de Nuestro Proyecto](#-los-superpoderes-de-nuestro-proyecto)
* [Tu Kit de Inventor (Materiales)](#-tu-kit-de-inventor-materiales)
* [La Receta Secreta (Instalación)](#-la-receta-secreta-instalación)
* [¡A Jugar! (Cómo Usarlo)](#-a-jugar-cómo-usarlo)
* [¿Necesitas Ayuda?](#-necesitas-ayuda)

---

### **🤔 ¿De qué trata este invento?**

Este proyecto tiene dos versiones o "modos":

1.  **Modo Control de Luces Mágico**: Usamos un programa que mira a través de la cámara y, cuando levantas una mano, ¡prende una luz! Si levantas la otra, ¡prende otra luz! [cite_start]Funciona conectando foquitos (LEDs) o relevadores directamente a la Raspberry Pi[cite: 10, 241, 252].

2.  [cite_start]**Modo Mensajes Secretos**: Usamos otro programa que también entiende tus gestos, pero en vez de prender luces, envía "comandos" o mensajes secretos por un cable a otro aparato. Así, podrías controlar un robot, un carrito o lo que se te ocurra.

[cite_start]Lo más genial es que la cámara tiene su propio cerebro (un chip llamado IMX500) que hace todo el trabajo pesado de pensar, así que la Raspberry Pi queda libre y rápida[cite: 10, 12].

### **✨ Los Superpoderes de Nuestro Proyecto**

* **Ojos de Halcón**: Puede ver y seguir a las personas que aparecen frente a la cámara en tiempo real.
* **Entiende tus Gestos**: Sabe cuando...
    * Levantas la mano derecha.
    * Levantas la mano izquierda.
    * Levantas ambas manos.
    * Cruzas los brazos para decir "¡Alto!".
* **Detector de Presencia**: Se da cuenta si hay alguien en el cuarto y puede prender una luz general.

### **🛠️ Tu Kit de Inventor (Materiales)**

[cite_start]Para construir este proyecto, necesitas las piezas que vienen en el "Kit Inicial de IA Raspberry Pi® 5 4GB"[cite: 4, 5].
* [cite_start]Una mini computadora **Raspberry Pi 5**[cite: 18].
* [cite_start]El **Módulo de cámara con IA** (¡los ojos del proyecto!)[cite: 22].
* [cite_start]Una **Tarjeta MicroSD** de 64 GB (la memoria)[cite: 30].
* [cite_start]**Fuente de alimentación** USB-C (para darle energía)[cite: 25].
* [cite_start]Un **Disipador de calor** (un ventilador para que no se caliente)[cite: 33].
* [cite_start]Un **Cable micro HDMI a HDMI** (para conectarla a una pantalla)[cite: 39].
* Unos foquitos **LEDs** y cables para hacer las pruebas de luces.

### **🔧 La Receta Secreta (Instalación)**

Antes de usar los programas, hay que preparar nuestra Raspberry Pi. ¡Es como instalar un videojuego!

1.  [cite_start]**Instala el "Cerebro" del Sistema**: Con la herramienta "Raspberry Pi Imager", instala el sistema operativo **Raspberry Pi OS (64-bit)** en tu tarjeta MicroSD[cite: 53].

2.  [cite_start]**Ponlo al Día**: Abre una ventana de "Terminal" y escribe esto para actualizar todo a la última versión[cite: 59].
    ```bash
    sudo apt update && sudo apt full-upgrade -y
    ```

3.  [cite_start]**Instala los "Drivers" de la Cámara**: Ahora, instala el software especial para que la Raspberry Pi pueda hablar con la cámara con IA[cite: 89].
    ```bash
    sudo apt install imx500-all
    ```

4.  **Dale Herramientas Extra a Python**: Python es el lenguaje con el que están escritos nuestros programas. [cite_start]Vamos a darle unas herramientas extra que necesita[cite: 144].
    ```bash
    sudo apt install python3-opencv python3-munkres
    ```

5.  [cite_start]**Reinicia**: Para que todos los cambios funcionen, reinicia tu Raspberry Pi[cite: 91].
    ```bash
    sudo reboot
    ```

6.  **Activa el Puerto de Mensajes Secretos** (sólo si usarás el script de comandos seriales):
    * [cite_start]En la terminal, escribe `sudo raspi-config`[cite: 347].
    * [cite_start]Usa las flechas para ir a `Interface Options` > `Serial Port`[cite: 348].
    * Te preguntará si quieres una consola de login, dile que **No**.
    * [cite_start]Luego te preguntará si quieres habilitar el puerto de hardware, dile que **Sí**[cite: 349].
    * Termina y reinicia la Raspberry Pi. [cite_start]¡El puerto para enviar mensajes ya está abierto! [cite: 350]

---

### **🚀 ¡A Jugar! (Cómo Usarlo)**

Ya que tienes todo instalado, ¡es hora de la acción!

#### **Modo 1: Control de Luces Mágico**

Conecta tus foquitos LED a los pines correctos de la Raspberry Pi. Un pin es como un enchufe chiquito.

* [cite_start]Pin GPIO 17: Para la luz de la mano izquierda[cite: 284].
* [cite_start]Pin GPIO 18: Para la luz de la mano derecha[cite: 285].
* [cite_start]Pin GPIO 22: Para la luz de ambas manos[cite: 286].
* [cite_start]Pin GPIO 23: Para la luz que avisa si hay alguien[cite: 287].
* Pin GPIO 24: Para la luz que se activa al cruzar los brazos.

Para empezar, ve a la carpeta `src` en la terminal y ejecuta este comando:

```bash
python3 "Control de luminarias por detección de pose.py"
