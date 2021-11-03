import os, curses, time, requests, json

title =  ["""__  ______  ____    _     _____ ____   ____ _____ ____  """,
          """\ \/ /  _ \|  _ \  | |   | ____|  _ \ / ___| ____|  _ \ """,
          """ \  /| |_) | |_) | | |   |  _| | | | | |  _|  _| | |_) |""",
          """ /  \|  _ <|  __/  | |___| |___| |_| | |_| | |___|  _ < """,
          """/_/\_\_| \_\_|     |_____|_____|____/ \____|_____|_| \_\\"""]

def display_title(stdscr, msg):
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

def parse_port(fp):
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

def find_port():
    relative = '.config/ripple/rippled.cfg'
    home = os.getenv('HOME')
    filepath = os.path.join(home, relative)
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            if '[port_rpc_admin_local]' in line:
                return parse_port(fp)
            line = fp.readline()

def check_health(stdscr, addr, attempts):
    if attempts == 0:
        display_title(stdscr, msg = "Failed to connect, press any key to terminate")
        return

    data = json.dumps({"method": "server_info"})
    headers = {'content-type': "application/json"}
    r = None
    try:
        r = requests.post("http://" + addr, data=data, headers=headers)
        if r and r.status_code == 200:
            return
    except:
        pass

    time.sleep(.5)
    check_health(stdscr, addr, attempts - 1)

def wait_for_sync(stdscr, addr):
    data = json.dumps({"method": "server_info"})
    headers = {'content-type': "application/json"}
    while True:
        r = None
        try:
            r = requests.post("http://" + addr, data=data, headers=headers)
        except:
            pass

        if r and r.status_code == 200:
            response = json.loads(r.text)
            state = response["result"]["info"]["server_state"] 
            if (state == "proposing" or state == "full" or state == "validating"):
                return
            else:
                display_title(stdscr, msg="Please wait, server is syncing, this can take up to 15 minutes")

        time.sleep(10)


def connect(stdscr):
    display_title(stdscr, msg="Validator Dashboard")
    admin = find_port()
    time.sleep(1)
    display_title(stdscr, msg=("Connecting to " + admin))
    time.sleep(1)
    check_health(stdscr, admin, 4)
    display_title(stdscr, msg="Connected, starting application")
    time.sleep(1)
    wait_for_sync(stdscr, admin)
    # TODO: PUT app.start(adminPort) here
    display_title(stdscr, msg="Server is synced")

    stdscr.clear()

