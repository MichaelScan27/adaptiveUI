# Design and Evaluation of an Affective State Adaptive User Interface Using Simulated State Signals

## Flask Web Application

- Flask backend (backend/)
- HTML / CSS frontend (frontend/)
- TypeScript scripting language (compiles to JavaScript; frontend/src/)

## Instructions
1. Clone repo
```bash
git clone repo <url>
```
2. Create Python virtual environment
```bash
cd project/backend
python -m venv venv
source venv/bin/activate
```
3. Install Python (pip) dependencies
```bash
pip install -r requirements.txt
```
4. Install JavaScript (npm) dependencies
```bash
cd ../frontend
npm install 
```

Compile TypeScript:
```bash
npx tsc
```

5. Run the Flask server.
```bash
cd ../backend
python app.py
```

6. Go to 'http://127.0.0.1:5000' in a web browser.

## TypeScript 
This project uses TypeScript, a static typed language that compiles safely to JavaScript.

If you make changes to the TS, you must compile it to JS using the following command from project/frontend:
```bash
npx tsc
```

Ensure you have installed the Node Packages.  See step 4 in the instructions.

For more information on TypeScript: https://www.typescriptlang.org/