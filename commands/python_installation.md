* pyenv installation
```bash
curl https://pyenv.run | bash
```

1. Update and install the essential packages
```bash
sudo apt update
sudo apt install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev libgdbm-dev libnss3-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev \
liblzma-dev
```

2. Download compressed python source that you want to install and use
- from python.org => https://www.python.org/downloads/source/
```bash
wget https://www.python.org/ftp/python/3.11.14/Python-3.11.14.tgz
```

3. Extract the compressed python source
```bash
# tgz file
tar -xvzf [file_name].tgz
# tar.xz file
tar -xvf [file_name].tar
```

4. Move extracted directory
```bash
cd [extracted_directory]
```

5. (Optinoal) Clean (when you try configure and make again)
```bash
make distclean
```

6. Configure
```bash
./configure --enable-optimizations
```

7. Make
```bash
# nproc is for the number of cpu cores, for improving build speed
make -j $(nproc)
```

8. Make install
```bash
sudo make altinstall
```

9. (Optional) Python Version Management
- Check python binary path
```bash
which python3.11
```
- Register python with priority
```bash
sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1
```

- Change version through the following command
```bash
sudo update-alternatives --config python
There are 2 choices for the alternative python (providing /usr/bin/python).

  Selection    Path                       Priority   Status
------------------------------------------------------------
* 0            /usr/local/bin/python3.9    1         auto mode
  1            /usr/local/bin/python3.11   1         manual mode
  2            /usr/local/bin/python3.9    1         manual mode

Press <enter> to keep the current choice[*], or type selection number: 1
update-alternatives: using /usr/local/bin/python3.11 to provide /usr/bin/python (python) in manual mode
```

