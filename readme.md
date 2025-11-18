# fanl_yp Antivir

A Python tool to clean your game files thats are infected by undeletable or corrupted blocks, allowing recovery without affecting any level data.

## Overview

fanl_yp-Block-Remover removes problematic blocks from game files while leaving level data untouched. It offers two modes to control which blocks are removed:

    Mode 1: Select blocks you want to remove.

    Mode 2: Select blocks you want to keep (all other blocks will be removed).

## Requirements
Python 3.12 or newer

## Usage
Make sure that you have a backup of your gamefiles

1. Open a terminal or command prompt.
2. Navigate to the directory containing the script.
3. Run: `python3 deinfectGameFile.py`
4. Follow the steps
5. rename the output file `[GameID]_fixed` to `[GameID]`
6. zip it and impoort it back
