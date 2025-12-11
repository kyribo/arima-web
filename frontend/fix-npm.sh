#!/bin/bash
cd /home/rizky/project/arima-web/frontend
echo "Removing node_modules and package-lock.json..."
rm -rf node_modules package-lock.json
echo "Running npm install..."
npm install
echo "Done! The issue should be resolved."
