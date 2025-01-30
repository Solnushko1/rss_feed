# AppRSSFeed

### Running locally

Run the following commands to bootstrap your environment if you are unable to run the application using Docker

```bash
cd rss_feed
pip install -r requirements/dev.txt
npm install
npm run-script build
npm start  # run the webpack dev server and flask server using concurrently
```

Go to `http://localhost:5000`. You will see a pretty welcome screen.

If you use Windows, then you should read this article on installing node.js
https://phoenixnap.com/kb/install-node-js-npm-on-windows

If you use MacOs. Use your homebrew ```brew install node```

#### Before the work of the program, you need to initialize data from the env.example file
**Windows** $env:FLASK_APP = "autoapp.py"   And so with the rest

**MacOs** export FLASK_APP=autoapp.py


#### Fill in Gigachat data in App

The necessary variables for filling are located in the envs .env.example folder

#### RSS Feeds

To change the received newsletter of the novations, you need to change URL filling_db

#### Database Initialization (locally)

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration

```bash
flask db init
flask db migrate
flask db upgrade
```


## Running Tests/Linter

To run all tests, run

```bash
flask test
```
