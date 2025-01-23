exec > /tmp/autoexpense_webapp.log 2>&1

env

# You may need to add here things like : source .../.bashrc

echo "Starting autoexpense webapp..."

cd /app
/root/.local/bin/uv run fastapi run app.py --port 80
