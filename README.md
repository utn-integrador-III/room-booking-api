# room-booking-api

1. cd Managment_API
2. create virtual env: `python3 -m venv venv`
3. create .env file
4. run pip3 install -r requirements.txt
5. If you are using vs code, go to `run and debug` and create a launch.json file and add the following (for env file, copy your path and paste it): { "version": "0.2.0",
   "configurations": [
   {
   "name": "Python: Current File",
   "type": "debugpy",
   "request": "launch",
   "program": "./app.py",
   "console": "integratedTerminal",
   "envFile": ".env"
   }
   ]
   }

6. Run the project under 'Run and debug'
7. If you get mongo certificate issues, run the following command with the proper python version on your system: `open "/Applications/Python 3.10/Install Certificates.command" `
