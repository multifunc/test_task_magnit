from pathlib import Path
from configparser import ConfigParser
from typing import Dict

BASE_DIR: Path = Path(__file__).parent.parent

TEMPLATE_DIR: Path = BASE_DIR / 'templates'

CONFIG: Path = BASE_DIR / 'config.ini'

if not CONFIG.exists():
    raise FileNotFoundError(f"Файл конфигурации {str(CONFIG)} не найден!")

parser = ConfigParser()
parser.read(CONFIG, encoding='utf-8')

DATABASE_SETTINGS: Dict[str, str] = dict(parser.items("database"))

DATABASE: Path = BASE_DIR / DATABASE_SETTINGS['db']
DATABASE_INIT_SCRIPT: Path = BASE_DIR / DATABASE_SETTINGS['create_db_script']