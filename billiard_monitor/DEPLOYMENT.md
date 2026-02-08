# Deployment Guide for Render.com

This guide explains how to host your Billiard Monitor application on Render as a web service using SQLite.

## Prerequisites

1.  A [GitHub](https://github.com/) account.
2.  A [Render](https://render.com/) account.

## Step 1: Push to GitHub

1.  Initialize a git repository if you haven't already:
    ```bash
    git init
    git add .
    git commit -m "Initial commit for deployment"
    ```
2.  Create a new repository on GitHub.
3.  Push your code to the new repository:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    git branch -M main
    git push -u origin main
    ```

## Step 2: Create Web Service on Render

1.  Log in to your Render dashboard.
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub account if not already connected.
4.  Search for your repository (`billiard_monitor`) and click **Connect**.

## Step 3: Configure Service Settings

Fill in the details as follows:

-   **Name**: `billiard-monitor` (or any name you like)
-   **Region**: Choose the one closest to you (e.g., Singapore for Asia).
-   **Branch**: `main`
-   **Root Directory**: Leave empty (defaults to root).
-   **Runtime**: **Python 3**
-   **Build Command**: `./build.sh`
-   **Start Command**: `gunicorn billiard_monitor.wsgi:application`
-   **Plan**: **Free** (for hobby projects)

## Step 4: Environment Variables (Optional)

In the "Environment" tab (or "Advanced" section during creation), you can add:

-   `PYTHON_VERSION`: `3.11.0` (or your preferred version)
-   `SECRET_KEY`: Generate a random string for security. If not set, the app uses a default insecure key.
-   `DEBUG`: `False` (default is False on Render implicitly via our settings logic, but good to be explicit).

## Step 5: Deploy

Click **Create Web Service**. Render will:
1.  Clone your repository.
2.  Run the `build.sh` script (install dependencies, collect static files, migrate database).
3.  Start the app using `gunicorn`.

Once the deployment shows "Live", you can click the URL (e.g., `https://billiard-monitor.onrender.com`) to visit your site.

## Important Note regarding SQLite

Since you requested **SQLite**, please be aware of the "Ephemeral Filesystem" on Render's free tier (and most web services).
-   **Data Persistence**: If the web service restarts or redeploys, **ALL DATA in the SQLite database will be LOST** because the file is deleted.
-   **Solution 1 (Recommended)**: Use Render's managed **PostgreSQL** database (Free tier available).
-   **Solution 2 (Persistent Disk)**: You can attach a "Disk" to your service on Render (requires a paid plan) and store the `db.sqlite3` file there.
-   **For Demo Only**: If this is just a demo and you don't care about losing data on restart, the current setup works fine.

To use PostgreSQL instead:
1.  Create a PostgreSQL database on Render.
2.  Copy the `Internal Database URL`.
3.  Add it as an environment variable `DATABASE_URL` in your Web Service.
4.  Update `settings.py` to use `dj_database_url` to parse it (requires installing `dj-database-url` and `psycopg2-binary`).
