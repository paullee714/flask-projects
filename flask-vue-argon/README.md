# flask-vue-argon

## Project Sturcture

```bash
.
├── README.md
├── backend
│   ├── app.py
│   ├── back.dev.Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── frontend
│   ├── CHANGELOG.md
│   ├── ISSUES_TEMPLATE.md
│   ├── LICENSE.md
│   ├── README.md
│   ├── babel.config.js
│   ├── front.dev.Dockerfile
│   ├── node_modules
│   ├── package.json
│   ├── public
│   ├── src
│   ├── vue.config.js
│   └── yarn.lock
└── requirements.txt
```

## how to run?

- Dockerfile로 실행

    ```bash
    $ docker-compose --buid up
    ```

- 로컬 개발환경에서 실행

    ```bash
    # frontend 폴더에서
    $ yarn install && yarn run serve
    ```

    ```bash
    # backend 폴더에서
    $ python3 -m pip virtualenv 
    $ virtualenv venv && source venv/bin/activate
    (venv) $ pip install flask flask-cors python-dotenv
    (venv) $ python3 app.py
    ```