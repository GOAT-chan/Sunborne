# Sunborne
Yet another Discord bot for Sunrise-powered servers

## Deploying
For production, it is recommended to containerize Sunborne using Docker for the sake of convenience and stability. However, for development, one can manually run the bot by
- Installing Python 3 either via your distro's package manager, or via the official installers
- Cloning this repository
- Installing all dependencies by running `pip install -r requirements.txt`
- Set required environment variables appropriately (see `.env.example`)
- Copy `config.example.json` to `config.json` then edit the values appropriately
- Run `python3 sunborne.py`