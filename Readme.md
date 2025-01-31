# HealthMangement

## Project Structure

### 1.**Backend:** healthbackend

**adminlteui:** Django admin UI, a third-party package that integrates the **AdminLTE** admin dashboard template with Django's built-in **admin panel**.

**api:** The Django restful api framework. Used for the backend for the healthmanagement project.

**healthbackend:** project main branch

**healthmanage:** The non-decoupled Django project, can be run seperately for the whole project function.

**medias:** project icon

**static:** css, html, js settings

### 2.**Frontend:** healthadmin

**dist:** the system default settings

**node_modules:** the library from 

**public:** healthadmin icon 

**src:** the frontend source code of the HealthManagement project



## Run the Project

### 1.Backend/Non-decoupled Django project

go to the project path

run 

```python
python manage.py runserver
```

Open the  development server from the given port

for example: http://127.0.0.1:8000/

### 2.Frontend:

**Installation**:

Install the application dependencies by running:

```sh
yarn
```

**Development**:

Start the application in development mode by running:

```sh
yarn dev
```

**Production**:

Build the application in production mode by running:

```sh
yarn build
```

open the frontend through the given port

### 3. env. settings

You'll find an `.env` file at the project root that includes a `VITE_JSON_SERVER_URL` variable. Set it to the URL of your backend.