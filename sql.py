import psycopg2
from configparser import ConfigParser
from tabulate import tabulate


# Connect to the School database
conn = psycopg2.connect(
    dbname="telegrambot",
    user="postgres",
    password="C0mpn3t!",
    host="localhost"
)

cur = conn.cursor()

#Absensi Karyawan
##/checkin untuk mencatat kehadiran.
def checkin_sql(user: int):
    cur = conn.cursor()
    try:
        # Cek apakah user sudah melakukan check-in
        
        cur.execute("SELECT * FROM attendance WHERE user_id = %s AND date = CURRENT_DATE;", (user,))
        result = cur.fetchone()
        
        if result:  # Jika ada hasil, berarti user sudah absen
            jam_absen = result[2]
            return f"Anda tidak boleh melakukan absensi lagi karena Anda sudah absen pada pukul {jam_absen}"
        else:
            # Jika belum absen, tambahkan data ke tabel attendance
            cur.execute("INSERT INTO attendance (user_id) VALUES (%s)", (user,))
            conn.commit()

            # Ambil waktu check-in yang baru saja dimasukkan
            cur.execute("SELECT checkin_time FROM attendance WHERE user_id = %s ORDER BY id DESC LIMIT 1;", (user,))
            jam_absen = cur.fetchone()[0]
            return f"Anda sudah berhasil absen pada pukul {jam_absen}"
    except Exception as e:
        return f"Terjadi error: di checkin {e}"
    finally:
        cur.close()

def checkout_sql(user: int)->int:
    cur = conn.cursor()
    try:
        # Ambil checkout_time untuk user hari ini
        cur.execute(
            "SELECT checkout_time FROM attendance WHERE user_id = %s AND date = CURRENT_DATE ORDER BY id DESC LIMIT 1;",
            (user,)
        )
        result = cur.fetchone()

        if result is None:
            return "Anda harus check-in terlebih dahulu."
        
        checkout_time = result[0]
        if checkout_time is None:  # Belum absen keluar
            # Update checkout_time untuk absensi hari ini
            cur.execute(
                "UPDATE attendance SET checkout_time = CURRENT_TIMESTAMP WHERE user_id = %s AND date = CURRENT_DATE;",
                (user,)
            )
            conn.commit()
            
            # Ambil waktu checkout terbaru
            cur.execute(
                "SELECT checkout_time FROM attendance WHERE user_id = %s AND date = CURRENT_DATE ORDER BY id DESC LIMIT 1;",
                (user,)
            )
            jam_absen = cur.fetchone()[0]
            return f"Anda sudah berhasil absen keluar pada pukul {jam_absen}."
        else:
            return f"Anda sudah melakukan absensi keluar pada pukul {checkout_time}."
    except Exception as e:
        return f"Terjadi error: {e}"
    finally:
        cur.close()

def list_sql():
    cur = conn.cursor()
    try:
        sql="SELECT * FROM attendance"
        # Ambil semua data absensi untuk user tertentu
        cur.execute(sql)
        mydata = cur.fetchall()
        
        cur.execute(sql) 
        head = [desc[0] for desc in cur.description] 
        markdown_table = "```\n" + tabulate(mydata, headers=head, tablefmt="grid") + "\n```"
        return markdown_table
        
    except Exception as e:
        return f"Terjadi error: list task {e}"
    finally:
        cur.close()

def add_task_sql(text):
    cur = conn.cursor()
    try:
        # Ambil semua data absensi untuk user tertentu
        cur.execute(
            'INSERT INTO tasks(description) VALUES(%s) RETURNING id', (text,) )
        hundred = cur.fetchone()[0]
        conn.commit()
        # hundred = cur.fetchone()
        return f'Tugas anda sudah dibuat dengan list id {hundred}'
        
    except Exception as e:
        return f"Terjadi error:  {e}"
    finally:
        cur.close()

def list_tasks_sql():
    cur = conn.cursor()
    try:
        # Ambil semua data dari tabel tasks
        sql = "SELECT * FROM tasks"
        cur.execute(sql)
        mydata = cur.fetchall()
        head = [desc[0] for desc in cur.description]
        
        # Buat tabel dalam format Markdown
        markdown_table = "```\n" + tabulate(mydata, headers=head, tablefmt="grid") + "\n```"
        return markdown_table
    except Exception as e:
        return f"Terjadi error: list task sql {e}"
    finally:
        cur.close()

def pending_tasks_sql():
    cur = conn.cursor()
    try:
        # Ambil semua data absensi untuk user tertentu
        sql = "SELECT * FROM tasks WHERE status = false"
        cur.execute(sql)
        mydata = cur.fetchall()
        if mydata:
            cur.execute(sql) 
            head = [desc[0] for desc in cur.description] 
            markdown_table = "```\n" + tabulate(mydata, headers=head, tablefmt="grid") + "\n```"
            return markdown_table
        else:
            return('Silahkan istirahat sudah tidak ada pending')        
    except Exception as e:
        return f"Terjadi error: {e}"
    finally:
        cur.close()

def show_one_task_sql(id : int):
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM tasks WHERE id = %s',(id,))
        mydata = cur.fetchmany()
        if mydata:
            cur.execute('SELECT * FROM tasks WHERE id = %s',(id,)) 
            head = [desc[0] for desc in cur.description] 
            markdown_table = "```\n" + tabulate(mydata, headers=head, tablefmt="grid") + "\n```"
            return markdown_table
        else:
            return('Pekerjaan yang anda cari tidak ada')        
    except Exception as e:
        return f"Terjadi error: di show one task {e}"
    finally:
        cur.close()

def done_tasks_sql(id : int):
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM tasks WHERE id = %s',(id,))
        data = cur.fetchone()
        if data:
            cur.execute('UPDATE tasks SET status = true where id = %s', (id,))
            conn.commit()
            cur.execute('SELECT * FROM tasks WHERE id = %s',(id,))
            mydata = cur.fetchmany()
            cur.execute('SELECT * FROM tasks WHERE id = %s',(id,)) 
            head = [desc[0] for desc in cur.description] 
            markdown_table = "```\n" + tabulate(mydata, headers=head, tablefmt="grid") + "\n```"
            return markdown_table 
 
        else:
            return 'data yang dicari tidak ada'     
    except Exception as e:
        return f"Terjadi error: {e}"
    finally:
        cur.close()

# print(done_tasks_sql(2))

# print(checkin_sql(4))