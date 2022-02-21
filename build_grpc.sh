python3 -m grpc_tools.protoc --proto_path=messages messages/session.proto \
--python_out=. --grpc_python_out=messages
echo "Generated protobuf and gRPC callbacks for ./messages/session.proto !"