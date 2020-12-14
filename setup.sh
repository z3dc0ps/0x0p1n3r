sudo snap install amass
sudo apt install amass
sudo apt install httpie
sudo apt install golang-go
sudo apt install cargo
sudo apt install python3-pip
sudo apt install curl
sudo apt install jq
pip3 install -r ./requirements.txt
git clone https://github.com/Edu4rdSHL/findomain.git tools/findomain
cd tools/findomain/
cargo build --release
sudo cp target/release/findomain /bin/
cd ../../
GO111MODULE=on go get -u -v github.com/lc/gau
go get -u github.com/tomnomnom/httprobe
go get -u github.com/tomnomnom/assetfinder
go get -u github.com/tomnomnom/anew
GO111MODULE=on go get -u -v github.com/projectdiscovery/httpx/cmd/httpx
export PATH=$PATH:$(go env GOPATH)/bin
