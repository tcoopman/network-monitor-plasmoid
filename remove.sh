#!/bin/bash

plasmapkg -t dataengine -r network-monitor-dataengine
rm kotnetlogindataengine.zip

plasmapkg -t plasmoid -r network-monitor-plasmoid
rm kotnetloginplasmoid.zip