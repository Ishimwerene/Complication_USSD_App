import mysql.connector
from datetime import datetime
import random
import re  # Import regular expressions for phone number validation
# Connect to the database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='cpmsphp'
)
conn = connection.cursor()

#Main menu for our application
def main_menu():
    while True:
        ussd_code = input("Enter ussd code: ")
        if ussd_code == 'c':
            print("Welcome to the Complaint Management System")
            print("1. Kinyarwanda")
            print("2. English")
            language_choose=input("")
            if language_choose=='2':
             while True:
                print("\nChoose Service ")
                print("0. Make Comlication")
                print("00. Make Appeal")
                print("000. Create your account")
                print("0000. Exit")

                user_choose = input("")
                if user_choose == '0':
                    login_user()
                elif user_choose == '00':
                    userlogin_appeal()
                elif user_choose == '000':
                    register_user()
                elif user_choose== '0000':
                    quit()    
                else:
                    print("Invalid Option. Try Again!!")

            elif language_choose=='1':
                menu_kiny()
            else:
                print("Invalid Choose. Try Again!!")    
        else:
            print("Invalid USSD Code!!")


#Fuction that call menu for kinyarwanda language change
def menu_kiny():

     while True:
        print("\nHitamo serivise ushaka ")
        print("0. gutanga Ikirego")
        print("00. Kujurira Umwanzuro")
        print("000. Kwiyandikisha bw'ambere")
        print("0000. Gusohoka")

        user_choose = input("")
        if user_choose == '0':
            login_userkiny()
        elif user_choose == '00':
            userlogin_appealkiny()
        elif user_choose == '000':
            register_userkiny()
        elif user_choose== '0000':
            quit()    
        else:
            print("Guhitamo Nabi . Mwongere Mugerageze!!")

#fuction for registration of account of new user
def register_user():
    user_fullname = input("Please enter your Full name: ")
    username = input("Please enter your Username: ")
    user_email = input("Please enter your Email: ")
    user_password = input("Enter password: ")
    
    # Phone number validation
    while True:
        user_phone = input("Please enter your Phone number (10 digits, starting with 078, 079, 072, or 073): ")
        if re.match(r'^(078|079|072|073)\d{7}$', user_phone):
            break
        else:
            print("Invalid phone number. Please enter a valid 10-digit phone number starting with 078, 079, 072, or 073.")
    
    # Gender input
    while True:
        user_gender = input("Please enter your Gender (M/F): ").upper()
        if user_gender in ['M', 'F']:
            break
        else:
            print("Invalid input. Please enter 'M' for Male or 'F' for Female.")
    
    # Insert the data into the database
    conn.execute("""INSERT INTO circle
                    (name, username, email, password, phone_number, gender, date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                 (user_fullname, username, user_email, user_password, user_phone, user_gender, datetime.now()))
    connection.commit()
    print("Data inserted successfully")
    input("Press Enter to go back to main menu...")


#fuction for make appeal of complaint 
def make_appeal():
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="cpmsphp"
)

    cursor = conn.cursor()
    while True:
        print("PLEASE ENTER COMPLAINT NUMBER")
        print("\n")
        reference_number = input("Please enter your Complaint Number: ")
        
        # Fetch complaint details from completedcomp table
        cursor.execute("SELECT compnum, remark FROM completedcomp WHERE compnum = %s", (reference_number,))
        data = cursor.fetchone()
        if data:
            # Display the complaint details
            complaint_view(data)
            
            # Ask the user if they want to appeal
            appeal_choice = input("Would you like to file an appeal? (y/n): ").lower()
            
            if appeal_choice == 'y':
                user_phone = input("Please enter your User Phone: ")
                appeal_reason = input("Please enter your reason for appeal: ")
                
                # Insert the appeal into the compappeal table
                cursor.execute(
                    "INSERT INTO compappeal (phone_number, appeal_reason, compnum) VALUES (%s, %s, %s)",
                    (user_phone, appeal_reason, data[0])
                )
                conn.commit()
                
                print("Your appeal has been submitted successfully.")
                
            choice = input("Press B to go back to main menu or any other key to exit: ").lower()
            if choice == 'b':
                break
        else:
            print("Complaint number not found.")
            choice = input("Press B to go back to main menu or any other key to retry: ").lower()
            if choice == 'b':
                break

#function of user to login before make his/her appeal of complaint 
def userlogin_appeal():
    """Authenticate user and allow them to make a complaint if login is successful."""
    conn = None
    cursor = None
    try:
        # Database connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cpmsphp"
        )
        cursor = conn.cursor(dictionary=True)
        
        while True:
            print("ENTER YOUR CREDENTIALS")
            print("\n")
            user_phone = input("Please enter your Phone Number: ")
            user_pin = input("Please enter your PIN: ")
            
            # Check user credentials
            query = "SELECT * FROM circle WHERE phone_number=%s AND password=%s"
            cursor.execute(query, (user_phone, user_pin))
            

            data = cursor.fetchone()
            
            if data:
                print("Login successful.")
                message = make_appeal()
                print(message)
                break
            else:
                print("Failed to login")
                choice = input("Press B to go back to main menu or any other key to retry: ")
                if choice.lower() == 'b':
                    break
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

#function for user to ogin before make new complaint
def login_user():
    """Authenticate user and allow them to make a complaint if login is successful."""
    conn = None
    cursor = None
    try:
        # Database connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cpmsphp"
        )
        cursor = conn.cursor(dictionary=True)
        
        while True:
            print("ENTER YOUR CREDENTIAL")
            print("\n")
            user_phone = input("ENter your Phone Number: ")
            user_pin = input("Enter Your Password: ")
            
            # Check user credentials
            query = "SELECT * FROM circle WHERE phone_number=%s AND password=%s"
            cursor.execute(query, (user_phone, user_pin))
            

            data = cursor.fetchone()
            
            if data:
                print("Login Successfull.")
                message = add_complaint(user_phone)
                print(message)
                break
            else:
                print("Fail to Login")
                choice = input("Please Press b to go Back: ")
                if choice.lower() == 'b':
                    break
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

#fuction for getting user details
def get_user_details(phone_number):
    """Fetch user details from the database based on the phone number."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cpmsphp"
        )
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, name, username, email, phone_number FROM circle WHERE phone_number = %s"
        cursor.execute(query, (phone_number,))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

