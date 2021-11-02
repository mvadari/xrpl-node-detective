import os, curses, time, requests, json

title =  ["""__  ______  ____    _     _____ ____   ____ _____ ____  """,
          """\ \/ /  _ \|  _ \  | |   | ____|  _ \ / ___| ____|  _ \ """,
          """ \  /| |_) | |_) | | |   |  _| | | | | |  _|  _| | |_) |""",
          """ /  \|  _ <|  __/  | |___| |___| |_| | |_| | |___|  _ < """,
          """/_/\_\_| \_\_|     |_____|_____|____/ \____|_____|_| \_\\"""]

def displayTitle(stdscr, msg):
    stdscr.clear()

    for i,line in enumerate(title): 
        stdscr.addstr(
            curses.LINES // 2 - len(title) // 2 + i,
            curses.COLS // 2 - len(line) // 2,
            line,
        )

    stdscr.addstr(
        curses.LINES // 2 - len(title) // 2 + len(title),
        curses.COLS // 2 - len(msg) // 2,
        msg,
        curses.color_pair(85)
    )

    stdscr.refresh()
    curses.curs_set(0)

def parsePort(fp):
    line = fp.readline()
    port = None
    ip = None
    while line:
        if 'port' in line and len(line.split('=')) > 1:
            port = line.split('=')[1].strip()
        elif 'ip' in line:
            ip = line.split('=')[1].strip()

        if port and ip:
            return ip + ":" + port

        line = fp.readline()

def findPort():
    relative = '.config/ripple/rippled.cfg'
    home = os.getenv('HOME')
    filepath = os.path.join(home, relative)
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            if '[port_rpc_admin_local]' in line:
                return parsePort(fp)
            line = fp.readline()

def checkHealth(stdscr, addr, attempts):
    if attempts == 0:
        displayTitle(stdscr, msg = "Failed to connect, press any key to terminate")
        return

    data = json.dumps({"method": "server_info"})
    headers = {'content-type': "application/json"}
    r = None
    try:
        r = requests.post("http://" + addr, data=data, headers=headers)
        print(r.status_code)
        if r and r.status_code == 200:
            return
    except:
        None

    time.sleep(.5)
    checkHealth(stdscr, addr, attempts - 1)


def connect(stdscr):
    displayTitle(stdscr, msg="Validator Dashboard")
    adminPort = findPort()
    time.sleep(1)
    displayTitle(stdscr, msg=("Connecting to " + adminPort))
    time.sleep(1)
    checkHealth(stdscr, adminPort, 4)
    displayTitle(stdscr, msg="Connected, starting application")
    time.sleep(1)
    stdscr.clear()
    # TODO: PUT app.start(adminPort) here

