#!/bin/bash
pkill -9 java 2>/dev/null
export GDK_BACKEND=x11
export _JAVA_AWT_WM_NONREPARENTING=1
export JAVA_TOOL_OPTIONS="-Dprism.order=sw"
echo "🚀 Lancement JavaFX..."
mvn clean compile exec:java -Dexec.mainClass="com.app.App"