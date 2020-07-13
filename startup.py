import os
if 'config.json' not in os.listdir('.'):
    open('config.json', 'x').close()
    config = open('config.json', "w")
    config.write('{"password": "Test"}')
    print("config.json created.\nDefault password as: Test (case sensitive).")
    open('config.json').read()
    config.close()

if __name__ == "__main__":
    os.system("Docker build -t ryankeys/docker-nas:latest .")
    os.system(
        "Docker run -p 5000:5000 --rm --name flask-container ryankeys/docker-nas:latest")
