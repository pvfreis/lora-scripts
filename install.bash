echo "Creating python venv..."
python3 -m venv venv
source venv/bin/activate

pip install wheel

echo "Installing torch & xformers..."

pip install torch==2.0.0+cu118 torchvision==0.15.1+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
pip install xformers==0.0.17 -i https://pypi.python.org/simple


echo "Installing deps..."
cd ./sd-scripts

pip install --upgrade -r requirements.txt
pip install --upgrade lion-pytorch lycoris-lora

echo "Install completed"
