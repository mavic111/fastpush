# fastpush

## Push Notifications backend using FastAPI and PostgreSQL

FastPush for faster push notifications. 🚀

Supports Push API for Progressive Web App

## Features

- Using Push API for push notifications
- Using BackgroundTasks to send the notifications
- Revalidate notifications page in the frontend after broadcast
- Store subscription and message in PostgreSQL.

## Stacks

- FastAPI
- Supabase PostgreSQL
- Vercel

## Install dependencies

`pip install -r requirements.txt`

## Run the server

production

`uvicorn app.main:app`

development

`uvicorn app.main:app --reload`

## Deployment

Ready to deploy in Vercel

## Bugs

- Lifespan events are not executed when deployed in Vercel.

_Solution_: Run it first in the local to create the database and table.
