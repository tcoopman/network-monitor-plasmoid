#!/bin/bash

cd dataengine
zip -r ../kotnetlogindataengine.zip
cd ..
plasmapkg -i kotnetlogindataengine.zip

cd applet
zip -r ../kotnetloginplasmoid.zip
cd ..
plasmapkg -i kotnetloginplasmoid.zip