import sqlite3

class MyDatabase:
    def __enter__(self):
        self.conn = sqlite3.connect('database.db')
        print("opened database successfully")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        print("connection is closed")


    def create(self):
        create_table = '''CREATE TABLE COMPANY
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    SYMBOL TEXT NOT NULL,
                    YEAR INTEGER NOT NULL,
                    NET_INCOME DECIMAL(15, 2),
                    TOTAL_ASSET DECIMAL(15,2),
                    UNIQUE (COMPANY_NAME, YEAR));'''

        self.conn.execute(create_table)

        print("table is created successfully")

    def read(self):
        cursor = self.conn.execute("SELECT * FROM COMPANY")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        cursor.close()

    def insert(self, symbol, year, net_income, total_asset):
        query = f"INSERT INTO COMPANY (SYMBOL, COMPANY_NAME, YEAR, NET_INCOME, TOTAL_ASSET) VALUES (?, ?, ?, ?, ?);"
        data_to_insert = (symbol, year, net_income, total_asset)

        cursor = self.conn.cursor()
        cursor.execute(query, data_to_insert)
        self.conn.commit()
        cursor.close()


if __name__ == "__main__":
    with MyDatabase() as db:
        print("1. Create Table.")
        print("2. Read From Table.")
        print("3. Insert Data in Table")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            db.create()
        elif choice == 2:
            db.read()
        elif choice == 3:
            while True:
                symbol = input("Enter Symbol: ")
                year = int(input("Enter Year: "))
                net_income = float(input("Enter Net Income: "))
                total_asset = float(input("Enter Total Asset: "))
                db.insert(symbol, year, net_income, total_asset)
                if input("exit::") == "exit":
                    break
        else:
            print("try again.")