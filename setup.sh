mkdir -p bin/

# Get chromedriver
curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
unzip chromedriver.zip -d ./bin/

# Get Headless-chrome
curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
unzip headless-chromium.zip -d ./bin/

# Clean
rm headless-chromium.zip chromedriver.zip

virtualenv venvs --python=python3
source venvs/bin/activate
pip install -r requirements.txt