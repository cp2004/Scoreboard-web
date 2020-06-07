# Table Tennis Scoreboard - A web based scoreboard with optional RGB Matrix support

![Python application](https://github.com/cp2004/Scoreboard-web/workflows/Python%20application/badge.svg?branch=master)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e0d483520e2c421396937d67a027308c)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=cp2004/Scoreboard-web&amp;utm_campaign=Badge_Grade)

---
## Features
  -Complete user authentication, with encrypted passwords
  -Table tennis scoreboard (Up to 11 points) with tiebreak and serving indicator
   -Saving games from the scoreboard to track progress
  -Statistics views: User stats as well as a global league table
  -Optional RGB Matrix support

---
## Credits
  -[Flask](https://flask.palletsprojects.com/en/1.1.x/) Webserver
  -[Bootstrap 4](https://getbootstrap.com/) Site styling
  -[Data Tables](https://datatables.net/) Data table for home page
  -[Fontawesome](https://fontawesome.com/) Icons

---
## Screenshots
![Homepage screenshot](resources/Home.jpg)![Homepage screenshot](resources/scoreboard.jpg)
![Homepage screenshot](resources/user.jpg)
![Homepage screenshot](resources/win.jpg)

---
## Installation
1. Clone the repo `git clone https://github.com/cp2004/Scoreboard-web`

2. Browse the config file config.py, make any changes:
    - Path to RGB Matrix (If required)

3. Create a virtual environment if needed (`python -m virtualenv NAME`)

4. Install dependencies `pip install -r requirements.txt`

5. Run with `flask run`

6. PLAY!
