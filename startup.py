import os
if 'config.json' not in os.listdir('.'):
    open('config.json', 'x').close()
    config = open('config.json', "w")
    config.write('{"password": "Test"}')
    print("config.json created.\nDefault password as: Test (case sensitive).")
    open('config.json').read()
    config.close()

if __name__ == "__main__":
    os.system("docker build -t flask-image .")
    os.system("docker run -p 5000:5000 --rm --name flask-container flask-image")