#fuction for adding a new complaint
def add_complaint(phone_number):
    """Insert a new complaint into the cmp_log table."""
    conn = None
    cursor = None
    try:
        # Fetch user details based on the email
        user = get_user_details(phone_number)
        if not user:
            return "No user Found."

        id = user['id']
        name = user['name']
        username = user['username']
        email = user['email']
        phoneno =user['phone_number']

        # Collect additional user input
        #phoneno = input("Enter your Phone Number (10 digits): ")
        subject = input("Enter The  Subject of Complaint: ")

        complain = input("Enter your Complaint: ")


        # Validate phone number
        #if not phoneno.isdigit() or len(phoneno) != 10:
        #    return "Invalid Phone Number. Please enter a 10-digit number."

        # Generate reference number
        ref = random.randint(3858558, 10000000)

        # Insert complaint into cmp_log table
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cpmsphp"
        )
        cursor = conn.cursor()
        sql = ("INSERT INTO cmp_log (user_id, name, username, email, phoneno, subject, complain, ref_no, date) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data = (id, name, username, email, phoneno, subject, complain, ref,datetime.now())
        cursor.execute(sql, data)
        conn.commit()
        message = f"Your complaint has been registered, you need to come with the required file. Your reference number is  {ref}."
        
    except mysql.connector.Error as err:
        message = f"Failed to register your complaint. Error: {err}"
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return message


#function for viewing compaint
def complaint_view(data):
    print("\nComplaint Details:")
    print(f"Reference Number: {data[0]}")
    print(f"Remark: {data[1]}")
    print("\n")

# ABOVE IS OPTION FOR ENGLISH ONE,AND ABOVE ONE IS FOR KINYARWANDA OPTION






#fuction for registration of account of new user
def register_userkiny():
    user_fullname = input("Mwandike Amazina Yanyu Yombi: ")
    username = input("Mwandike Izina Muzajya Mukoresha: ")
    user_email = input("Mwandike Email Yanyu: ")
    user_password = input("Mwandike Ijambo Banga Muzajya Mukoresha: ")
    
    # Phone number validation
    while True:
        user_phone = input("Mwandike Nimero Ya Telephone Igizwe(Imibare 10 ,Itangizwa 078, 079, 072, cy 073): ")
        if re.match(r'^(078|079|072|073)\d{7}$', user_phone):
            break
        else:
            print("Nimero Mushizemo Ntiyemewe. Mushiremo Nimero Zemewe Zigizwe Ni Mibare 10 Zitangizwa 078, 079, 072, cy 073.")
    
    # Gender input
    while True:
        user_gender = input("Mwandike(M) Igitsina Gabo,(F) Kugitsina Gore: ").upper()
        if user_gender in ['M', 'F']:
            break
        else:
            print("Mwanditse Ibitaribyo. Mwandike 'M' Kubagabo cy 'F' Kubagore.")
    
    # Insert the data into the database
    conn.execute("""INSERT INTO circle
                    (name, username, email, password, phone_number, gender, date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                 (user_fullname, username, user_email, user_password, user_phone, user_gender, datetime.now()))
    connection.commit()
    print("Kwiyandikisha Bigenze Neza")
    input("Mukande kugirango musubire Ahabanza...")


#fuction for make appeal of complaint
def make_appealkiny():
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="cpmsphp"
)

    cursor = conn.cursor()
    while True:
        print("MWANDIKE NIMERO Y'IKIREGO")
        print("\n")
        reference_number = input("Mwandike Nimero Yikirego: ")
        
        # Fetch complaint details from completedcomp table
        cursor.execute("SELECT compnum, remark FROM completedcomp WHERE compnum = %s", (reference_number,))
        data = cursor.fetchone()
        if data:
            # Display the complaint details
            complaint_viewkiny(data)
            
            # Ask the user if they want to appeal
            appeal_choice = input("Murifuza Gutanga Ubujurire? (y/n): ").lower()
            
            if appeal_choice == 'y':
                user_phone = input("Mwandike Nimero Yanyu: ")
                appeal_reason = input("Impavu Yubujurire: ")
                
                # Insert the appeal into the compappeal table
                cursor.execute(
                    "INSERT INTO compappeal (phone_number, appeal_reason, compnum) VALUES (%s, %s, %s)",
                    (user_phone, appeal_reason, data[0])
                )
                conn.commit()
                
                print("Ubujurire Bwanyu Bwatanze Neza.")
                
            choice = input("Mukande B Musohoke: ").lower()
            if choice == 'b':
                break
        else:
            print("Ntakirego Kibonetse.")
            choice = input("ukande B Musohoke: ").lower()
            if choice == 'b':
                break

#fuction for make appeal of complaint
def userlogin_appealkiny():
    """Authenticate user and allow them to make a complaint if login is successful."""
    conn = None
    cursor = None
    try:
        # Database connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cpmsphp"
        )
        cursor = conn.cursor(dictionary=True)
        
        while True:
            print("MWANDIKE IBIBARANGA")
            print("\n")
            user_phone = input("Mwandike Nimero ya Telephone: ")
            user_pin = input("Mwandike Ijambo Banga: ")
            
            # Check user credentials
            query = "SELECT * FROM circle WHERE phone_number=%s AND password=%s"
            cursor.execute(query, (user_phone, user_pin))
            

            data = cursor.fetchone()
            
            if data:
                print("Kwinjira Bigenze Neza.")
                message = make_appealkiny()
                print(message)
                break
            else:
                print("Ntibikunze Kwinjira Mwongere Mugerageze")
                choice = input("Mukande B Musohoke: ")
                if choice.lower() == 'b':
                    break
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()



#fuction for user login
def login_userkiny():
    """Authenticate user and allow them to make a complaint if login is successful."""
    conn = None
    cursor = None
    try:
        # Database connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cpmsphp"
        )
        cursor = conn.cursor(dictionary=True)
        
        while True:
            print("MWANDIKE IBIBARANGA")
            print("\n")
            user_phone = input("Mwandike Nimero Ya Telephone: ")
            user_pin = input("Mwandike Ijambo Banga: ")
            
            # Check user credentials
            query = "SELECT * FROM circle WHERE phone_number=%s AND password=%s"
            cursor.execute(query, (user_phone, user_pin))
            

            data = cursor.fetchone()
            
            if data:
                print("Kwinjira Bigenze Neza.")
                message = add_complaintkiny(user_phone)
                print(message)
                break
            else:
                print("Ntibikunze Kwinjira Mwongere Mugerageze")
                choice = input("Mukande B Musohoke: ")
                if choice.lower() == 'b':
                    break
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

#fuction for getting user details
def get_user_detailskiny(phone_number):
    """Fetch user details from the database based on the phone number."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cpmsphp"
        )
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, name, username, email, phone_number FROM circle WHERE phone_number = %s"
        cursor.execute(query, (phone_number,))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

#fuction for adding a new complaint
def add_complaintkiny(phone_number):
    """Insert a new complaint into the cmp_log table."""
    conn = None
    cursor = None
    try:
        # Fetch user details based on the email
        user = get_user_detailskiny(phone_number)
        if not user:
            return "Ntamuntu tubonye Ufite Iyi Nimero."

        id = user['id']
        name = user['name']
        username = user['username']
        email = user['email']
        phoneno =user['phone_number']

        # Collect additional user input
        #phoneno = input("Enter your Phone Number (10 digits): ")
        subject = input("Mwandike Impamvu Y'ikirego: ")
        complain = input("Mwandike Ikirego: ")

        # Validate phone number
        #if not phoneno.isdigit() or len(phoneno) != 10:
        #    return "Invalid Phone Number. Please enter a 10-digit number."

        # Generate reference number
        ref = random.randint(3858558, 10000000)

        # Insert complaint into cmp_log table
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cpmsphp"
        )
        cursor = conn.cursor()
        sql = ("INSERT INTO cmp_log (user_id, name, username, email, phoneno, subject, complain, ref_no, date) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data = (id, name, username, email, phoneno, subject, complain, ref, datetime.now())
        cursor.execute(sql, data)
        conn.commit()
        message = f"Ikirego Cyanyu Cyanditse,Mukeneye Kuzana Ibindi Bijyanye Nacyo. Nimero Y'ikirego  {ref}."
        
    except mysql.connector.Error as err:
        message = f"Habaye Ikibazo Mukwandika Ikirego Mwongere Mugerageze. Error: {err}"
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return message

#fuction for viewing complaint
def complaint_viewkiny(data):
    print("\nAMAKURU Y'IKIREGO:")
    print(f"Nimero Y'ikirego: {data[0]}")
    print(f"Umwanzuro Wafashwe: {data[1]}")
    print("\n")

# Start the application
if __name__ == "__main__":
     main_menu()
