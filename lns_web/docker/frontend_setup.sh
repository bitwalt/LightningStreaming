#!/bin/sh
cd src/
npm install
# yarn install
# yarn serve --host 0.0.0.0
yarn build --watch --mode=production