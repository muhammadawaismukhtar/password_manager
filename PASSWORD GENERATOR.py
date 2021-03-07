from hashlib import sha256
import sqlite3

# *** Global Variables ***
SECRET_KEY = 's3cr3t'
ALPHABET = ('abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789!@#$%^&*()-_')


# def set_password():
#     while True:
#         curr_pass = input("Enter the current password: ")
#         if curr_pass == database_password:
#             print("Correct Password!")
#             set_new_pass = input("Now enter new password: ")
#             print("New Database password updated.")
#             return set_new_pass
#             break
#
#         else:
#             print("Please enter correct current password: ")


# *** MAIN FUNCTION ***
def main():
    create_db(None, inp_serv, inp_pass, out_hash)
    final_selection()


# *** Defining password generator Functions ***
def get_hexdigest(service, password):
    strg = service + password
    en_strg = strg.encode()
    return sha256(en_strg).hexdigest()


def make_password(plaintext, service):
    salt = get_hexdigest(SECRET_KEY, service)[:20]
    hsh = get_hexdigest(salt, plaintext)
    return ''.join((salt, hsh))


def password(plaintext, service, length=10):
    raw_hexdigest = make_password(plaintext, service)

    # Convert the hexdigest into decimal
    num = int(raw_hexdigest, 16)

    # What base will we convert `num` into?
    num_chars = len(ALPHABET)

    # Build up the new password one "digit" at a time,
    # up to a certain length
    chars = []
    while len(chars) < length:
        num, idx = divmod(num, num_chars)
        chars.append(ALPHABET[idx])

    return ''.join(chars)


# def secure():
#     count = 0
#     while True:
#         if count >= 3:
#             print("You have entered invalid password for 3 times. Program is quiting...")
#             quit(exit())
#         database_password = "qwertyuiop"
#         inp_user = input("Enter Database Password: ")
#         if inp_user != database_password:
#             print("Wrong password. Try Again: ")
#             count += 1
#             print(f"{3 - count} attempt(s) left.")
#             continue
#         else:
#             return database_password
#             break


# *** Creating DB ***


def create_db(ID, inp_serv, inp_pass, out_hash):
    conn = sqlite3.connect("test.db")
    try:
        conn.execute('''CREATE TABLE passwordmanager
               (ID INTEGER PRIMARY KEY,
               SEARCH_SERVICE TEXT NOT NULL,
               SEARCH_PASSWORD TEXT NOT NULL,
               SEARCH_HASH TEXT NOT NULL)''')
    except:
        pass


# *** Defining General Functions ***
def insert_all(inp_serv, inp_pass, out_hash):
    conn = sqlite3.connect("test.db")
    try:
        conn.execute("INSERT INTO passwordmanager (SEARCH_SERVICE, SEARCH_PASSWORD, SEARCH_HASH)  VALUES (?,?,?)",
                     [inp_serv, inp_pass, out_hash])
        conn.commit()
        conn.close()
    except:
        pass


def view_by_id(row_id):
    conn = sqlite3.connect('test.db')
    cur = conn.execute('select * from passwordmanager where ID=?', row_id)
    res = [dict(ID=row[0], SEARCH_SERVICE=row[1], SEARCH_PASSWORD=row[2], SEARCH_HASH=row[3]) for row in cur.fetchall()]
    conn.close()
    print(res)


def view_by_service(v_service):
    conn = sqlite3.connect('test.db')
    cur = conn.execute('select * from passwordmanager where SEARCH_SERVICE=?', v_service)
    res = [dict(ID=row[0], SEARCH_SERVICE=row[1], SEARCH_PASSWORD=row[2], SEARCH_HASH=row[3]) for row in cur.fetchall()]
    conn.close()
    print(res)


def view_by_password(v_password):
    conn = sqlite3.connect('test.db')
    cur = conn.execute('select * from passwordmanager where SEARCH_PASSWORD=?', v_password)
    res = [dict(ID=row[0], SEARCH_SERVICE=row[1], SEARCH_PASSWORD=row[2], SEARCH_HASH=row[3]) for row in cur.fetchall()]
    conn.close()
    print(res)


def view_all():
    conn = sqlite3.connect('test.db')
    cur = conn.execute('select * from passwordmanager')
    res = [dict(ID=row[0], SEARCH_SERVICE=row[1], SEARCH_PASSWORD=row[2], SEARCH_HASH=row[3]) for row in cur.fetchall()]
    conn.close()
    print(res)


def del_by_id(row_id):
    conn = sqlite3.connect('test.db')
    cur = conn.execute('DELETE from passwordmanager where ID=?', (row_id,))
    res = [dict(ID=row[0], SEARCH_SERVICE=row[1], SEARCH_PASSWORD=row[2], SEARCH_HASH=row[3]) for row in cur.fetchall()]
    conn.commit()
    conn.close()
    print(f"The record on row {row_id} is deleted successfully")


