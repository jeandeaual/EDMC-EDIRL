import tkinter as tk
from ttkHyperlinkLabel import HyperlinkLabel
import logging
import l10n
import functools
import os

from typing import Optional, Dict, Any
from config import appname

from wikipedia import query_wikipedia_page

plugin_name = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f'{appname}.{plugin_name}')

# If the Logger has handlers then it was already set up by the core code, else
# it needs setting up here.
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

_ = functools.partial(l10n.Translations.translate, context=__file__)

system_label: Optional[tk.Label]
system_status: Optional[HyperlinkLabel]
body_label: Optional[tk.Label]
body_status: Optional[HyperlinkLabel]

star_system: Optional[str] = None
body: Optional[str] = None


def plugin_start3(plugin_dir: str) -> str:
    logger.debug(f'{plugin_name} plugin loaded ({plugin_dir})')
    return plugin_name


def plugin_stop() -> None:
    pass


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    update_status()


def plugin_app(parent) -> tk.Frame:
    global system_label, system_status, body_label, body_status

    frame = tk.Frame(parent)

    system_label = tk.Label(frame, text=f'{_("System")}:')
    system_label.grid(row=0, column=0, sticky=tk.W)
    system_status = HyperlinkLabel(frame, text='', url=None)
    system_status.grid(row=0, column=2, sticky=tk.E)

    body_label = tk.Label(frame, text=f'{_("Body")}:')
    body_label.grid(row=1, column=0, sticky=tk.W)
    body_status = HyperlinkLabel(frame, text='', url=None)
    body_status.grid(row=1, column=2, sticky=tk.E)

    frame.columnconfigure(2, weight=1)

    update_status()

    return frame


def journal_entry(
    cmdr: str, is_beta: bool, system: str, station: str, entry: Dict[str, Any], state: Dict[str, Any]
) -> None:
    global star_system, body

    if entry['event'] == 'FSDJump':
        # We arrived at a new system!
        if 'StarSystem' in entry:
            star_system = entry['StarSystem']
    elif entry['event'] == 'SupercruiseExit':
        if 'StarSystem' in entry:
            star_system = entry['StarSystem']
        if 'Body' in entry:
            body = entry['Body']
        else:
            body = None
    elif entry['event'] == 'Docked':
        if 'StarSystem' in entry:
            star_system = entry['StarSystem']
        if 'Body' in entry:
            body = entry['Body']
        else:
            body = None
    elif entry['event'] == 'Cargo':
        if 'StarSystem' in entry:
            star_system = entry['StarSystem']
        if 'Body' in entry:
            body = entry['Body']
        else:
            body = None

    update_status()


def update_status() -> None:
    global star_system, body, system_status, body_status

    if star_system is not None:
        url = query_wikipedia_page(star_system)
        if url is not None:
            system_status['text'] = star_system
            system_status['url'] = url
        else:
            system_status['text'] = _('No data found')
            system_status['url'] = None
    else:
        system_status['text'] = _('No data found')
        system_status['url'] = None

    if body is not None:
        url = query_wikipedia_page(body)
        if url is not None:
            body_status['text'] = body
            body_status['url'] = url
        else:
            body_status['text'] = _('No data found')
            body_status['url'] = None
    else:
        body_status['text'] = _('No data found')
        body_status['url'] = None
