import os, curses, time, requests, json

title =  ["""__  ______  ____    _     _____ ____   ____ _____ ____  """,
          """\ \/ /  _ \|  _ \  | |   | ____|  _ \ / ___| ____|  _ \ """,
          """ \  /| |_) | |_) | | |   |  _| | | | | |  _|  _| | |_) |""",
          """ /  \|  _ <|  __/  | |___| |___| |_| | |_| | |___|  _ < """,
          """/_/\_\_| \_\_|     |_____|_____|____/ \____|_____|_| \_\\"""]

def display_title(interface, msg: str):
    stdscr = interface.stdscr
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

    interface.refresh()
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

#TODO: Add this to the home screen UI
def check_health(interface, addr: str, attempts: int):
    if attempts == 0:
        display_title(interface, msg = "Failed to connect, press 'q' to terminate")
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
    check_health(interface, addr, attempts - 1)

#If not synced, returns a time to check again
def check_if_synced():
    data = json.dumps({"method": "server_info"})
    headers = {'content-type': "application/json"}
    r = None
    try:
        r = requests.post("http://" + find_port(), data=data, headers=headers)
    except:
        pass

    if r and r.status_code == 200:
        response = json.loads(r.text)
        state = response["result"]["info"]["server_state"]
        return state
    else:
        return "unable to check - 'server_info' request failed"


#TODO: Add this nice boot up animation to the Home interface
def connect(interface):
    display_title(interface, msg="Validator Dashboard")
    admin = find_port()
    time.sleep(1)
    display_title(interface, msg=("Connecting to " + admin))
    time.sleep(1)
    check_health(interface, admin, 4)
    display_title(interface, msg="Connected, starting application")
    time.sleep(1)
    check_if_synced(interface, admin)
    # TODO: PUT app.start(adminPort) here
    display_title(interface, msg="Server is synced")

    interface.stdscr.clear()

