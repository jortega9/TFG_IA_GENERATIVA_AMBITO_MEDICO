# Proyecto: TFG IA Generativa en el Ámbito Médico

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalados los siguientes programas y herramientas:

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) (versión recomendada: 3.8+)
- [Node.js](https://nodejs.org/) (versión recomendada: 16+)
- [HeidiSQL](https://www.heidisql.com/)
- Una clave API de [OpenAI](https://platform.openai.com/signup)

## Pasos de Instalación

1. **Clonar el repositorio**  
   Ejecuta el siguiente comando en tu terminal:
   ```bash
   git clone git@github.com:jortega9/TFG_IA_GENERATIVA_AMBITO_MEDICO.git
   ```

2. **Navegar al directorio del proyecto**  
   ```bash
   cd TFG_IA_GENERATIVA_AMBITO_MEDICO
   ```

3. **Crear y activar un entorno virtual (opcional pero recomendado)**  
   En sistemas Unix/Linux:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

4. **Instalar las dependencias de Python**  
   ```bash
   pip install -r requirements.txt
   ```

5. **Instalar las dependencias de Node.js**  
   ```bash
   npm install
   ```

6. **Configurar la base de datos**  
   - Abre HeidiSQL y crea la base de datos
   - urolobot
       - user
       - user_group
       - user_meta

7. **Configurar la clave de API de OpenAI**  
   - Crea un archivo `.env` en el directorio raíz del proyecto.
   - Añade la siguiente línea:
     ```
     OPENAI_API_KEY=tu_clave_aqui
     ```
