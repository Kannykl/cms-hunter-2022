#! /bin/bash
output=$(which python3.10)
if [[ -z $output ]]
then
  echo "There is no python in your system. Now it will be installed"
  sudo apt-get install build-essential checkinstall
  sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
  cd /opt
  sudo apt-get install wget
  sudo wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
  sudo tar xzf Python-3.10.0.tgz
  cd Python-3.10.0
  sudo ./configure --enable-optimizations
  sudo make altinstall
  version=`python3.10 -V`
  cd ..
  if [[ ! -z $version ]]
  then
    echo "Python installation complete!"
  else
    echo "Python installation didnt complete. Something goes wrong.Try again"
    exit 1
  fi
fi

sudo apt install ruby
sudo apt install build-essential libcurl4-openssl-dev libxml2 libxml2-dev libxslt1-dev ruby-dev  libgmp-dev zlib1g-dev -y
sudo gem install wpscan -y

sudo apt install python3-pip
pip install virtualenv
python3.10 -m venv cms_hunter_env
source cms_hunter_env/bin/activate
pip install -r requirements.txt
sudo apt update
sudo apt install redis-server
sudo systemctl restart redis

python3 manage.py makemigrations cms_hunter
python3 manage.py migrate
python3 manage.py initadmin
celery -A config.celery worker --loglevel=INFO | python3 manage.py runserver 
