import base64
import os
import platform
import subprocess
from time import sleep

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from lib.Color import *


class CustomEncryption:

    NUM: str = "1"

    @classmethod
    def clean(cls, type_os):
        """
        :param type_os:
        :return
        Implement platform-specific code to clear the console
        """
        if type_os == "Windows":
            # Windows-specific code
            os.system("cls")
        elif type_os == "Linux" or type_os == "Darwin":
            # Linux-Darwin code
            os.system("clear")
        else:
            # Handle other operating systems
            print(Color.Error("This is an unsupported operating system."))

    @classmethod
    def get_serial_number(cls):
        """ Implement getting the serial number """
        command = 'wmic bios get serialnumber'
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
            serial_number = result.decode().split('\n')[1].strip()
            return serial_number
        except subprocess.CalledProcessError:
            return None

    @classmethod
    def rewrite_file(cls, file_name, new_content):
        """Implement rewriting a file"""
        with open(file_name, 'w') as file:
            file.write(new_content)

    @classmethod
    def generate_key(cls, password, salt):
        """Generate a key from the provided password and salt."""
        backend = default_backend()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )
        key = kdf.derive(password)
        return key

    @classmethod
    def encrypt_text(cls, text_encrypt, password, key_file_name, is_save_file=True):
        """Encrypt the given text using the provided password."""

        salt: bytes = os.urandom(16)
        key = cls.generate_key(password.encode(), salt)

        cipher_suite = Fernet(base64.urlsafe_b64encode(key))
        encrypted_text = cipher_suite.encrypt(text_encrypt.encode())
        if is_save_file:
            cls.save_password_salt_to_file(salt, f"{os.getcwd()}/{key_file_name}")
        return encrypted_text, salt

    @classmethod
    def decrypt_text(cls, encrypted_text, password, salt):
        """Decrypt the given encrypted text using the provided password and salt."""
        key = cls.generate_key(password.encode(), salt)

        cipher_suite = Fernet(base64.urlsafe_b64encode(key))
        decrypted_text = cipher_suite.decrypt(encrypted_text)
        return decrypted_text.decode()

    @classmethod
    def encrypt_file(cls, origin_file: str, password: str, key_file_name: str):
        """Encrypt the contents of the given file using the provided password."""
        with open(origin_file, 'rb') as file:
            plain_data = file.read()

        salt = os.urandom(16)
        key = cls.generate_key(password.encode(), salt)

        cipher_suite = Fernet(base64.urlsafe_b64encode(key))
        encrypted_data = cipher_suite.encrypt(plain_data)

        encrypted_file_path = origin_file + '.enc'
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        cls.save_password_salt_to_file(salt, key_file_name)
        return encrypted_file_path

    @classmethod
    def decrypt_file(cls, encrypted_file_path, key_file_name):
        """Decrypt the contents of the given encrypted file using the provided password and salt."""
        password, salt = cls.load_password_salt_from_file(file_path=key_file_name)

        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        key = cls.generate_key(password.encode(), salt)

        cipher_suite = Fernet(base64.urlsafe_b64encode(key))
        decrypted_data = cipher_suite.decrypt(encrypted_data)

        decrypted_file_path = encrypted_file_path[:-4]  # Remove the '.enc' extension
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

    @classmethod
    def save_password_salt_to_file(cls, salt, file_path):
        """Save the password and salt to a file."""
        with open(f"{file_path}.i9x", 'wb') as file:
            file.write(salt)

    @classmethod
    def load_password_salt_from_file(cls, file_path):
        """Load the password and salt from a file."""

        with open(f"{file_path}.i9x", 'rb') as file:
            password = input("Please Enter The password : ")
            salt = file.read()
            return password, salt

    @classmethod
    def main_page(cls):
        print(Color.banner+"\t\t\t╔══════════════════════════════╗"+Color.Reset)
        print(Color.banner+"\t\t\t║        Main Menu             ║"+Color.Reset)
        print(Color.banner+"\t\t\t╠══════════════════════════════╣"+Color.Reset)
        print(Color.banner+"\t\t\t║ 1. Encrypt Text              ║"+Color.Reset)
        print(Color.banner+"\t\t\t║ 2. Decrypt Text              ║"+Color.Reset)
        print(Color.banner+"\t\t\t║ 3. Encrypt File              ║"+Color.Reset)
        print(Color.banner+"\t\t\t║ 4. Decrypt File              ║"+Color.Reset)
        print(Color.banner+"\t\t\t║ 5. exit                      ║" + Color.Reset)
        print(Color.banner+"\t\t\t╠══════════════════════════════╣\n"+Color.Reset)

    @classmethod
    def main(cls):

        if cls.NUM == "1":

            cls.clean("Linux")

            print("\n")
            cls.main_page()
            print("\n")
            Num = input("Choose>> ")
            if Num == "exit":
                cls.NUM = "0"
            if Num == "1":
                # Encrypt Text
                cls.clean("Linux")

                print(Color.Success(" Enter the password: "))
                password = input()
                print(f"\n{Fore.GREEN}")
                plain_text = input("\n[*] Enter the text to be encrypted: ")
                print(f"\n{Fore.GREEN}")
                print(Color.Success("[*] Enter Name File For Save password and salt: "))
                NameSaveSalat = input()
                file_name_encrypt = input("\n[*] please Enter New Name File for save text Encrypt: ")
                print(f"\n{Fore.RESET}")

                if password == "" or plain_text == "" or NameSaveSalat == "" or file_name_encrypt == "":
                    print(f"\n{Fore.RED}")
                    print("[-] Please Check Data ")
                    sleep(2)
                    cls.main()

                encrypted_text, salt = cls.encrypt_text(
                    plain_text,
                    password,
                    NameSaveSalat
                )

                with open(f"{file_name_encrypt}.txt", 'wb') as file:
                    file.write(encrypted_text)  # Save the encrypted text
                print(f"\n{Fore.GREEN}")
                print(f"[+] Text Encrypt saved to file:{file_name_encrypt}.txt")

                print(f"[+] Password and salt saved to file:{NameSaveSalat}.i9x")
                print(f"\n{Fore.RESET}")
                cls.main()

            elif Num == '2':
                print(f"\n{Fore.GREEN}")
                file_name = input("[*] Please Enter Name File txt Encrypt: ".title())
                file_name_key = input("[*] Please Enter Name File Key: ".title())

                if file_name == "" or file_name_key == "":
                    print(f"\n{Fore.RED}")
                    print("[-] Please Check Data ")
                    cls.main()
                password, salt = cls.load_password_salt_from_file(
                    file_path=file_name_key,
                )
                try:
                    with open(f"{file_name}.txt", 'rb') as file:
                        encrypted_text = file.read()
                except FileNotFoundError:
                    print(f"\n{Fore.RED}")
                    print(f"[-] The {file_name}.txt Not Valid")

                except Exception as e:
                    print(f"{Fore.RED}")
                    print(f"[-] An unexpected error occurred: {e}")
                try:
                    clean_txt = cls.decrypt_text(
                        password=password,
                        salt=salt,
                        encrypted_text=encrypted_text
                    )
                    cls.rewrite_file(
                        file_name=f"{file_name}.txt",
                        new_content=clean_txt
                    )
                except ExceptionGroup:
                    print(f"\n{Fore.RED}")
                    print("[-] password Error !".title())

            elif Num == "3":
                print(f"\n{Fore.GREEN}")
                password: str = input("\n[*] Enter the password:  ".title())
                file_path: str = input("\n[*] Enter the path of the file to be encrypted: ")
                file_name_key: str = input("\n[*] Please Enter Name File Key: ")

                try:

                    encrypted_file_path = cls.encrypt_file(
                        origin_file=file_path,
                        password=password,
                        key_file_name=file_name_key)

                    print(f"\n{Fore.GREEN}")
                    print(f"[+] File encrypted and saved as: {encrypted_file_path}")
                    print(f"\n{Fore.RESET}")

                except FileNotFoundError:
                    print(f"\n{Fore.RED}")
                    print(f"[-] The {file_path} Not Valid")

            elif Num == "4":
                print(f"\n{Fore.GREEN}")
                file_name = input("[*] Please Enter Name File  Encrypt: ".title())
                file_name_key = input("[*] Please Enter Name File Key: ".title())
                if file_name == "" or file_name_key == "":
                    print(Color.Error("[-] Please Check Data "))
                    exit(0)

                try:
                    cls.decrypt_file(
                        file_name,
                        file_name_key,
                    )
                    print("\n")
                    print(Color.Success("[+] Done Decrypt File .".title()))
                except ExceptionGroup:
                    print("\n")
                    print(Color.Error("[-] password Error !".title()))

            if Num != "exit":
                print("\n")
                print(Color.Error("[-] Invalid choice. !".title()))




        else:
            cls.NUM = "1"
            return 0