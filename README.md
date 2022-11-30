# CarService

CarService is a single-page application created using Flask and Vue.
The application allows you to manage parts, services, clients, and visits.

|![CarService_1](https://user-images.githubusercontent.com/100156421/204818197-26834ed8-664c-4b08-bdbb-cef44be84953.PNG)|![CarService_2](https://user-images.githubusercontent.com/100156421/204852387-9051efdd-8d3b-4962-9d94-a372734a9469.PNG)|
|:-------------------------:|:-------------------------:|
|![CarService_3](https://user-images.githubusercontent.com/100156421/204852521-287dd80a-17e6-4dae-b7b9-2b3b86778360.PNG)|![CarService_4](https://user-images.githubusercontent.com/100156421/204820704-e778753f-4d90-493d-a8b0-e1b318a83ff9.PNG)|

## Installation
**Requirements:**
You must have python 3.10, node.js, and git installed on your machine.

Clone repository:
```bash
$ git clone https://github.com/bartvbx/carservice-flask-vue.git
$ cd carservice-flask-vue/server
```

Set and run virtual environment:
```bash
$ py -m venv ./venv
$ . venv/Scripts/activate
```

Install required dependencies and run Flask application:
```bash
(venv)$ pip install -r requirements.txt
(venv)$ python run.py
```

Let's open a new terminal to run Vue application:
```bash
$ cd client
$ npm install
$ npm run dev
```

By default, Flask will run at localhost:5000, and Vue will use localhost:3000.

## Tech Stack

Backend:
- Flask
- SQLAlchemy
- Marshmallow
- SQLite

Frontend:
- Vue3
- BootstrapVue3

## License

[MIT](https://choosealicense.com/licenses/mit/)