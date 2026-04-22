import time
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
# print("current file path:", os.getcwd())

def read_merchant_code(m_file_name):
# know who is active now, so I don't need to ask what is his code
    with open(m_file_name, "r") as user_file:
        lines = user_file.readlines()
        for line in lines:
            line = line.replace("\n", "").split(" ; ")
            if line[3] == "active":
                active_account_code = line[0]
    return active_account_code

def read_merchant_gmail(m_file_name):
    # know who is active now, so I don't need to ask what is his gmail
    with open(m_file_name, "r") as user_file:
        lines = user_file.readlines()
        for line in lines:
            line = line.replace("\n", "").split(" ; ")
            if line[3] == "active":
                active_account_gmail = line[1]
    return active_account_gmail

def detection_invalid_gmail(input_gmail):
    # in case forget enter "@"
    try:
        gmail = input_gmail.split("@")
        # cannot enter empty gmail
        if gmail[0] == "":
            print("\033[31mYour gmail account cannot be empty.\033[0m")
            time.sleep(0.5)
            return 0
        # cannot enter other email address
        elif gmail[1] != "gmail.com":
            print("\033[31mWe only accept Google Gmail Address.\033[0m")
            time.sleep(0.5)
            return 0
        # give 1 to stop looping
        else:
            return 1
    # cannot enter without "@"
    except IndexError:
        print("\033[31mInvalid Gmail format.\033[0m")
        time.sleep(0.5)
        return 0
    
def only_one_merchant_active(m_file_name):
    # count how many account is active
    how_many_active = 0
    with open(m_file_name, "r") as user_file:
        lines = user_file.readlines()
        for line in lines:
            line = line.replace("\n", "").split(" ; ")
            if line[3] == "active":
                how_many_active += 1
    # have 2 account active, then change all "active" to "offline", but "blocked" still there
    if how_many_active > 1:
        with open(m_file_name, "r") as user_file:
            lines = user_file.readlines()
        with open(m_file_name, 'w') as user_file:
            for line in lines:
                line = line.replace("\n", "").split(" ; ")
                if line[3] == "active":
                    line[3] = "offline"
                user_file.write(" ; ".join(line) + '\n')
                
def motion_merchant_signup(m_file_name):
# loop3 asking merchant's code
    loop3 = 0
    while loop3 == 0:
        loop3 = 1
        print("\nWhat type of business do you operate?")
        merchant_type = input("H. Hotel\nT. Travel Agency\nR. Restaurant\nA. Attraction\n> ")
        merchant_code = merchant_type.upper().strip()
        # not allow other code
        if merchant_code not in ("H", "T", "R", "A"):
            print("\033[31mChoose either Hotel / Travel Agency / Restaurant / Attraction only.\033[0m")
            time.sleep(1)
            loop3 = 0
# loop asking account gmail
    loop = 0
    while loop < 1:
        loop = 1
    # loop4 asking correct gmail
        loop4 = 0
        while loop4 == 0:
            sign_up_gmail = input("\nEnter your gmail account for sign up.\n> ")
            sign_up_gmail = sign_up_gmail.lower()
            loop4 = detection_invalid_gmail(sign_up_gmail)
        # in case file is not exist, read if gmail repeated
        try:
            user_file = open(m_file_name, "r")
            lines = user_file.readlines()
            for line in lines:
                line = line.replace("\n", "").split(" ; ")
                if sign_up_gmail == line[1]:
                    print("\033[31mThis Account has already been registered. Please use a different gmail address.\033[0m")
                    loop = 0
            user_file.close()
        # create then write the title into file
        except FileNotFoundError:
            user_file = open(m_file_name, "w")
            user_file.write("Code ; Gmail ; Password ; Status\n")
