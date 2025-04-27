# Proyecto: TFG IA Generativa en el Ámbito Médico

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalados los siguientes programas y herramientas:

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) (versión recomendada: 3.12.7)
- [Node.js](https://nodejs.org/) (versión recomendada: 20.18.0)
   - ```bash
      curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
      nvm install 20
      sudo apt install npm
     ```
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
   
3. **Instalar las dependencias de Python**  
   - Selecciona el interprete de python 3.12.7
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. **Instalar las dependencias de Node.js**  
   ```bash
   cd frontend
   npm install
   ```

6. **Configurar la base de datos**  
   - Abre HeidiSQL y crea la base de datos
   - urolobot
       - user
          - ![image](https://github.com/user-attachments/assets/da2046ad-4b30-40fc-b332-2b3675253ab1)
       - user_group
          - ![image](https://github.com/user-attachments/assets/f0618a6d-4de2-418c-81cc-349d6fdb44c9)
       - user_meta
          - ![image](https://github.com/user-attachments/assets/3af4094a-4f2b-49a5-8db7-491d76c7013f)

7. **Configurar archivo .env**  
   - Crea un archivo `.env` en el directorio raíz del proyecto basandote en env.template .
    ```bash
   cp .env.template .env
   ```
## Modo De Uso
- Arrancar el backend de la aplicación

```bash
   cd backend
   uvicorn src.app:app --reload --port 8000 --host 0.0.0.0 --env-file ../.env
```

- Arrancar frontend de la aplicación

```bash
   cd frontend
   npm run dev
```

## Notas Adicionales

- Asegurate de tener bien configurado el archivo .env
- Asegurate de tener creada la base de datos sql (HeidiSQL) para el control de usuarios de la aplicación
- Asegurate de tener todas las dependencias instaladas (python y node.js)
