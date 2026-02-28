# MUIOGO Installation Guide

This guide provides step-by-step instructions for installing and running MUIOGO on Windows and macOS systems. The application runs locally on your computer and provides a web-based interface for working with CLEWS/OSeMOSYS models.

---

## Table of Contents

- [System Requirements](#system-requirements)
- [Windows Installation](#windows-installation)
- [macOS Installation](#macos-installation)
- [Running the Application](#running-the-application)
- [Verifying Installation](#verifying-installation)
- [Next Steps](#next-steps)
- [Quick Reference](#quick-reference)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11 or macOS 10.15+
- **Python**: 3.9 or higher (3.9, 3.10, 3.11, 3.12 supported)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 2 GB free space (more for model data)
- **Internet**: Required for initial setup only

---

## Windows Installation

### Step 1: Verify Prerequisites

Open Command Prompt (press `Win + R`, type `cmd`, press Enter) and verify:

```cmd
python --version
pip --version
git --version
```

**If any command fails:**
- **Python**: Download from [python.org](https://www.python.org/downloads/)
- **Git**: Download from [git-scm.com](https://git-scm.com/download/win)

### Step 2: Download MUIOGO

**Option A: Using Git (Recommended)**
```cmd
cd C:\Users\YourUsername\Documents
git clone https://github.com/EAPD-DRB/MUIOGO.git
cd MUIOGO
```

**Option B: Download ZIP**
1. Visit [github.com/EAPD-DRB/MUIOGO](https://github.com/EAPD-DRB/MUIOGO)
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to `C:\Users\YourUsername\Documents\MUIOGO`
5. Open Command Prompt and navigate to the folder:
   ```cmd
   cd C:\Users\YourUsername\Documents\MUIOGO
   ```

### Step 3: Create Virtual Environment

A virtual environment keeps MUIOGO's dependencies separate from other Python projects.

```cmd
python -m venv venv
```

### Step 4: Activate Virtual Environment

```cmd
venv\Scripts\activate
```

### Step 5: Install Dependencies

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

---

## macOS Installation

### Step 1: Verify Prerequisites

Open Terminal (press `Cmd + Space`, type "Terminal", press Enter) and verify:

```bash
python3 --version
pip3 --version
git --version
```

**If any command fails:**
- **Homebrew**: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- **Python**: `brew install python`
- **Git**: `brew install git`

### Step 2: Download MUIOGO

**Option A: Using Git (Recommended)**
```bash
cd ~/Documents
git clone https://github.com/EAPD-DRB/MUIOGO.git
cd MUIOGO
```

**Option B: Download ZIP**
1. Visit [github.com/EAPD-DRB/MUIOGO](https://github.com/EAPD-DRB/MUIOGO)
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract to your Documents folder
5. Open Terminal and navigate:
   ```bash
   cd ~/Documents/MUIOGO
   ```

### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
```

### Step 4: Activate Virtual Environment

```bash
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```
---
### Starting the Server

#### Windows

1. **Open Command Prompt**
2. **Navigate to MUIOGO folder**
   ```cmd
   cd C:\Users\YourUsername\Documents\MUIOGO
   ```

3. **Activate virtual environment**
   ```cmd
   venv\Scripts\activate
   ```

4. **Start the application**
   ```cmd
   cd API
   python app.py
   ```

#### macOS

1. **Open Terminal**
2. **Navigate to MUIOGO folder**
   ```bash
   cd ~/Documents/MUIOGO
   ```

3. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Start the application**
   ```bash
   cd API
   python app.py
   ```

### What You Should See

When the application starts successfully, you'll see output like:
```
/path/to/MUIOGO/WebAPP
/path/to/MUIOGO/WebAPP
/path/to/python
__main__
PORTTTTTTTTTTT
Serving on http://127.0.0.1:5002
```

### Accessing the Web Interface

1. **Open your web browser** (Chrome, Firefox, Safari, or Edge)
2. **Navigate to**: `http://127.0.0.1:5002` or `http://localhost:5002`
3. **You should see the MUIOGO interface**

### Stopping the Server

- Press `Ctrl + C` in the terminal/command prompt where the server is running
- Wait for the server to shut down gracefully

---

## Next Steps

After successful installation:

1. **Read the documentation**
   - `docs/ARCHITECTURE.md` - Understand the system structure
   - `CONTRIBUTING.md` - If you want to contribute

2. **Try the demo data**
   - Load the CLEWs Demo case
   - Run a simple model
   - Explore the results

3. **Learn the models**
   - CLEWS tutorial: [capacity.desa.un.org/article/introduction-clews](https://capacity.desa.un.org/article/introduction-clews)
   - OSeMOSYS docs: [osemosys.readthedocs.io](https://osemosys.readthedocs.io/)

4. **Join the community**
   - Watch the repository for updates
   - Participate in discussions
   - Report bugs or suggest features

---

## Quick Reference

### Starting the Application

**Windows:**
```cmd
cd C:\Users\YourUsername\Documents\MUIOGO
venv\Scripts\activate
cd API
python app.py
```

**macOS:**
```bash
cd ~/Documents/MUIOGO
source venv/bin/activate
cd API
python app.py
```

### Updating MUIOGO

**If installed via Git:**
```bash
cd MUIOGO
git pull origin main
pip install -r requirements.txt
```

**If downloaded as ZIP:**
- Download the latest ZIP
- Extract and replace old files
- Reinstall dependencies: `pip install -r requirements.txt`

---

## Support

For questions, issues, or contributions:

- **Issues**: [github.com/EAPD-DRB/MUIOGO/issues](https://github.com/EAPD-DRB/MUIOGO/issues)
- **Discussions**: [github.com/EAPD-DRB/MUIOGO/discussions](https://github.com/EAPD-DRB/MUIOGO/discussions)
- **Email**: See `README.md` for mentor contact information

---
