import sqlite3, os, csv


def import_tsv(file_path, table_name, cursor):
        with open(file_path, "r") as file:
                reader = csv.reader(file, delimiter="\t")
                columns = next(reader) # Skip the header row

                quoted_columns = [f'"{col}"' for col in columns]
                print(quoted_columns)

                query = f"INSERT INTO {table_name} ({', '.join(quoted_columns)}) VALUES ({', '.join(['?'] * len(columns))})"
                for data in reader:
                    cursor.execute(query, data)

def create_database():
    database_exists = os.path.exists("database.db")
    # connect to the database. If the database does not exist the command then creates the database.
    conn = sqlite3.connect("database.db")
    # if the database did not exist, create the tables
    if not database_exists:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE delly_cnv (
                        chrom TEXT,
                        start INTEGER,
                        end INTEGER, 
                        cn0 INTEGER, 
                        cn1 INTEGER, 
                        cn2 INTEGER, 
                        cn3 INTEGER, 
                        cn4 INTEGER, 
                        cn5 INTEGER, 
                        cn6 INTEGER, 
                        cn7plus INTEGER
                        )''')

        cursor.execute('''CREATE TABLE variants (
                        chrom TEXT, 
                        start INTEGER, 
                        end INTEGER, 
                        type TEXT, 
                        ac INTEGER, 
                        ah TEXT, 
                        classifier TEXT
                        )''')

        # import data from TSV files
        import_tsv("tsv_files/manta.tsv","variants",cursor)
        import_tsv("tsv_files/delly.tsv","variants",cursor)
        import_tsv("tsv_files/smoove.tsv","variants",cursor)
        import_tsv("tsv_files/gridss.tsv","variants",cursor)
        import_tsv("tsv_files/delly_cnv.tsv","delly_cnv",cursor)

        # Create indexes
        cursor.execute('CREATE INDEX dcnv_end ON delly_cnv(chrom, end)')
        cursor.execute('CREATE INDEX dcnv_start ON delly_cnv(chrom, start)')
        cursor.execute('CREATE INDEX classifier_ind ON variants(classifier)')
        cursor.execute('CREATE INDEX start_class_ind ON variants(chrom, start, classifier)')
        cursor.execute('CREATE INDEX end_class_ind ON variants(chrom, end, classifier)')
        cursor.execute('CREATE INDEX start_end_class_ind ON variants(chrom, start, end, classifier)')

        conn.commit()
        cursor.close()
        conn.close()                        
