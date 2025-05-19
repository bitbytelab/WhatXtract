// Common helper functions used by both extract and restore
// Universal async runner wrapper for Selenium execute_async_script
function runAsync(asyncFunc, ...args) {
    const callback = args[args.length - 1];
    asyncFunc(...args.slice(0, -1)).then(callback).catch(err => {
        console.error("Async function failed:", err);
        callback(null);
    });
}

function getResultFromRequest(request) {
    return new Promise((resolve) => {
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => resolve(null);
    });
}

async function getDB(name, upgradeStoreNames = []) {
    const request = window.indexedDB.open(name);

    request.onupgradeneeded = () => {
        const db = request.result;
        for (const storeName of upgradeStoreNames) {
            if (!db.objectStoreNames.contains(storeName)) {
                db.createObjectStore(storeName, {
                    keyPath: 'id',
                    autoIncrement: true
                });
            }
        }
    };

    return await getResultFromRequest(request);
}

async function exportDatabases(dbNames) {
    const result = {};

    for (const dbName of dbNames) {
        const db = await getDB(dbName);
        if (!db) continue;

        const tx = db.transaction(db.objectStoreNames, 'readonly');
        const storeData = {};

        for (const storeName of db.objectStoreNames) {
            const store = tx.objectStore(storeName);
            const data = await getResultFromRequest(store.getAll());
            storeData[storeName] = data ?? []; // fallback to [] if null
        }

        result[dbName] = storeData;
        db.close();
    }

    return result;
}

async function restoreDatabases(data) {
    for (const [dbName, stores] of Object.entries(data)) {
        const upgradeStoreNames = Object.keys(stores);
        const db = await getDB(dbName, upgradeStoreNames);
        if (!db) continue;

        const tx = db.transaction(upgradeStoreNames, 'readwrite');

        for (const [storeName, records] of Object.entries(stores)) {
            const store = tx.objectStore(storeName);
            for (const record of records) {
                try {
                    store.put(record);
                } catch (e) {
                    console.warn(`Failed to insert record into store "${storeName}":`, e);
                }
            }
        }

        await tx.complete;
        db.close();
    }
}

// Uncomment for Selenium async execution:
// runAsync(restoreDatabases, arguments[0]);


// driver.execute_async_script(INDEXEDDB_SCRIPT_BASE + """
// var callback = arguments[arguments.length - 1];
// var SESSION_DATA = arguments[0];
// restoreDatabases(SESSION_DATA).then(callback);
// """, session_data)

// var SESSION_DATA = arguments[0];
// return await restoreDatabases(SESSION_DATA);


/********************** old extract script **********************/
async function readAllKeyValuePairs(dbName) {
    var db = await getDB(dbName);
    var objectStore = db.transaction("user").objectStore("user");
    var request = objectStore.getAll();
    return await getResultFromRequest(request);
}

// uncomment before executing from python
// var dbName = arguments[0];
// return await readAllKeyValuePairs(dbName);


/********************** old inject script **********************/
async function injectSession(SESSION_STRING) {
    var session = eval(SESSION_STRING);
    var db = await getDB();
    var objectStore = db.transaction("user", "readwrite").objectStore("user");
    for(var keyValue of session) {
        var request = objectStore.put(keyValue);
        await getResultFromRequest(request);
    }
}

// we can pass "arguments" from python to javascript
// uncomment before executing from python
// var SESSION_STRING = arguments[0];
// await injectSession(SESSION_STRING);


