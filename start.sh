#!/bin/bash
python3 -m bot
gunicorn app:app
