w#!/bin/bash
protoc messages/session.proto --python_out messages/
echo "Messages generated using protoBuf!"