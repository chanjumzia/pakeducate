#!/bin/bash

# Install dependencies
for package in flask flask-sqlalchemy gunicorn werkzeug; do
  if ! python -c "import $package" &> /dev/null; then
    echo "Installing $package..."
    pip3 install $package
  fi
done

# Run the application
python app.py