#!/bin/bash

echo "Running smoke test for Chiller application..."

# Start Streamlit in a non-interactive mode and in the background
# We provide a dummy API key as it's just for starting, not full functionality
GEMINI_API_KEY="dummy_key_for_test" streamlit run src/app.py --server.port 8501 --server.headless true &

# Get the process ID of the Streamlit app
STREAMLIT_PID=$!

echo "Streamlit app started with PID: $STREAMLIT_PID"

# Give the app a few seconds to start up
sleep 10

# Check if the Streamlit process is still running
if kill -0 $STREAMILIT_PID > /dev/null 2>&1; then
    echo "Streamlit app is running. Smoke test PASSED."
    # Kill the Streamlit process
    kill $STREAMLIT_PID
    exit 0
else
    echo "Streamlit app failed to start or crashed. Smoke test FAILED."
    exit 1
fi