# loop2 asking secure password
    loop2 = 0
    while loop2 == 0:
        loop2 = 1
        sign_up_password = input("\nEnter your password.\n> ")
        # set = 0
        password_uppercase = password_number = password_special_character = 0
        # collect which is special character
        special_character = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/\\`~"
        # must have 8 number of password
        if len(sign_up_password) < 8:
            print("\033[31mPassword must contain at least 8 characters!\033[0m")
            loop2 = 0
            time.sleep(1)
        # check password security
        else:
            for password in sign_up_password:
                if "A" <= password <= "Z":
                    password_uppercase += 1
                elif "0" <= password <= "9":
                    password_number += 1
                elif password in special_character:
                    password_special_character += 1
            # if password security, then confirm again
            if password_uppercase > 0 and password_number > 0 and password_special_character > 0:
                confirmed_password = input("\nConfirm your password again.\n> ")
                if confirmed_password != sign_up_password:
                    print("\033[31mPassword Incorrect, retry again.\033[0m")
                    loop2 = 0
            # display which requirement didn't get
            else:
                loop2 = 0
                print("---------------Password Requirements---------------")
                if password_uppercase == 0:
                    print("\033[31m1. Your password must contain at least 1 uppercase letter.\033[0m")
                else:
                    print("\033[32m1. Good! Your password contains", password_uppercase, "uppercase letter.\033[0m")
                if password_number == 0:
                    print("\033[31m2. Your password must contain at least 1 number.\033[0m")
                else:
                    print("\033[32m2. Good! Your password contains", password_number, "number.\033[03m")
                if password_special_character == 0:
                    print("\033[31m3. Your password must contain at least 1 special character.\033[0m")
                else:
                    print("\033[32m3. Good! Your password contains", password_special_character, "special character.\033[0m")
                time.sleep(1)
    # add merchant information into file
    with open(m_file_name, "a") as user_file:
        user_file.write(" ; ".join([merchant_code, sign_up_gmail, sign_up_password, "offline"])+"\n")
        print("\033[34m<<", sign_up_gmail, ">>\033[0m sign up successful!")
    # ask what they want next
    merchant_log_in_sign_out()
    
def motion_merchant_login(m_file_name):
    # in case file not exist
    try:
        user_file = open(m_file_name, "r")
        user_file.close()
    except FileNotFoundError:
        print("Seem you haven't sign up an account.")
        time.sleep(1)
        motion_merchant_signup(m_file_name)
    else:
        only_one_merchant_active(m_file_name)
    # loop2 asking merchant to log in
        loop2 = 0
        while loop2 == 0:
        # loop3 checking invalid gmail
            loop3 = 0
            while loop3 == 0:
                log_in_gmail = input("\nEnter your gmail account for log in.\n> ")
                log_in_gmail = log_in_gmail.lower()
                loop3 = detection_invalid_gmail(log_in_gmail)
            # if gmail found, then +1
            count_name = 0
            # find the line where name is, so I can know where to find password
            with open(m_file_name, "r") as user_file:
                lines = user_file.readlines()
            with open(m_file_name, "w") as user_file:
                for line in lines:
                    line = line.replace("\n", "").split(" ; ")
                    if log_in_gmail == line[1]:
                        # if account is active, then no need password
                        if line[3] == "active":
                            print("\nThis account\033[34m has been activated\033[0m, so no password is required.")
                            loop2 = 1
                        # if account is blocked, then cannot access
                        elif line[3] == "blocked":
                            print("\nThis account\033[31m has been blocked.\033[0m")
                        # offline account change to active
                        else:
                        # loop1 ask 3 time to enter password
                            loop1 = 3
                            while loop1 > 0:
                                log_in_password = input("Enter your password.\n> ")
                                # password correct, stop asking gmail, stop asking password
                                if log_in_password == line[2]:
                                    line[3] = "active"
                                    print("\033[34m<<", log_in_gmail, ">>\033[0m log in successful!\n")
                                    loop2 = 1
                                    loop1 = 0
                                    time.sleep(1)
                                    break
                                else:
                                    loop1 = loop1 - 1
                                    # chances finished then stop to log in
                                    if loop1 == 0:
                                        print("\033[31mTry after 10 minutes. Don't Shut This Website!(Jason: just wait, dont re run it,cause error.\033[0m")
                                        time.sleep(6)
                                    else:
                                        print("\033[31mPASSWORD INCORRECT!\nYou have", loop1, "chance to re-enter your password.\033[0m")
                        count_name += 1
                    # write "active" into file
                    user_file.write(" ; ".join(line) + '\n')
                if count_name == 0:
                    print("\033[31m<<", log_in_gmail, ">> is not founded in system. Try another one.\033[0m")
        # maybe after have 2 acitve account, so check which is the old actived account, then change it into "offline"
        with open(m_file_name, "r") as user_file:
            lines = user_file.readlines()
            active_found = 0
            for line in lines:
                line = line.replace("\n", "").split(" ; ")
                if line[3] == "active":
                    active_found += 1
            with open(m_file_name, "w") as user_file:
                for line in lines:
                    line = line.replace("\n", "").split(" ; ")
                    if active_found > 1:
                        if line[1] != log_in_gmail:
                            # blocked account still "blocked"
                            if line[3] == "blocked":
                                line[3] = "blocked"
                            elif line[3] == "Status":
                                line[3] = "Status"
                            else:
                                line[3] = "offline"
                        else:
                            # blocked account still "blocked"
                            if line[3] == "blocked":
                                line[3] = "blocked"
                            else:
                                line[3] = "active"
                    user_file.writelines(" ; ".join(line) + '\n')
                    
def motion_merchant_logout(m_file_name):
    # in case file is not exist
    try:
        user_file = open(m_file_name, "r")
        user_file.close()
    except FileNotFoundError:
        print("Seem you haven't sign up an account.")
        time.sleep(1)
        motion_merchant_signup(m_file_name)
    # actually should remove this part, because won't have > 2 active account anymore, I just want to keep my code
    count_active = 0
    print("------Activated Account------")
    with open(m_file_name, "r") as user_file:
        lines = user_file.readlines()
        for line in lines:
            line = line.replace("\n", "").split(" ; ")
            # display active account only
            if line[3] == "active":
                print("-", line[1])
                count_active += 1
    # no active account then no need to log out
    if count_active == 0:
        print("\033[31mNo activated account, moving to the next step.\033[0m\n")
        merchant_log_in_sign_out()
    else:
    # loop asking motion
        loop = 0
        while loop == 0:
            loop = 1
            ask_log_out = input("\nDo you want to log out?\n> ")
            ask_log_out = ask_log_out.lower().strip()
            # count check your account inside the file or not
            count = 0
            if ask_log_out == "yes":
                with open(m_file_name, "w") as user_file:
                    for line in lines:
                        line = line.replace("\n", "").split(" ; ")
                        if line[3] == "active":
                            line[3] = "offline"
                            print("\033[34m<<", line[1], ">>\033[0m is successfully logged out.")
                            count += 1
                        user_file.write(" ; ".join(line) + '\n')
                if count == 0:
                    print("\033[31mYour name is not founded in system. Try another one.\033[0m\n")
                    loop = 0
            # no log out then ask what to do next
            elif ask_log_out == "no":
                merchant_log_in_sign_out()
            else:
                print("\033[31mInvalid Input.\033[0m")
                time.sleep(1)
                loop = 0
                
def back_up_product_file(file_name):
# in case file is disappear, we upload our backup file
    product_file = open(file_name, "w")
    product_file.write("Code ; Name ; Place ; Price ; Availability ; Date ; Status\n"
                        "H ; Sunway Pyramid Hotel ; Petaling Jaya ; MYR 614 ; 4ppl ; 13/7/2024 ; Canceled\n"
                        "H ; Cititel Mid Valley ; Kuala Lumpur ; MYR 240 ; 5ppl ; 12/7/2024 ; Available\n"
                        "H ; Cititel Mid Valley ; Kuala Lumpur ; MYR 280 ; 2ppl ; 13/7/2024 ; Booked\n"
                        "A ; Thean Hou Temple ; Kuala Lumpur ; MYR 0 ; 168ppl ; 13/7/2024 ; Available\n"
                        "A ; Petronasains ; Kuala Lumpur ; MYR 40 ; 40ppl ; 13/7/2024 ; Available\n"
                        "A ; Dataran Merdeka ; Kuala Lumpur ; MYR 0 ; 400ppl ; 1/7/2024 ; Available\n"
                        "A ; Batu Cave ; Gombak ; MYR 0 ; 800ppl ; 5/7/2024 ; Available\n"
                        "R ; Xin Cuisine ; Kuala Lumpur ; MYR 60 ; 70ppl ; 10/7/2024 ; Available\n"
                        "T ; Seasonice Travel & Tour ; Kuala Lumpur ; MYR 268 ; 20ppl ; 11/7/2024 ; Available\n"
                        "T ; Hello Holidays Travel ; Kuala Lumpur ; MYR 198 ; 13ppl ; 12/7/2024 ; Available\n"
                        "R ; Hai Di Lao ; Kuala Lumpur ; MYR 150 ; 4ppl ; 13/7/2024 ; Available\n"
                       )
    
def m_add_product(p_file_name, m_file_name):
# read your code and gmail
    active_account_gmail = read_merchant_gmail(m_file_name)
    active_account_code = read_merchant_code(m_file_name)
# loop asking your product detail
    loop = 0
    while loop == 0:
        loop = 1
        product_detail = input("\n1. What is the name of your restaurant/hotel/attraction/travel agency?\n"
                               "2. What is the address of your service?\n"
                               "3. What are your pricing details\n"
                               "4. How many people can your service accommodate?\n"
                               "5. What is the available dates for your service?\n"
                               "\033[3;34mE.g. APU , Bukit Jalil , 0 , 723 , 23/7/2024\033[0m\n> ")
        # in case typing error
        try:
            details = product_detail.split(" , ")
            name = details[0]
            place = details[1]
            price = "MYR " + details[2]
            availability = details[3] + "ppl"
            date = details[4]
        except UnboundLocalError:
            print("\033[31mPlease enter in a correct format!\033[0m")
            time.sleep(1)
            loop = 0
        except IndexError:
            print("\033[31mPlease enter in a correct format!\033[0m")
            time.sleep(1)
            loop = 0
    # someone would type short form, nicely help them change
    if place in ("KL", "Kl", "kl"):
        place = "Kuala Lumpur"
    elif place in ("PJ", "Pj", "pj"):
        place = "Petaling Jaya"
    elif place in ("SA", "Sa", "sa"):
        place = "Shah Alam"
    elif place in ("SJ", "Sj", "sj"):
        place = "Subang Jaya"
    # someone type simply, help them capitalize
    new_name = name.title()
    new_place = place.title()
    # show information
    print("---------------Product Informations---------------")
    print("Name:", new_name, "\nPlace:", new_place, "\nPrice:", price, "\nAvailability:", availability, "\nDate(DD/MM/YYYY):", date)
    time.sleep(2)
    print("Dear \033[34m<<", active_account_gmail, ">>\033[0m ", end="")
    # check information correct or not
    motion = input(",If all the information is correct, type \033[32m< confirm >\033[0m\n> ")
    motion = motion.strip().lower()
    if motion == "confirm":
        with open(p_file_name, "a") as product_file:
            product_file.write(" ; ".join([active_account_code, new_name, new_place, price, availability, date, "Available"]) + "\n")
    else:
        print("\033[31mInvalid Input. Cleaning Incorrect Data.\033[0m")
        time.sleep(2)
        m_add_product(p_file_name, m_file_name)
        
def m_delete_product(p_file_name, m_file_name):
# read your code and gmail
    active_account_gmail = read_merchant_gmail(m_file_name)
    active_account_code = read_merchant_code(m_file_name)
    # only display product that might relate to merchant
    with open(p_file_name, "r") as product_file:
        lines = product_file.readlines()
        print("Dear \033[34m<<", active_account_gmail, ">>\033[0m , These are the products which might related to you.")
        for line in lines:
            time.sleep(0.5)
            line = line.replace("\n", "").split(" ; ")
            if line[0] == active_account_code:
                print("-", line[1])
    time.sleep(1)
# loop asking motion
    loop = 0
    while loop == 0:
        loop = 1
        delete_which_product = input("Which product you want to delete.\n> ")
        delete_which_product = delete_which_product.title()
        count_number = 0
        with open(p_file_name, "w") as product_file:
            for line in lines:
                line = line.replace("\n", "").split(" ; ")
                if delete_which_product == line[1]:
                    line = ""
                    print(delete_which_product, "is successfully deleted")
                    count_number = 1
                product_file.writelines(" ; ".join(line) + "\n")
            if count_number == 0:
                print("\033[31m", delete_which_product, "is not found at Products List.\033[0m")
                time.sleep(1)
                loop = 0
# jason's file management system, i proud of my code
    with open(p_file_name, "r") as product_file:
        lines = product_file.readlines()
    with open(p_file_name, "w") as product_file:
        for line in lines:
            line = line.replace("\n", "")
            if line == "":
                continue
            else:
                product_file.write(line + "\n")
                
def m_update_product(p_file_name, m_file_name):
# read your code and gmail
    active_account_gmail = read_merchant_gmail(m_file_name)
    active_account_code = read_merchant_code(m_file_name)
    # only display product that might relate to merchant
    with open(p_file_name, "r") as product_file:
        lines = product_file.readlines()
        print("Dear \033[34m<<", active_account_gmail, ">>\033[0m , These are the products which might related to you.")
        for line in lines:
            time.sleep(0.5)
            line = line.replace("\n", "").split(" ; ")
            if line[0] == active_account_code:
                print("-", line[1])
    time.sleep(1)
# loop asking motion
    loop = 0
    while loop == 0:
        loop = 1
        update_which_product = input("Which product you want to update.\n> ")
        update_which_product = update_which_product.title()
        count_number = 0
        with open(p_file_name, "w") as product_file:
            for line in lines:
                line = line.replace("\n", "").split(" ; ")
                if update_which_product == line[1]:
                    print(line[1:6])
                    loop1 = 0
                    while loop1 == 0:
                        loop1 = 1
                        # in case the input is not number
                        try:
                            which_part = int(input("Which information you want to update? \033[31m(number)\033[0m\n> "))
                        except ValueError:
                            loop1 = 0
                        else:
                            if which_part not in (1, 2, 3, 4, 5):
                                print("\033[31m1 to 5 only\033[0m")
                                time.sleep(1)
                                loop1 = 0
                    count_number = 1
                    new_information = input("New Information\n> ")
                    if which_part == 1:
                        line[which_part] = new_information.title()
                    # someone would type short form, nicely help them change
                    elif which_part == 2:
                        if new_information in ("KL", "Kl", "kl"):
                            new_information = "Kuala Lumpur"
                        elif new_information in ("PJ", "Pj", "pj"):
                            new_information = "Petaling Jaya"
                        elif new_information in ("SA", "Sa", "sa"):
                            new_information = "Shah Alam"
                        elif new_information in ("SJ", "Sj", "sj"):
                            new_information = "Subang Jaya"
                        line[which_part] = new_information.title()
                    elif which_part == 3:
                        line[which_part] = "MYR " + new_information
                    elif which_part == 4:
                        line[which_part] = new_information + "ppl"
                    else:
                        line[which_part] = new_information
                    print("Updated Product Information")
                    print(line[1:6])
                product_file.writelines(" ; ".join(line) + "\n")
            if count_number == 0:
                print("\033[31m", update_which_product, "is not found at Products List.\033[0m")
                time.sleep(1)
                loop = 0
                
def m_view_booking(p_file_name, m_file_name):
# read your code and gmail
    active_account_gmail = read_merchant_gmail(m_file_name)
    active_account_code = read_merchant_code(m_file_name)
    # only display product that might relate to merchant
    with open(p_file_name, "r") as product_file:
        lines = product_file.readlines()
        print("Dear \033[34m<<", active_account_gmail, ">>\033[0m , These are the products which might related to you.")
        for line in lines:
            time.sleep(0.5)
            line = line.replace("\n", "").split(" ; ")
            if line[0] == active_account_code:
                print("-", line[1::])
    time.sleep(1)
    
def m_cancel_booking(p_file_name, m_file_name):
# read your code and gmail
    active_account_gmail = read_merchant_gmail(m_file_name)
    active_account_code = read_merchant_code(m_file_name)
    # only display product that might relate to merchant
    with open(p_file_name, "r") as product_file:
        lines = product_file.readlines()
        print("Dear \033[34m<<", active_account_gmail, ">>\033[0m , These are the products which might related to you.")
        for line in lines:
            time.sleep(0.5)
            line = line.replace("\n", "").split(" ; ")
            if line[0] == active_account_code:
                print("-", line[1::])
    time.sleep(1)
# loop asking motion
    loop = 0
    while loop == 0:
        loop = 1
        cancel_which_product = input("Which product you want to cancel.\n> ")
        cancel_which_product = cancel_which_product.title()
        count_number = 0
        with open(p_file_name, "w") as product_file:
            for line in lines:
                line = line.replace("\n", "").split(" ; ")
                if cancel_which_product == line[1]:
                    line[6] = "Cancelled"
                    print("Product Successfully Canceled")
                    count_number = 1
                product_file.writelines(" ; ".join(line) + "\n")
            if count_number == 0:
                print("\033[31m", cancel_which_product, "is not found at Products List.\033[0m")
                time.sleep(1)
                loop = 0
                
def m_confirm_booking(p_file_name, m_file_name):
# read your code and gmail
    active_account_gmail = read_merchant_gmail(m_file_name)
    active_account_code = read_merchant_code(m_file_name)
    # only display product that might relate to merchant
    count_number1 = 0
    with open(p_file_name, "r") as product_file:
        lines = product_file.readlines()
        print("Dear \033[34m<<", active_account_gmail, ">>\033[0m , These are the products which might related to you.")
        for line in lines:
            time.sleep(0.5)
            line = line.replace("\n", "").split(" ; ")
            if line[0] == active_account_code:
                if line[6] == "Booked":
                    count_number1 += 1
                    print("-", line[1::])
    time.sleep(1)
    if count_number1 > 0:
        loop = 0
        while loop == 0:
            loop = 1
            confirm_which_booking = input("Which product you want to confirm booking.\n> ")
            confirm_which_booking = confirm_which_booking.title()
            count_number = 0
            with open(p_file_name, "w") as product_file:
                for line in lines:
                    line = line.replace("\n", "").split(" ; ")
                    # only booked product can be confirmed
                    if confirm_which_booking == line[1]:
                        if line[6] == "Booked":
                            line[6] = "Confirmed Booking by Merchant"
                            print("Booking Successfully Confirmed")
                            count_number = 1
                    product_file.writelines(" ; ".join(line) + "\n")
                if count_number == 0:
                    print("\033[31m", confirm_which_booking, "is not found at Products List.\033[0m")
                    time.sleep(1)
                    loop = 0
    else:
        print("\033[31mNo product has been booked before.\033[0m")
        
def merchant_log_in_sign_out():
# file name
    merchant_file_name = "Merchant Registration.txt"
    product_file_name = "Product Information.txt"
    loop = 0
    while loop == 0:
        loop = 1
        x1 = input("\nDo you want to \033[34mlog in\033[0m,\033[34m log out\033[0m or \033[34msign up\033[0m account?\n> ")
        motion = x1.lower().replace(" ", "")
        if motion == "signup":
            motion_merchant_signup(merchant_file_name)
            time.sleep(1)
        elif motion == "login":
            motion_merchant_login(merchant_file_name)
            m_product()
        elif motion == "logout":
            motion_merchant_logout(merchant_file_name)
        else:
            print("\033[31mInvalid Input.\033[0m\n")
            time.sleep(1)
            loop = 0
            
def m_product():
# file name
    merchant_file_name = "Merchant Registration.txt"
    product_file_name = "Product Information.txt"
    loop = 0
    while loop == 0:
        loop = 1
        try:
            product_file = open(product_file_name, "r")
            product_file.close()
        except FileNotFoundError:
            print("Loading File System...")
            time.sleep(1)
            back_up_product_file(product_file_name)
        # ask motion
        x2 = input("\nDo you want to \033[34mAdd / Delete / Update\033[0m Information or \033[34mView / Cancel / Confirm\033[0m Booking?\n> ")
        x2 = x2.lower().replace(" ", "")
        if x2 == "add":
            m_add_product(product_file_name, merchant_file_name)
        elif x2 == "delete":
            m_delete_product(product_file_name, merchant_file_name)
        elif x2 == "update":
            m_update_product(product_file_name, merchant_file_name)
        elif x2 == "view":
            m_view_booking(product_file_name, merchant_file_name)
        elif x2 == "cancel":
            m_cancel_booking(product_file_name, merchant_file_name)
        elif x2 == "confirm":
            m_confirm_booking(product_file_name, merchant_file_name)
        else:
            print("\033[31mInvalid Input.\033[0m")
            time.sleep(1)
            loop = 0
            
def create_account(username, password):
    with open("Admin Account.txt", "a") as f:
        f.write(f"{username}:{password}\n")
    print("Account created successfully!")
    
def check_admin_name_availability(username):
    try:
        with open("Admin Account.txt", "r") as f:
            users = f.readlines()
            for user in users:
                if user.split(":")[0] == username:
                    return False
            return True
    except FileNotFoundError:
        return True
    
def signup():
    username = input("Enter a username: ")
    if check_admin_name_availability(username):
        password = input("Enter a password: ")
        create_account(username, password)
    else:
        print("Username already taken. Please try again.")
        
def login(username, password):
    try:
        with open("Admin Account.txt", "r") as f:
            users = f.readlines()
            for user in users:
                user_username, user_password = user.strip().split(":")
                if username == user_username and password == user_password:
                    print("Login successful!")
                    return True
            print("Invalid username or password. Please try again.")
            return False
    except FileNotFoundError:
        print("No users found. Please sign up first.")
        file = open("Admin Account.txt", "w")
        file.write("name:password\n")
        return False
    
def admin_login(username, password):
    # Check if username and password are valid
    if username == "admin" and password == "password":
        print("Login successful!")
        return True
    else:
        print("Invalid username or password. Please try again.")
        return False
    
def admin_logout():
    print("You have been logged out.")
    return True

def add_merchant_account():
    code = input("Enter the code for the new merchant account: ")
    code = code.capitalize()
    gmail = input("Enter the Gmail for the new merchant account: ")
    password = input("Enter the password for the new merchant account: ")
    status = "offline"
    with open("Merchant Registration.txt", "a") as f:
        f.write(f"{code} ; {gmail} ; {password} ; {status}\n")
    print("Merchant account added successfully!")
    
def block_merchant_account():
    gmail = input("Enter the Gmail of the merchant account to block: ")
    with open("Merchant Registration.txt", "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if gmail in line:
            lines[i] = line.replace("offline", "blocked")
    with open("Merchant Registration.txt", "w") as f:
        f.writelines(lines)
    print("Merchant account blocked successfully!")
    
def update_promotion():
    try:
        f = open("Product Information.txt", "r")
        f.close()
    except FileNotFoundError:
        print("Loading File System...")
        time.sleep(1)
        back_up_product_file("Product Information.txt")
    finally:
        with open("Product Information.txt", "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                code, name, place, price, availability, date, status = line.strip().split(" ; ")
                print(f"{i+1}. {name} - {place} - {price} - {availability} - {date} - {status}")
        choice = int(input("Enter the number of the promotion to update: ")) - 1
        code, name, place, price, availability, date, status = lines[choice].strip().split(" ; ")
        new_discount = input("Enter the new discount: ")
        new_recommendation = input("Enter the new recommendation: ")
        print("Promotion updated successfully!")
        try:
            f = open("Product Promotion.txt", "r")
            f.close()
        except FileNotFoundError:
            with open("Product Promotion.txt", "w") as f:
                f.write("Name ; New Status ; Recommendation\n")
        finally:
            with open("Product Promotion.txt", "a") as f:
                f.write(f"{name} ; {new_discount} ; {new_recommendation}\n")
            print("Deduction note added to Promotion File")
            
def block_traveller_account():
    print("Travellers:")
    with open("travellers.txt", "r") as f:
        lines = f.readlines()[1:]  # skip the header
        for line in lines:
            name, _, _, phone_number, _ = line.strip().split(" ; ")
            print(f"Name: {name}, Phone Number: {phone_number}")
    phone_number = input("Enter the phone number of the traveller to block: ")
    with open("travellers.txt", "r") as f:
        lines = f.readlines()
    with open("travellers.txt", "w") as f:
        for line in lines:
            if phone_number in line:
                f.write(line.replace("active", "blocked"))
            else:
                f.write(line)
    print("Traveller account blocked successfully!")
    
def main1():
    while True:
        print("KL Trip Planner Application - Admin Menu")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if login(username, password):
                # Login successful, display admin menu
                while True:
                    print("Admin Menu")
                    print("1. Block merchant account")
                    print("2. Add merchant account")
                    print("3. Update promotion")
                    print("4. Block traveller")  # Add new option
                    print("5. Logout")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        # Manage Users feature
                        block_merchant_account()
                    elif choice == "2":
                        # Manage Trips feature
                        add_merchant_account()
                    elif choice == "3":
                        update_promotion()
                    elif choice == "4":
                        block_traveller_account()
                    elif choice == "5":
                        admin_logout()
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == "2":
            signup()
        elif choice == "3":
            print("Exiting Admin Menu.Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            
def display_menu():
    print("Welcome to the Trip Booking System")
    print("1. View Available Trips")
    print("2. View Recommended Trips")
    print("3. Create New Account")
    print("4. Exit")
    choice = input("Please choose an option: ")
    return choice

def read_txt_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    else:
        print(f"The file {file_name} does not exist.")
        
def display_available_trips():
    print("Available Trips:")
    read_txt_file('Product Information.txt')
    input("Press any key to return to the main menu...")
    
def display_recommended_trips():
    print("Recommended Trips:")
    read_txt_file('Product Promotion.txt')
    input("Press any key to return to the main menu...")
    
def create_new_account():
    username = input("Enter username: ")
    password = input("Enter password: ")
    with open('guest_file.txt', 'a', encoding='utf-8') as file:
        file.write(f"{username},{password}\n")
    print("Account created successfully!")
    
def main2():
    while True:
        choice = display_menu()
        if choice == '1':
            display_available_trips()
        elif choice == '2':
            display_recommended_trips()
        elif choice == '3':
            create_new_account()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")
            
def load_users(user_file):
    users = {}
    with open(user_file, 'r') as file:
        for line in file:
            username, password, email, phone, status = line.strip().split(' ; ')
            users[username] = {'password': password, 'email': email, 'phone': phone, 'status': status}
    return users

def load_products(product_file):
    products = []
    with open(product_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            code, name, place, price, availability, date, status = line.strip().split(' ; ')
            product = {'code': code, 'name': name, 'place': place, 'price': price, 'availability': availability, 'date': date, 'status': status}
            products.append(product)
    return products

def save_users(users, user_file):
    with open(user_file, 'w') as file:
        for username, details in users.items():
            file.write(f"{username} ; {details['password']} ; {details['email']} ; {details['phone']} ; {details['status']}\n")
            
def save_products(products, product_file):
    with open(product_file, 'w') as file:
        for product in products:
            file.write(f"{product['code']} ; {product['name']} ; {product['place']} ; {product['price']} ; {product['availability']} ; {product['date']} ; {product['status']}\n")

def book_product(products, product_name):
    for product in products:
        if product['name'] == product_name:
            if product['status'] not in ("Booked", "Cancelled"):
                product['status'] = "Booked"
                print(f"Booking successful for {product['name']}.")
            else:
                print(f"{product['name']} is already booked or cancelled by service provider.")
            return
    print("Product not found.")
def cancel_booking(products, product_name):
    for product in products:
        if product['name'] == product_name:
            if product['status'] == "Booked":
                product['status'] = "Available"
                print(f"Cancellation successful for {product['name']}.")
            else:
                print(f"No booking found for {product['name']}.")
            return
    print("Product not found.")

def display_products(products):
    print("\nProducts:")
    for product in products:
        print(f"{product['name']} | {product['place']} | {product['price']} | {product['availability']} | {product['date']} | {product['status']}")

def search_product(products, keyword):
    results = []
    for product in products:
        if keyword.lower() in product['name'].lower():
            results.append(product)
    return results

def t_login(users, username, password):
    if username in users and users[username]['password'] == password:
        print("Login successful. Welcome,", username + "!")
        return True
    else:
        print("Invalid username or password. Please try again.")
        return False

def sign_up(users, user_file):
    print("Sign Up:")
    while True:
        username = input("Enter username: ")
        if username in users:
            print("Username already exists. Please try again.")
        else:
            break
    password = input("Enter password: ")
    while True:
        email = input("Enter email: ")
        if any(email == details['email'] for details in users.values()):
            print("Email already exists. Please try again.")
        else:
            break
    while True:
        phone = input("Enter phone number: ")
        if any(phone == details['phone'] for details in users.values()):
            print("Phone number already exists. Please try again.")
        else:
            break
    status = "active"
    users[username] = {'password': password, 'email': email,'phone':phone, 'status':status}
    save_users(users,user_file)
    print("Sign up successful. You can now log in.")
    return True

def update_traveler_profile(users, username, user_file):
    print("Update Profile:")
    print("1. Change Username")
    print("2. Change Password")
    print("3. Change Email")
    print("4. Change Phone")
    choice = input("Enter your choice (1/2/3/4): ")
    if choice == "1":
        while True:
            new_username = input("Enter new username: ")
            if new_username in users:
                print("Username already exists. Please try again.")
            else:
                break
        users[new_username] = users.pop(username)
        username = new_username
        print("Username changed successfully.")
    elif choice == "2":
        new_password = input("Enter new password: ")
        users[username]['password'] = new_password
        print("Password changed successfully.")
    elif choice == "3":
        new_email = input("Enter new email: ")
        while True:
            if any(new_email == details['email'] for details in users.values()):
                print("Email already exists. Please try again.")
                new_email = input("Enter new email: ")
            else:
                break
        users[username]['email'] = new_email
        print("Email changed successfully.")
    elif choice == "4":
        new_phone = input("Enter new phone number: ")
        while True:
            if any(new_phone == details['phone'] for details in users.values()):
                print("Phone number already exists. Please try again.")
                new_phone = input("Enter new phone number: ")
            else:
                break
        users[username]['phone'] = new_phone
        print("Phone number changed successfully.")
    else:
        print("Invalid choice.")
    save_users(users, user_file)

def main3():
    user_file = "travellers.txt"
    product_file = "Product Information.txt"
    users = load_users(user_file)
    products = load_products(product_file)
    # Account check
    account_choice = input("Do you have an account? (yes/no): ").lower()
    if account_choice == "no":
        if not sign_up(users, user_file):
            exit()
    # Logging in
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        if t_login(users, username, password):
            break
    # Update profile
    choice = input("Do you want to update your profile? (yes/no): ").lower()
    if choice == "yes":
        update_traveler_profile(users, username, user_file)
    # View or search products
    choice = input("Do you want to view or search for products? (view/search): ").lower()
    if choice == "view":
        display_products(products)
    elif choice == "search":
        keyword = input("Enter keyword to search products: ")
        search_results = search_product(products, keyword)
        if search_results:
            print("\nSearch Results:")
            for result in search_results:
                print(
                    f"{result['name']} | {result['place']} | {result['price']} | {result['availability']} | {result['date']} | {result['status']}")
        else:
            print("No matching products found.")
    # Book a product
    choice = input("Do you want to book a product? (yes/no): ").lower()
    if choice == "yes":
        product_to_book = input("Enter the name of the product to book: ")
        book_product(products, product_to_book)
    # Cancel a booking
    choice = input("Do you want to cancel a booking? (yes/no): ").lower()
    if choice == "yes":
        product_to_cancel = input("Enter the name of the product to cancel booking: ")
        cancel_booking(products, product_to_cancel)
    # Save products after any changes
    save_products(products, product_file)

def who_are_you():
    loop = 0
    while loop == 0:
        loop = 1
        print("\nChoose your Identity.")
        who = input("1. System Administrator\n2. Service Provider\n3. Guest\n4. Traveller\n> ")
        if who == "1":
            if __name__ == "__main__":
                main1()
        elif who == "2":
            merchant_log_in_sign_out()
        elif who == "3":
            if __name__ == "__main__":
                main2()
        elif who == "4":
            if __name__ == "__main__":
                main3()
        else:
            print("\033[31mChoose either 1 / 2 / 3 / 4 only.\033[0m")
            loop = 0

who_are_you()
