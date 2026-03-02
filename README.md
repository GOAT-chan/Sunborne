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

## Acknowledgments
- Beatmap status icons are from [Lucide](https://lucide.dev/)
- Grades and judgements images are from the [Hyperdimension Neptunia Re;birth 1 skin](https://skins.osuck.net/skins/4911)
- Game mode and beatmap statistic icons are from the [official osu! assets repository](https://github.com/ppy/osu-resources)

## License
Sunborne is licensed under version 2.1 of the GNU Lesser General Public License. You may read it [here](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html).

Please do note that above license only applies to Sunborne's **code** as well as all other **original** assets (will be explicitly stated). Assets used in the above [Acknowledgments](#acknowledgments) section are used in a non-commercial manner and may be licensed under a different license.