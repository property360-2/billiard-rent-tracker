# Step-by-Step PythonAnywhere Deployment Guide

This guide will help you host your **Billiard Monitor** Django app on PythonAnywhere.

## Step 1: Upload Your Code

1.  **Login** to your [PythonAnywhere dashboard](https://www.pythonanywhere.com/).
2.  Open a **Bash Console** from the "Consoles" tab.
3.  Clone your repository (if it's on GitHub):
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    ```
    *Alternatively, you can upload a zip file via the "Files" tab and extract it.*

4.  Navigate into your project folder:
    ```bash
    cd YOUR_REPO_NAME
    ```

## Step 2: Create a Virtual Environment

In the same Bash Console, create a virtual environment to install your dependencies:

```bash
mkvirtualenv --python=/usr/bin/python3.10 billiard-venv
pip install -r requirements.txt
```
*(You can use python 3.9 or 3.11 depending on what's available on your PythonAnywhere account).*

## Step 3: Set Up the Web App

1.  Go to the **Web** tab in the PythonAnywhere dashboard.
2.  Click **Add a new web app**.
3.  Select **Manual Configuration** (do NOT select Django, as we already have the code).
4.  Choose the **Python version** you used for your virtual environment (e.g., Python 3.10).
5.  After the web app is created, configure the following sections:

### Code Section:
-   **Source code**: `/home/YOUR_USERNAME/YOUR_REPO_NAME`
-   **Working directory**: `/home/YOUR_USERNAME/YOUR_REPO_NAME`

### Virtualenv Section:
-   **Virtualenv**: `/home/YOUR_USERNAME/.virtualenvs/billiard-venv`

### Static Files Section:
You need to map your static files so they load correctly:
1.  **URL**: `/static/`
2.  **Directory**: `/home/YOUR_USERNAME/YOUR_REPO_NAME/staticfiles`

*(Note: Run `python manage.py collectstatic` in your console first if you haven't already).*

## Step 4: Configure WSGI File

1.  In the **Web** tab, under the **Code** section, find the **WSGI configuration file** link and click it.
2.  Delete everything in that file and replace it with this:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOUR_USERNAME/YOUR_REPO_NAME'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'billiard_monitor.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual PythonAnywhere username and folder name.*

## Step 5: Database and Migrations

Go back to your **Bash Console** and run the migrations:

```bash
python manage.py migrate
```

## Step 6: Reload and Visit

1.  Go back to the **Web** tab.
2.  Click the big green **Reload** button.
3.  Visit your site at `http://YOUR_USERNAME.pythonanywhere.com`.

---

## Important Tips for PythonAnywhere:
-   **Persistence**: Unlike Render, your `db.sqlite3` file **is persistent** on PythonAnywhere. Your data will not be lost when you reload the app.
-   **Media Files**: If you add image uploads later, you'll need to add another mapping in the **Static Files** section for `/media/`.
-   **Environment Variables**: If you want to use a real `SECRET_KEY`, you can set it in a `.env` file and use `python-dotenv` or set it in your WSGI file.
