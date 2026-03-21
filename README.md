🧩 STEP 1 — SUPABASE DATABASE SETUP:

1. Create project
Go to: https://supabase.com
Click New Project
Set:
Name: smartgrid
Password: (save it!)


2. Create table
Go to SQL Editor → New Query and run:

CREATE TABLE energy (
    id SERIAL PRIMARY KEY,
    voltage FLOAT,
    current FLOAT,
    power FLOAT,
    energy FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


3. Get DATABASE URL
Go to:

Project Settings → Database → Connection string → URI

You’ll get something like:
postgresql://postgres:PASSWORD@db.xxxx.supabase.co:5432/postgres


⚙️ STEP 2 — BACKEND SETUP (LOCAL → GITHUB)
1. Create project folder
smartgrid-backend/

Add these files:
server.py
database.py
ai_model.py
mqtt_listener.py
requirements.txt
Procfile
runtime.txt


2. Test locally (VERY IMPORTANT)

Open terminal:
pip install -r requirements.txt

Set env variable:
# Windows
set DATABASE_URL=your_supabase_url

# Linux / Mac
export DATABASE_URL=your_supabase_url


Run:
python server.py

Open browser:
http://localhost:10000/api/data

👉 Should return JSON


3. Push to GitHub
git init
git add .
git commit -m "backend ready"
git branch -M main
git remote add origin https://github.com/yourusername/smartgrid-backend.git
git push -u origin main


