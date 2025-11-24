# Soccer Data Scraper

Step-by-step guide to run the scraper inside an isolated Python environment.

## Requirements
- Python 3.12.x recommended (Python 3.13 currently fails building `lxml` because wheels are not yet published)
- pip

## Install Python 3.12 (if you don't have it)
- Easiest GUI: download and install the official macOS 3.12 installer from https://www.python.org/downloads/macos/ (then restart your shell).
- Quick via Homebrew: `brew install python@3.12` (gives you `python3.12` in `/opt/homebrew/bin`).
- Using pyenv (already installed):  
  1) `pyenv install 3.12.6` (or latest 3.12.x)  
  2) In this repo: `pyenv local 3.12.6` (writes `.python-version` so pyenv shims use 3.12 here)  
  3) Verify: `python --version` should show 3.12.x before creating the venv.

## Setup
1. From the project root, create (or recreate) the virtual environment with Python 3.12: `python3.12 -m venv venv` (or, after `pyenv local 3.12.6`, just `python -m venv venv`). The existing `venv/` in the repo was initialized with Python 3.13; regenerating it with 3.12 avoids the current `lxml` build failure on 3.13.
2. Activate the environment  
   - macOS/Linux: `source venv/bin/activate`  
   - Windows (PowerShell): `venv\\Scripts\\Activate.ps1` or Command Prompt: `venv\\Scripts\\activate.bat`
3. (Optional) Upgrade pip: `python -m pip install --upgrade pip`
4. Install dependencies: `python -m pip install -r requirements.txt`

## Run
- With the virtual environment active, run: `python main.py`
- Adjust `league` and `season` in `main.py` if you want a different competition.
- To pull SofaScore data via `datafc`, run: `python datafc_fetch.py` (writes `premierleague_2022_23_stats.csv`).

## Deactivate
- Leave the virtual environment with `deactivate`

## Notes
- `soccerdata` fetches live data, so an internet connection is required when running the script.
- If you see `ModuleNotFoundError: No module named 'distutils'`, ensure pyenv is active (so you're on Python 3.12) and install setuptools: `python -m pip install --upgrade setuptools` (also now listed in `requirements.txt`).

## If `python` is not found after `pyenv local`
1. Ensure pyenv is initialized in the current shell: `export PYENV_ROOT="$HOME/.pyenv"` (adjust if you installed pyenv via Homebrew to `/opt/homebrew/var/pyenv`), then `export PATH="$PYENV_ROOT/bin:$PATH"` and `eval "$(pyenv init -)"`.
2. Verify shims: `pyenv versions` and `pyenv which python`.
3. In the repo, confirm 3.12 is active: `python --version` should show 3.12.x. If not, run `pyenv local 3.12.6` again (or `pyenv shell 3.12.6` for a single session).
