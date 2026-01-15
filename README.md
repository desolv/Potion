# Potion

A Discord bot built with discord.py featuring moderation capabilities and PostgreSQL database integration.

## Features

- Moderation commands
- PostgreSQL database support with SQLAlchemy
- Async/await architecture
- Automatic extension loading

## Requirements

- Python 3.8+
- PostgreSQL database

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Potion
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```env
DISCORD_TOKEN=your_discord_bot_token
POSTGRES=postgresql://user:password@localhost/database
```

## Usage

Run the bot:
```bash
python potion.py
```

## Project Structure

```
Potion/
├── backend/          # Database backend and utilities
├── commands/         # Bot command modules
├── core/             # Core bot functionality
├── master/           # Master control modules
├── models/           # Database models
├── potion.py         # Main entry point
├── requirements.txt  # Python dependencies
└── .env              # Environment variables (not in repo)
```

## Configuration

The bot uses a `?` prefix for commands by default. This can be modified in `potion.py`.
