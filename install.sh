#!/bin/bash

cd dataengine
zip -r ../kotnetlogindataengine.zip .
cd ..
plasmapkg -t dataengine -i kotnetlogindataengine.zip

cd applet
zip -r ../kotnetloginplasmoid.zip .
cd ..
plasmapkg -t plasmoid -i kotnetloginplasmoid.zip