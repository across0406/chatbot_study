# 1. Download and execute install.sh
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

# 2. Pull the models you want to use
```bash
# Select and download models that you want to use
ollama pull llama3:8b
ollama pull solar
```

# 3. Start serving service
```bash
# background service
ollama serve &
```