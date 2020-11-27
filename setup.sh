sudo apt  install golang-go
sudo apt  install cargo
sudo apt install python3-pip
sudo apt-get install curl
sudo apt-get install jq
git clone https://github.com/Edu4rdSHL/findomain.git
cd findomain
cargo build --release
sudo cp target/release/findomain /usr/bin/
cd ../
go get -u github.com/tomnomnom/httprobe
go get -u github.com/tomnomnom/assetfinder
go get -u github.com/tomnomnom/anew
pip3 install -r requirements.txt
export PATH=$PATH:$(go env GOPATH)/bin
