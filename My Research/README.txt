================================================================================
ETL Control Panel - User Manual
================================================================================
Standalone Windows application (.exe)
Version: 1.0

--------------------------------------------------------------------------------
1. OVERVIEW
--------------------------------------------------------------------------------
The ETL Control Panel is a desktop tool that automates loading of data files
(CSV / Excel) into a staging area of a relational database and logs every run.

It is driven by a "control table" that defines, per module:
  - where to look for files (source directory + file name pattern)
  - what type of files to expect (csv / xlsx / both)
  - the staging table prefix to use
  - whether the module is active

After processing, each file is archived and a record is written to the
file log and module run log tables.

The application works with ANY relational database (SQLite, PostgreSQL,
SQL Server, MySQL, ...) through a SQLAlchemy connection string.

--------------------------------------------------------------------------------
2. FILES INCLUDED
--------------------------------------------------------------------------------
  ETLControlPanel.exe   - The standalone application (double-click to run).
  config.py             - Connection + path settings (only needed if you
                          rebuild the .exe; see section 6).
  app_gui.py            - Source of the GUI (only needed to rebuild).
  etl_engine.py         - Processing logic (only needed to rebuild).
  models.py             - Database schema / connection (only needed to rebuild).
  db_init.py            - Creates the control tables on a new database.
  build.py              - PyInstaller build script (only needed to rebuild).

NOTE: To simply USE the application you only need ETLControlPanel.exe.
      All other files are for rebuilding or customizing it.

--------------------------------------------------------------------------------
3. FIRST RUN
--------------------------------------------------------------------------------
  1. Double-click ETLControlPanel.exe.
  2. The main window shows a "Select Module to Process" dropdown.
  3. The dropdown is filled from the etl_control table (active modules only).
  4. If no modules appear, configure the database / control table first
     (sections 4 and 5).

By default the application points to the database configured at build time
(see config.DB_URL). On first use the control tables are created
automatically if they do not exist.

--------------------------------------------------------------------------------
4. CONFIGURING THE DATABASE (for a different RDBMS)
--------------------------------------------------------------------------------
The connection is defined by a SQLAlchemy URL. Examples:

  SQLite:
    sqlite:///C:/path/to/migration.db

  PostgreSQL:
    postgresql+psycopg2://user:password@host:5432/dbname

  SQL Server (ODBC):
    mssql+pyodbc://user:password@server/dbname?driver=ODBC+Driver+17+for+SQL+Server

  MySQL:
    mysql+pymysql://user:password@host:3306/dbname

To change the database, edit config.DB_URL in config.py and rebuild the .exe
(see section 6), OR ask the packager to rebuild with the new connection.

For databases other than SQLite you must also have the matching driver
installed in the build environment (e.g. psycopg2-binary, pyodbc, pymysql).

--------------------------------------------------------------------------------
5. THE CONTROL TABLE (etl_control)
--------------------------------------------------------------------------------
Each row defines one module. Columns:

  module_name          Unique name of the module (e.g. SALES).
  source_directory     Folder where input files are read from.
  file_pattern         Glob pattern, e.g. sales_*.csv
  file_type            One of: csv, xlsx, both
  staging_table_prefix Prefix for the staging table, e.g. stg_sales
  active               1 = enabled, 0 = hidden from the dropdown
  description          Free text shown in the UI.
  created_at / updated_at  Managed automatically.

If the table is empty, use db_init.py to seed a sample "SALES" module:
    python db_init.py

--------------------------------------------------------------------------------
6. USING THE APPLICATION
--------------------------------------------------------------------------------
  a) Select a module from the dropdown.
  b) Its configuration is displayed in the "Configuration" box.
  c) Click "Run Processing":
       - The app finds matching files in the source directory.
       - Each file is loaded into a staging table
         (<prefix>_<filename with dots replaced by underscores>).
       - The file is moved to the archive folder.
       - A record is added to etl_file_log and etl_module_run_log.
  d) The "Recent File Logs" and "Recent Module Runs" tables refresh
     automatically after the run.
  e) Click "Refresh" to reload the module list and logs at any time.

Processing runs in the background; the status bar at the top shows progress
and the final summary (processed / success / failed / records).

--------------------------------------------------------------------------------
7. LOGGING & ARCHIVING
--------------------------------------------------------------------------------
  - Processed files are moved to: <ARCHIVE_ROOT>\<module_name>\
  - Detailed logs are written to logs\etl.log next to the application.
  - The etl_file_log table records each file's status (SUCCESS / FAILED /
    SKIPPED) and any error message.
  - The etl_module_run_log table records per-run totals.

--------------------------------------------------------------------------------
8. REBUILDING THE EXE (advanced)
--------------------------------------------------------------------------------
Requirements: Python 3.11, PyInstaller, SQLAlchemy, pandas, openpyxl, and
the optional DB driver(s). UPX is bundled under build_tools\.

    pip install pyinstaller sqlalchemy pandas openpyxl
    python build.py

Output: dist\ETLControlPanel.exe

The build uses --onefile --windowed with UPX compression and excludes unused
large libraries to keep the executable as small as possible.

--------------------------------------------------------------------------------
9. TROUBLESHOOTING
--------------------------------------------------------------------------------
  - Empty module list: check the database connection and that etl_control
    has at least one row with active = 1.
  - "No active configuration" error: the selected module is inactive or
    missing in etl_control.
  - Database/driver errors: ensure the correct SQLAlchemy driver for your
    RDBMS is installed in the environment used to build the .exe.
  - Files not found: verify source_directory and file_pattern in the module.
  - Check logs\etl.log for full error details.

================================================================================
End of manual
================================================================================