def del_all():
    conn = sqlite3.connect('test.db')
    cur = conn.execute('DELETE from passwordmanager;')
    res = [dict(ID=row[0], SEARCH_SERVICE=row[1], SEARCH_PASSWORD=row[2], SEARCH_HASH=row[3]) for row in cur.fetchall()]
    conn.commit()
    conn.close()
    print("All the records deleted successfully")


def update_service(updated_service, row_id, old_password):
    conn = sqlite3.connect('test.db')
    cur = conn.execute('UPDATE passwordmanager set SEARCH_SERVICE=? where ID=?', (updated_service, row_id,))
    res = [dict(ID=row[0], SEARCH_SERVICE=row[1], SEARCH_PASSWORD=row[2], SEARCH_HASH=row[3]) for row in cur.fetchall()]
    conn.commit()
    # *** Changing the HASH ***
    # updated_serv = updated_service
    # old_pass = old_password
    new_hash = password(updated_service, old_password)
    cur = conn.execute('UPDATE passwordmanager set SEARCH_HASH=? where ID=?', (new_hash, row_id,))
    conn.commit()
    conn.close()
    print(f"The service name on row {row_id} is updated with {updated_service} successfully")


def update_password(updated_password, row_id, old_service):
    conn = sqlite3.connect('test.db')
    cur = conn.execute('UPDATE passwordmanager set SEARCH_PASSWORD=? where ID=?', (updated_password, row_id,))
    res = [dict(ID=row[0], SEARCH_SERVICE=row[1], SEARCH_PASSWORD=row[2], SEARCH_HASH=row[3]) for row in cur.fetchall()]
    conn.commit()
    # *** Changing the HASH ***
    # updated_pass = updated_password
    # old_serv = old_service
    new_hash = password(updated_password, old_service)
    cur = conn.execute('UPDATE passwordmanager set SEARCH_HASH=? where ID=?', (new_hash, row_id,))
    conn.commit()
    conn.close()
    print(f"The password on row {row_id} is updated with {updated_password} successfully")


def final_selection():
    while True:
        print("\nPress 'A' to see all the VIEW options.\n"
              "Press 'B' to see all the UPDATE options.\n"
              "Press 'C' to see all the DELETE options.\n"
              "Press 'S' to update the Database password.\n"
              "Press 'X' to exit.")
        selection = input("")
        # *** VIEW OPTIONS ***
        if selection == "A":
            print("\nPress '1' to VIEW the entry using ID.\n"
                  "Press '2' to VIEW all the entries in Database.\n"
                  "Press '3' to VIEW by using service.\n"
                  "Press '4' to VIEW by using password.\n")
            sub_selection = input("")
            if sub_selection == "1":
                view_by_id(row_id=input("Enter the row number: "))
            elif sub_selection == "2":
                view_all()
            elif sub_selection == "3":
                v_service = input("To search, enter Service name: ")
                view_by_service(v_service)
            elif sub_selection == "4":
                v_password = input("To search, enter Password: ")
                view_by_password(v_password)
            else:
                print("\nYou have entered wrong option.")
                continue
        # *** UPDATE OPTIONS ***
        elif selection == "B":
            print("\nPress '1' to UPDATE the service of an entry.\n"
                  "Press '2' to UPDATE the password of an entry.\n")
            sub_selection = input("")
            if sub_selection == "1":
                update_service(row_id=input("Enter the row number: "),
                               updated_service=input("Enter the service name: "), old_password=inp_pass)
            elif sub_selection == "2":
                update_password(row_id=input("Enter the row number: "), updated_password=input("Enter the password: "),
                                old_service=inp_serv)
            else:
                print("\nYou have entered wrong option.")
                continue
        # *** DELETE OPTIONS ***
        elif selection == "C":
            print("\nPress '1' to DELETE the entry by row number.\n"
                  "Press '2' to DELETE all the entries in the database.\n")
            sub_selection = input("")
            if sub_selection == "1":
                del_by_id(str(input("Enter the row number to be deleted...")))
            elif sub_selection == "2":
                print("Are you sure you want to permanently delete all the entries in Database? "
                      "Press 'Y' for Yes and 'N' for No: ")
                del_command = input("")
                if del_command == "Y":
                    del_all()
                    print("All the entries are deleted.")
                elif del_command == "N":
                    print("The entries are not deleted.")
                else:
                    print("You have enter neither option.")
                    continue
            else:
                print("\nYou have entered wrong option.")
                continue
        # *** EXIT ***
        elif selection == "X":
            break
        # *** DEFAULT Behaviour ***
        else:
            print("\nEnter correct option...")
            pass


# *** User Input ***
inp_serv = None
inp_pass = None
out_hash = None
search = None
# *** Continuous prompt ***
while search != '!':
    search = input("NOTE: Capital Letters must be used for selection of Options.\n"
                   "Press the Enter key to continue the program OR '!' to exit the program: ")
    if search == "!":
        print("\nThanks for using Password Manager.")
        break
    else:
        inp_serv = input("Enter service name: ")
        inp_pass = input("Enter password name: ")
        out_hash = password(inp_pass, inp_serv)
        insert_all(inp_serv, inp_pass, out_hash)

# *** RUNNING THE PROGRAM ***
if __name__ == '__main__':
    main()
