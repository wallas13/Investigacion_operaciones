# Optimización de procesos
En este repositorio se encuentra un software que tiene como objetivo
solucionar modelos matemáticos propuestos por los usuarios, está enfocado 
principalmente para que pequeñas y medianas empresas puedan hacer uso del software
con el fin de optimizar sus operaciones.
Este proyecto fue desarrollado en el lenguaje Python utilizando librerías como:
- Flask
- Matplotlib
- Numpy
- Json
- Date
## Instalación del proyecto
Para utilizar este software se recomienda seguir estos pasos:
- ### Realizar la instalación de Python en su máquina:
    Para su funcionamiento es indispensable que se haga la instalación de Python en la máquina.
    Podrá descargar Python dando click [aquí](https://www.python.org/downloads/) y siguiendo la instalación guiada.
- ### Creación de un entorno virtual    
    Cuando se manejan librerías es preferible el uso de entornos virtuales los cuales nos permitan hacer la instalación de estas librerías en dicho entorno sin necesidad de que se instalen de manera global, si usted lo desea puede saltar este paso y hacer la instalación de las librerías de manera global de lo contrario debe seguir estos pasos:
    - #### Instalar la librería que permite la creación de entornos virtuales
        Antes de nada se debe hacer la instalación de la librería que nos permite crear entornos virtuales, esta es **virtualenv**.
        Para su instalación únicamente se debe ejecutar el siguiente comando **pip install virtualenv** desde una terminal como cmd
    - #### Creación del entorno virtual
        Una vez instalada la librería se puede proceder a la creación del entorno virtual, para esto desde una terminal de comandos se debe ubicar en la raíz del proyecto y ejecutar el siguiente comando **virtualenv nombre_del_entorno_virtual**
    - #### Activación del entorno virtual
        Una vez completado el paso anterior se debió crear una una carpeta en la raíz del proyecto con el nombre que se le ha asignado en el comando de creación del entorno, dentro de esta carpeta se encontrará una nueva con el nombre **Scripts** dentro de esta carpeta se encuentran archivos como **activate.bat** o **activate.ps1**.
        Para activar el entorno virtual desde una terminal de comandos debe abrir la ubicación de cualquiera de estos dos archivos mencionados anteriormente como por ejemplo: 
        - **C:\>c:\ruta\al\entorno\virtual\scripts\activate.bat** en windows
        - **C:\>c:\ruta\al\entorno\virtual\scripts\activate.ps1** en windows con powershell
        - **$ source ruta/al/entorno/virtual/bin/activate** en macOS o linux
- ### Instalación de las librerías utilizadas
    Una vez instalado y activado el entorno virtual se puede proceder a hacer la instalación de las librerías requeridas por el proyecto, recordemos que si no se ha creado el entorno virtual estas librerías serán instaladas de manera global en Python. Para hacer la instalación de estas librerías debe ejecutar el siguiente comando **pip install -r requirements.txt** en la terminal donde se encuentre activado su entorno virtual y si no tiene entorno virtual debe ubicarse en la raíz del proyecto.
- ### Ejecución del software
    Una vez instaladas las librerías podrá ejecutar el `index.py` con el siguiente comando **`py index.py`** desde la terminal de comandos donde se encuentra activado el entorno virtual. Una vez hecho esto se estará ejecutando el software de manera predeterminada en el **localhost:5000**.
- ### Uso del software
    Desde cualquier navegador web como Google Chrome o Firefox en la barra superior donde normalmente se encuentran las url de los sitios web escribir **localhost:5000**, si ha modificado el código fuente entonces escriba el puerto que le ha asignado.
    Si ha seguido los pasos de manera correcta entonces ingresará al software y podrá empezar a utilizarlo con los modelos matemáticos que desee.