sudo apt  install cargo
sudo apt install python3-pip
pip3 install -r requirements.txt
git clone https://github.com/Edu4rdSHL/findomain.git
cd findomain
cargo build --release
sudo cp target/release/findomain /usr/bin/
cd ../
