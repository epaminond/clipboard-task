## Dependencies
* Python 3.5
* Virtualenv
* Node.js (>= v6.0.0)
* mongodb >= 3.4.0
* Yarn

## Installation
* Set up a virtual enviroment with:
  ```bash
  virtualenv venv
  source venv/bin/activate
  ```
* Install python dependencies in requirements.txt by:
  ```bash
  pip install -r ingestion/requirements.txt
  ```
* Install node dependencies with:
  ```bash
  npm install
  ```

### Running in development mode
1. Start webpack-dev-sever by typing ```npm start```
2. With your virtual enviroment enabled, run ```npm pipeline```

### Running in production mode
1. set `NODE_ENV=production` in your `.env` file
2. Compile webpack using ```npm run build```
3. With your virtual enviroment enabled, run ```npm pipeline```


1. ``` cp sample.env .env ``` and set values as appropriate.

2. Run `npm run forever-start` and navigate to `<ip>:<port> (default=7999)`.

###  Developing:
1. Set `NODE_ENV=development` in `.env`.
2. Run `npm run dev`
