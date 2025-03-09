#!/bin/bash
ollama serve &
sleep 5

# check if model exist
if ! ollama list | grep -q "llama3.1:8b"; then
    echo "Model llama3.1:8b not found pulling model"
    ollama pull llama3.1:8b
fi



# ollama serve &
pid=$!
wait $pid