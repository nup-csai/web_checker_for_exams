CREATE TABLE IF NOT EXISTS Repositories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repository_link VARCHAR(64),
    readme TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS Routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route VARCHAR(64),
    content TEXT,
    check_content_script TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS RoutesChecking (
    repository_id INTEGER,
    route_id INTEGER,
    status VARCHAR(20),
    FOREIGN KEY (repository_id) REFERENCES Repositories (id),
    FOREIGN KEY (route_id) REFERENCES Routes (id)
);

CREATE TABLE IF NOT EXISTS Files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE IF NOT EXISTS FileChecking (
    repository_id INTEGER,
    file_id INTEGER,
    status VARCHAR(20),
    FOREIGN KEY (repository_id) REFERENCES Repositories (id),
    FOREIGN KEY (file_id) REFERENCES Files (id)
);
