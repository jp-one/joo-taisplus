@echo off
docker-compose -p autostart-odoo-addons-dev -f .devcontainer/docker-compose.yml -f .devcontainer/odoo/docker-compose-autostart.yml up --build
pause