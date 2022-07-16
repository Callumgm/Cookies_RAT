import os

def main():
    try:
        try:
            os.system(f"C:\Users\{os.getlogin()}\AppData\Local\Programs\Python\Python39\python.exe -m pip install --upgrade pip")
            os.system("pip install wheel")
        except: pass

        with open ('requirements.txt', 'r') as f: requirements = f.read().splitlines()

        for req in requirements:
            os.system('pip install ' + req)

    except Exception as e:
        print(e)
        print('Error: Could not install requirements')
        input('\n\nPress enter to exit')
        exit(1)


main()
print('Success: Requirements installed')
input('\n\nPress enter to exit')