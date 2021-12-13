# Setup a default node for the  LN Deamon 

# Clone the repo and move into it:
git clone https://github.com/mably/lncli-web $GOPATH/src/github.com/mably/lncli-web
cd $GOPATH/src/github.com/mably/lncli-web

# Install dependencies
npm install

# Setup default configuration files
"./node_modules/.bin/gulp" bundle

# Setup cert file
# Enter the Lnd home directory, located by default at ~/.lnd on Linux or
# /Users/[username]/Library/Application Support/Lnd/ on Mac OSX
# $APPDATA/Local/Lnd on Windows. Also change '/CN=localhost/O=lnd' to '//CN=localhost\O=lnd' if you are using Git Bash.
cd ~/.lnd
openssl ecparam -genkey -name prime256v1 -out tls.key
openssl req -new -sha256 -key tls.key -out csr.csr -subj '/CN=localhost/O=lnd'
openssl req -x509 -sha256 -days 36500 -key tls.key -in csr.csr -out tls.cert
rm csr.csr
cp tls.cert $GOPATH/src/github.com/mably/lncli-web/lnd.cert

# Start the server to point to our Alice node:
cd $GOPATH/src/github.com/mably/lncli-web
node server --lndhost=localhost:10001

# Check out the available command line arguments
node server --help