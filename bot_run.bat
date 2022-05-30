@echo off

call %~dp0telegram_bot\venv\Scripts\activate

cd %~dp0telegram_bot

set TOKEN=5216993274:AAFHlga7nEht-8GPqaipWr_hJ8VI61ESdSI

python bot.py

pause