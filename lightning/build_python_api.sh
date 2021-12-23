virtualenv lnd

source lnd/bin/activate

pip install grpcio grpcio-tools googleapis-common-protos

git clone https://github.com/googleapis/googleapis.git

curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto

python -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. rpc.proto
