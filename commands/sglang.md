# Caution for memory!!!!!
# 1. Install packages
```bash
sudo apt update
sudo apt install autoconf automake libtool pybase64 pydantic orjson
```

# 2. (Optinoal) Delete pip cache
```bash
pip cache purge
```

# 3. Force install sglang and vllm with build
```bash
pip install --no-cache-dir --no-binary :all: "sglang[vllm]"
pip install "sglang[all]"
```

# 4. Execute SGLang server as vLLM backend
```bash
python -m sglang.launch_server \
    --model-path upstage/SOLAR-10.7B-v1.0 \
    --port 8001 \
    --host 127.0.0.1
```