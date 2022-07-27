apt update && apt upgrade -y

apt install -y -q docker python3-dev build-essential python3-pip

cp ./requirements.txt /code/requirements.txt

pip3 install -r /code/requirements.txt

cp ./src /code

python3 /code/main.py