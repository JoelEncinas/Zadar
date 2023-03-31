

# 🦝 Zadar
<img src="https://img.shields.io/badge/-python-blue" alt="python" style="max-width: 100%;"> <img src="https://img.shields.io/badge/-flask-white" alt="flask" style="max-width: 100%;"> <img src="https://img.shields.io/badge/-sqlite3-gray" alt="sqlite3" style="max-width: 100%;"> <img src="https://img.shields.io/badge/-jinja2-red" alt="jinja2" style="max-width: 100%;"> <img src="https://img.shields.io/badge/-bootstrap-purple" alt="bootstrap" style="max-width: 100%;"> 

A social media type page where you can share everything about the temtem universe, your opinions about the features of the game and discussions related to battle strategies.

Including information about every Temtem, their traits, techniques, and different stats, presented in a delightful UI.

Tools like the classic type chart, which lets you check your temtem weaknesses and strengths and a technique effectiveness calculator.

## 🚀 Things I learned about
- **Flask**

  - *Creating a full-stack Flask application*
  - *User authentication*
    - *session*
    - *before_app_request decorator for logged user*
  - *Routing*
    - *Using parameters & requests arguments*
    - *GET & POST requests*
    - *render_template & url_redirect*
  - *Blueprints*
  - *Error handling with flash*

- **Jinja2**
  - *extends and includes*
  - *modular design of templates*
  - *control structures*

- **SQL**

  - *Database creation/management*
  - *CRUD operations*
  
- **Python**

  - *Data handling & using APIs*
  - *General syntax*
  
## 📷 App screenshots
<img src="https://github.com/JoelEncinas/Lux/blob/main/demo_imgs/demo1.PNG" alt="demo" width="220" height="360"/> <img src="https://github.com/JoelEncinas/Lux/blob/main/demo_imgs/demo2.PNG" alt="demo" width="220" height="360"/> <img src="https://github.com/JoelEncinas/Lux/blob/main/demo_imgs/demo3.PNG" alt="demo" width="220" height="360"/> <img src="https://github.com/JoelEncinas/Lux/blob/main/demo_imgs/demo4.PNG" alt="demo" width="220" height="360"/> <img src="https://github.com/JoelEncinas/Lux/blob/main/demo_imgs/demo5.PNG" alt="demo" width="220" height="360"/> <img src="https://github.com/JoelEncinas/Lux/blob/main/demo_imgs/demo6.PNG" alt="demo" width="220" height="360"/> <img src="https://github.com/JoelEncinas/Lux/blob/main/demo_imgs/demo7.PNG" alt="demo" width="220" height="360"/>


## 💿 Test the app locally

Install dependencies:

- `pip install -r requirements.txt`

Create a virtual environment:

- `py -m venv env`

Activate the virtual environment: 

- `.\env\Scripts\activate`

Init the database:

- `flask --app zadar init-db`

Run the app:

- `flask --app zadar run --debug`

Open http://localhost:5000 to view it in your browser.