ASYNC_WRAPPER = """
function runAsync(asyncFunc) {
    console.log("Arguments received in runAsync:", arguments);
    const callback = arguments[arguments.length - 1]; // last is Selenium's callback
    const args = Array.prototype.slice.call(arguments, 1, arguments.length - 1); // middle args

    if (typeof callback !== "function") {
        console.error("Selenium callback missing or not a function.");
        return;
    }

    asyncFunc(...args)
        .then(callback)
        .catch(err => {
            console.error("Async function failed:", err);
            callback(null); // avoid timeout
        });
}
"""

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
(async () => {
    const snapshot = {
        indexedDB: {}
    };

    const allowedDBs = ["model-storage"];

    var dbName =

    const dbs = await indexedDB.databases();

    for (const dbInfo of dbs) {
        if (!allowedDBs.includes(dbInfo.name)) continue;
        const db = await openDB(dbInfo.name);
        if (!db || db.objectStoreNames.length === 0) {
            console.warn("Skipping DB:", dbInfo.name, "(no object stores)");
            if (db) db.close();
            continue;
        }

        const tx = db.transaction(db.objectStoreNames, 'readonly');
        const dbDump = {};

        for (const storeName of db.objectStoreNames) {
            const store = tx.objectStore(storeName);
            dbDump[storeName] = await getResultFromRequest(store.getAll());
        }

        snapshot.indexedDB[dbInfo.name] = dbDump

        db.close();
    }

    callback(snapshot);
})().catch(e => {
    console.error("Snapshot failed", e);
    callback(null);
});
"""

RESTORE_SNAPSHOT_SCRIPT = INDEXEDDB_SNAPSHOT_HELPERS + """
const callback = arguments[arguments.length - 1];

(async () => {
  try {
    const sessionData = arguments[0];
    const delay = ms => new Promise(res => setTimeout(res, ms));

    console.log("Starting restore of session snapshot", sessionData);
    // Step 1: Clear localStorage and sessionStorage
    localStorage.clear();
    sessionStorage.clear();

    await delay(200); // small wait

    // Step 2: Restore localStorage
    if (sessionData.localStorage) {
      for (const [key, value] of Object.entries(sessionData.localStorage)) {
        localStorage.setItem(key, value);
      }
    }

    // Step 3: Restore sessionStorage
    if (sessionData.sessionStorage) {
      for (const [key, value] of Object.entries(sessionData.sessionStorage)) {
        sessionStorage.setItem(key, value);
      }
    }

    await delay(200); // small wait


    // Step 6: Restore IndexedDB
    if (sessionData.indexedDB) {
      const allowedDBs = ["wawc"];
      for (const [dbName, dbData] of Object.entries(sessionData.indexedDB)) {
        if (!allowedDBs.includes(dbName)) continue;
        await delay(200); // small wait

        const { version, schemas, stores } = dbData;
        console.log("Restoring DB:", dbName, "v" + version);

        const db = await openDB(dbName);

      }
    }

    callback({ status: "success" });
  } catch (err) {
    console.error("Restore session failed:", err);
    callback({ status: "error", error: err.toString() });
  }
})();

"""



SETUP_INDEXEDDB = """

function getResultFromRequest(request) {
    return new Promise((resolve, reject) => {
        request.onsuccess = function(event) {
            resolve(request.result);
        };
    })
}

async function getDB() {
    var request = window.indexedDB.open("wawc");
    return await getResultFromRequest(request);
}
"""

EXTRACT_SESSION = SETUP_INDEXEDDB + """

async function readAllKeyValuePairs() {
    var db = await getDB();
    var objectStore = db.transaction("user").objectStore("user");
    var request = objectStore.getAll();
    return await getResultFromRequest(request);
}

const snapshot = {
    localStorage: { ...localStorage },
    sessionStorage: { ...sessionStorage },
    indexedDB: {
        wawc: {
            user: await readAllKeyValuePairs()
        }
    }
};

return JSON.stringify(snapshot);
"""


ASYNC_WRAPPER = """
function runAsync(asyncFunc) {
    console.log("Arguments received in runAsync:", arguments);
    const callback = arguments[arguments.length - 1]; // last is Selenium's callback
    const args = Array.prototype.slice.call(arguments, 1, arguments.length - 1); // middle args

    if (typeof callback !== "function") {
        console.error("Selenium callback missing or not a function.");
        return;
    }

    asyncFunc(...args)
        .then(callback)
        .catch(err => {
            console.error("Async function failed:", err);
            callback(null); // avoid timeout
        });
}
"""
