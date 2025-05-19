"""
whatxtract: WhatsApp data extraction and automation toolkit.
 description="WhatsApp Contacts Extractor and Number Checker via WhatsApp Web"
 A WhatsApp data extraction and automation toolkit

Author: Hasan Rasel
Email: rrss.mahmud@gmail.com
License: MIT
Version: 0.1.0
"""

__title__       = "whatxtract"
__package__     = "whatxtract"
__description__ = "A WhatsApp data extraction and automation toolkit"
__version__     = "0.1.0"
__author__      = "Hasan Rasel"
__email__       = "rrss.mahmud@gmail.com"
__license__     = "MIT"
__url__         = "https://github.com/rsmahmud/whatxtract"
__copyright__   = "2025 Hasan Rasel"


import logging
from pathlib import Path

try:
    from selenium.webdriver.common.by import By
except ImportError:
    import sys
    import subprocess
    print('[ * ] Installing selenium...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])
    from selenium.webdriver.common.by import By


DEFAULT_WAIT    = 30

LOG_LEVEL       = logging.DEBUG

LOG_DIR         = Path.cwd() / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE        = LOG_DIR / __package__ + '.log'
LOG_FORMAT      = '[%(asctime)s] %(levelname)s - %(message)s'

PROFILE_DIR     = Path.cwd() / 'WAProfiles'
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR      = Path.cwd() / 'output'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
WAMS_DB_PATH    = OUTPUT_DIR / 'wams_db.json'


# Selector for Selenium
LOGIN_QR_CODE                   = (By.CSS_SELECTOR, 'div[data-ref]')
LOG_INTO_WA_WEB__TEXT           = (By.XPATH, '//div[contains(text(), "Log into WhatsApp Web")]')
MAIN_NAV_BAR                    = (By.CSS_SELECTOR, '[data-js-navbar="true"]')
MAIN_SEARCH_BAR__SEARCH_BOX     = (By.CSS_SELECTOR, 'div[contenteditable="true"][role="textbox"]')
MAIN_SEARCH_BAR__SEARCH_ICON    = (By.CSS_SELECTOR, '#side span[data-icon="search"]')
LOGIN_QR_CANVAS__SCAN_ME        = (By.XPATH, '//canvas[@aria-label="Scan me!"]')


INDEXEDDB_SNAPSHOT_HELPERS = """
function getResultFromRequest(req) {
    return new Promise((resolve, reject) => {
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
    });
}

function openDB(name) {
    return new Promise((resolve) => {
        const req = indexedDB.open(name);
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => resolve(null);
    });
}
"""

EXPORT_SNAPSHOT_SCRIPT = INDEXEDDB_SNAPSHOT_HELPERS + """
const callback = arguments[arguments.length - 1];
const delay = ms => new Promise(res => setTimeout(res, ms));
(async () => {
    var dbName = arguments[0];
    await delay(200);
    
    const db = await openDB(dbName);
    if (!db || db.objectStoreNames.length === 0) {
        console.warn("Skipping DB:", dbName, "(no object stores)");
        if (db) db.close();
    }
    await delay(200);
    
    const tx = db.transaction(db.objectStoreNames, 'readonly');
    const dbDump = {};

    for (const storeName of db.objectStoreNames) {
        const store = tx.objectStore(storeName);
        dbDump[storeName] = await getResultFromRequest(store.getAll());
    }
    
    db.close();
    await delay(200);

    callback(dbDump);
})().catch(e => {
    console.error("Snapshot failed", e);
    callback(null);
});
"""
