#!/bin/bash

alembic upgrade head

python main.py --bind=0.0.0.0:8000