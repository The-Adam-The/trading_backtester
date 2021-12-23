


#script to rename the tables in sp500daata.db
for db_name in connection.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name').fetchall():
    if db_name[0] == "sp500tickers":
        print("Ticker Table Removed")
        continue
    amended_db_name = db_name[0].replace("TradeData", "")
    if db_name[0] == amended_db_name:
        print(f"Table {amended_db_name}, already changed")
        continue
    print(f"Before - amendment")
    if "-" in amended_db_name:
        amended_db_name = amended_db_name.replace("-", "")
    print(f"After - amendment: {amended_db_name}")

    connection.execute("ALTER TABLE " + db_name[0] + " RENAME TO " + amended_db_name)
