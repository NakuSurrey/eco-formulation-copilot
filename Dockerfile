# ============================================================
# Eco-Formulation Copilot — Docker Container Definition
# ============================================================
# This file tells Docker how to package the entire application
# into a single portable container that runs anywhere.
#
# HOW IT WORKS (step by step):
#   Step 1 → Start from an official Python image (the "base")
#   Step 2 → Set the working directory inside the container
#   Step 3 → Copy requirements.txt and install dependencies
#   Step 4 → Copy the rest of the project files into the container
#   Step 5 → Expose port 8501 (Streamlit's default port)
#   Step 6 → Define the command to run when the container starts
#
# HOW TO USE:
#   Build:  docker build -t eco-formulation-copilot .
#   Run:    docker run -p 8501:8501 --env-file .env eco-formulation-copilot
#   Open:   http://localhost:8501
# ============================================================

# ----------------------------------------------------------
# Step 1: Base Image
# ----------------------------------------------------------
# python:3.10-slim is a lightweight version of Python 3.10.
# "slim" means it has the bare minimum OS packages installed.
# This keeps the container small (~150MB instead of ~900MB).
# ----------------------------------------------------------
FROM python:3.10-slim

# ----------------------------------------------------------
# Step 2: Working Directory
# ----------------------------------------------------------
# WORKDIR creates a folder called /app inside the container
# and sets it as the current directory. Every command after
# this runs from /app. Think of it as doing "cd /app".
# ----------------------------------------------------------
WORKDIR /app

# ----------------------------------------------------------
# Step 3: Install Dependencies
# ----------------------------------------------------------
# We copy requirements.txt FIRST (before the rest of the code)
# because Docker caches each step. If requirements.txt has not
# changed, Docker skips reinstalling packages — saving minutes
# on every rebuild. This is called "layer caching".
#
# --no-cache-dir tells pip: do not store downloaded packages
# on disk after installing them. This keeps the container small.
# ----------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------
# Step 4: Copy Project Files
# ----------------------------------------------------------
# The "." on the left  = everything in the build context (your project folder)
# The "." on the right = the WORKDIR inside the container (/app)
#
# .dockerignore controls which files are EXCLUDED from this copy.
# ----------------------------------------------------------
COPY . .

# ----------------------------------------------------------
# Step 5: Expose the Port
# ----------------------------------------------------------
# EXPOSE does not actually open the port. It is documentation
# that tells anyone reading this Dockerfile: "This container
# expects traffic on port 8501." The actual port mapping
# happens at runtime with the -p flag (docker run -p 8501:8501).
# ----------------------------------------------------------
EXPOSE 8501

# ----------------------------------------------------------
# Step 6: Health Check
# ----------------------------------------------------------
# Docker periodically runs this command to check if the app
# is still responding. If it fails 3 times in a row, Docker
# marks the container as "unhealthy".
#
# curl: sends an HTTP request to the Streamlit health endpoint
# --interval=30s: check every 30 seconds
# --timeout=10s: wait up to 10 seconds for a response
# --retries=3: mark unhealthy after 3 consecutive failures
# ----------------------------------------------------------
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# ----------------------------------------------------------
# Step 7: Start Command
# ----------------------------------------------------------
# CMD is the command Docker runs when the container starts.
#
# streamlit run app.py         → launches the Streamlit server
# --server.port=8501           → listen on port 8501
# --server.address=0.0.0.0    → accept connections from ANY IP
#                                 (not just localhost — required
#                                  for Docker networking to work)
# --server.headless=true       → do not try to open a browser
#                                 (there is no browser inside a container)
# --browser.gatherUsageStats=false → disable Streamlit telemetry
# ----------------------------------------------------------
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
