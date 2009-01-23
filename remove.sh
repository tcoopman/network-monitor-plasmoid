#!/bin/bash

plasmapkg -t dataengine -r kotnet-dataengine
rm kotnetlogindataengine.zip

plasmapkg -t plasmoid -r kotnet-plasmoid
rm kotnetloginplasmoid.zip