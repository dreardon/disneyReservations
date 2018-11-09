mkdir -p bin/

echo "Disney Reservations Setup"
echo =============================================================================================
echo "Downloading Chrome Driver..."
arch=$(getconf LONG_BIT)
kernel=$(uname)
LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
if [ $kernel == "Darwin" ]; then
  curl -SL https://chromedriver.storage.googleapis.com/$LATEST/chromedriver_mac64.zip > chromedriver.zip
else
  if [ $arch == "64" ]; then
    curl -SL https://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip > chromedriver.zip
  else
    curl -SL https://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux32.zip > chromedriver.zip
  fi
  curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
  unzip headless-chromium.zip -d ./bin/
fi
unzip chromedriver.zip -d ./bin/
sudo ln -s $PWD/bin/chromedriver /usr/local/bin/chromedriver

# Clean
rm headless-chromium.zip chromedriver.zip