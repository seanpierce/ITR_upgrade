# (Yet Another) Intro To Rhythm Upgrade

This repository contains the latest upgrade of **Intro To Rhythm (I2R)**.  
The goals of this upgrade are threefold:  

1. **Update** platform versions to the latest stable releases  
2. **Modernize** existing features  
3. **Remove** deprecated or unnecessary legacy features  

---

## What is Intro To Rhythm?

**Intro To Rhythm (I2R)** is a freeform mix series and live-streaming audio station that has been running since 2017.  
All episodes and content are created and owned by the contributing artists, produced exclusively for I2R.  

Beyond broadcasting, I2R supports open-source projects and the spirit of collaboration and experimentation.  
If you’re interested in building your own live-streaming station or podcast platform, feel free to explore the source code (MIT License).  

Questions and comments: **hello@introtorhythm.com**

---

## What’s Changing?

In this upgrade:  

- **Frameworks**: Django `3.x → 4.x`, Vue `2.x → 3.x`  
- **Dependencies**: Updated across the board  
- **Features**: Some deprecated features removed, core features modernized  

---

### What’s Staying

- **Streaming**: Live, pre-recorded, and syndicated shows  
- **Chat**: Rebuilt with Socket.io (moving away from Firebase)  
- **Content API**: Migrating from a custom solution to Django REST Framework + model serialization (easier to maintain and industry-standard)  
- **Automated scheduling**: Existing cron + Python script system remains, with room for improvements  

---

### What’s Leaving

- **Subscribers**: Email subscriptions haven’t been used in years. This may return in a more thoughtful, enhanced form later.  
- **Episodes**:  
  - Early on, I2R focused on pre-recorded episodes, but once live streaming became the core, episode traffic dropped off.  
  - Maintaining and hosting large audio files was costly and time-consuming, so the feature has been deprecated.  
  - That said, if I2R gains more consistent live programming, automated episode management could be revisited in the future.  

---

## Dependencies

- **Python** 3.13.7  
- **Node** 26.7.0  

---

## Project Versions

- **Django** 4.2  
- **Vue** ^3.5.18  

## Installation and Local Usage

```bash
# Ensure Python v3.13.7 is installed and active in your OS
# Ensure Node v26.7.0 is installed and active in your OS

# Clone this repository
git clone https://github.com/seanpierce/ITR_upgrade

# Create BE virtual environment
cd introtorhythm_backend
python3 -m venv venv
source ./venv/bin/activate # or ./venv/Scripts/activate on Windows

# Install BE dependencies
pip install -r requirements.txt

# Create and migrate database
python3 manage.py migrate

# Create superuser (admin account)
python3 manage.py createsuperuser

# Run BE local dev server
python manage.py runserver

# Install FE dependencies
cd [project root]/introtorhythm_frontend
npm install

# Configure .env variables - reference the .env.example file for reference. Create a .env.local and a .env.production file and add the example keys and values.

# Run FE local dev server
npm run dev

# Run chat app local dev server
cd [project root]/introtorhythm_frontend/src/chat
node ./server.ts
```

![Intro To Rhythm Logo](introtorhythm_frontend\src\assets\images\i2r-bg-big-tall.png)