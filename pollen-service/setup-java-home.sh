#!/bin/bash
# Script to set up JAVA_HOME for the Allermind Pollen Service

# Find Java installation
JAVA_HOME=$(/usr/libexec/java_home -v 21)
echo "Found Java at: $JAVA_HOME"

# Export to current shell
export JAVA_HOME
export PATH=$JAVA_HOME/bin:$PATH

# Instructions for adding to profile
echo ""
echo "To make this permanent, add these lines to your ~/.zshrc or ~/.bash_profile:"
echo "export JAVA_HOME=$JAVA_HOME"
echo "export PATH=\$JAVA_HOME/bin:\$PATH"
echo ""
echo "Current Java version:"
java -version
