# Tobichat

Tobichat es un chat bot que usa el modelo "facebook/blenderbot-400M-distill" de Hugging Face para entablar una conversación casual en inglés con el usuario.

En este link podrás acceder al chat: [Tobichat](http://MiguelAmato.github.io/Tobichat)

Modelo usado: [facebook/blenderbot-400M-distill](https://huggingface.co/facebook/blenderbot-400M-distill)

## Instalación

Requisitos previos para la instalación manual:

- Tener instalado Node.js

```bash
# instala nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

# Descargar e instalar Node.js (Puede ser que necesites reiniciar la terminal)
nvm install 20
```
- Instalar el manejador de paquetes de node

```bash
sudo apt install npm
```

Una vez instalados los requisitos previos procedemos clonar el repositorio en nuestro dispositivo:

```bash
# Clonar el repositorio usando ssh
git clone git@github.com:MiguelAmato/Tobichat.git Tobichat
```

Clonado el repositorio, instalaremos dentro de el directorio raíz del proyecto las dependencias con el siguiente comando:

```bash
# Para acceder al directorio raíz
cd Tobichat

# Para instalar las dependencias
npm install
```

## Uso

Para iniciar la aplicación en local ejecutar el siguiente comando:

```bash
npm run dev
```

## Explicación de las decisiones tomadas:

### ¿Por qué un generador de texto (chatbot)?
He optado por hacer un generador de texto con una API de Hugging Face ya que al ser primera vez que trabajo en un proyecto relacionado al uso y consumo de una API me parecía algo interesante de hacer para no tener experiencia previa.

### ¿Por qué React?
Al ser también primera vez trabajando en un proyecto de desarrollo web he optado por usar React ya que siempre me ha llamado la atención por su facilidad de aprenderlo y usarlo, como este proyecto se centraba mayormente en tener una interfaz de usuario cómoda para el usuario, React era una opción muy buena ya que esta biblioteca fue creada para facilitar la construcción de dichas interfaces.

### Modelo elegido
facebook/blenderbot-400M-distill es un bot muy bueno para lo que quería hacer ya que está destinado para los chatbots, este modelo genera respuesta y tema de conversación a cualquier input en inglés que le envíes. No es un modelo muy desarrollado, pero para lo que quería lograr que era un chatbot funcional que de conversación ha dado resultados positivos.

## Explicación de la estructura del proyecto

En cuanto a la estructura del proyecto se puede dividir en 3 partes:

- HTML

el index html que llama al main.jsx para empezar a renderizar todos los componentes en la web.

- React 

Contiene la lógica de los componentes, como se distribuyen y su contenido, así como la lógica de la llamada a la API, tomada de la documentación del modelo. En esta parte se llama a la API con la autorización de nuestra API_KEY dándole un input del usuario y esta generará una respuesta que se mostrará en pantalla.

Los componentes principales de la aplicación:

-- Tobichat.jsx: Es el componente principal donde también se llama a la API, aquí contiene el header de la página, la zona donde se encuentra el avatar de la aplicación y el chat como tal. Dentro del contenedor del chat es donde se manejan los mensajes con los componentes de MessageList, MessageInput y la llamada de la API.

-- MessageList.jsx: En este componente se gestionan todos los mensajes y se muestran en el contenedor del chat, se maneja para cada mensaje varios parámetros que luego se usaran para darle el estilo al mensaje como tal: El contenido del mensaje que se enseñará en una burbuja, si el mensaje es de un usuario o es del bot, ya que si es uno u otro la disposición de los mensajes es distinta, tienen un diseño distinto los mensajes y el icono también es distinto. también si el mensaje es error en la API, lo maneja dándole un color de error al mensaje pidiéndole que refresque la página.

-- MessageInput.jsx: Es el componente de la barra de texto que maneja el input que recibe del usuario, se compone de un icono del usuario, el input text donde el usuario escribe y el botón de enviar. Se usa una librería llamada lucide-react que me proporciona el diseño de los iconos de usuario y del botón de enviar. Al recibir el input se le hace trim para evitar espacios al inicio y final de la cadena y se le manda a la API para que genere la respuesta.

-- ThemeContext.jsx: Al implementar el modo oscuro y claro en la aplicación este componente es el que se encarga de cambiar de modo para que luego en el estilo de la aplicación se apliquen los cambios de estilo necesarios.

-- ThemeToggle.jsx: Es el botón con el que se cambia de modo oscuro a modo claro, se encuentra en el header del chat container.

- CSS

chat.css: En cuanto al estilo se optó por un estilo simple que pueda ser responsive, tenemos una paleta de colores para el modo claro que esta en el className .root donde se definen colores como el fondo, el color de los textos, el color principal, el color secundario y tenemos otro className que es el del modo oscuro con las mismas variables pero con la paleta de colores respectiva, esto facilita el cambio ya que en los componentes solo hace falta poner el color de la variable y cuando se cambie de modo cambiarán también todas las variables de todos los componentes. Se buscaba que la aplicación sea lo mas sencilla posible para que el usuario pueda entender a primera vista que es un chat.