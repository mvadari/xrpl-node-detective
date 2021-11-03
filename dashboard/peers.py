from typing import List
import requests
import json

dummy_reponse =    {
    "result" : {
      "cluster" : {},
      "peers" : [
         {
            "address" : "50.22.123.222:51235",
            "complete_ledgers" : "32570 - 51815097",
            "ledger" : "223DB74FE021AB1A4AA9E1CC588E0DBCC3FC7C080B93C01C30C246D89F951EA2",
            "load" : 7,
            "metrics" : {
               "avg_bps_recv" : "1152",
               "avg_bps_sent" : "332",
               "total_bytes_recv" : "96601",
               "total_bytes_sent" : "45322"
            },
            "public_key" : "n9LbkoB9ReSbaA9SGL317fm6CvjLcFG8hGoierLYfwiCDsEXHcP3",
            "uptime" : 1,
            "version" : "rippled-1.3.1"
         },
         {
            "address" : "212.83.147.67:51235",
            "complete_ledgers" : "51815014 - 51815040",
            "ledger" : "223DB74FE021AB1A4AA9E1CC588E0DBCC3FC7C080B93C01C30C246D89F951EA2",
            "load" : 1,
            "metrics" : {
               "avg_bps_recv" : "0",
               "avg_bps_sent" : "1490",
               "total_bytes_recv" : "18348",
               "total_bytes_sent" : "46013"
            },
            "public_key" : "n94s5V53w1g4HdEdHdUU1FVrqHTVDbcb7bt44ib9JcM3c281LoDr",
            "sanity" : "unknown",
            "uptime" : 2,
            "version" : "rippled-1.3.1"
         },
         {
            "address" : "158.69.24.50:51235",
            "complete_ledgers" : "51478098 - 51815098",
            "ledger" : "223DB74FE021AB1A4AA9E1CC588E0DBCC3FC7C080B93C01C30C246D89F951EA2",
            "load" : 55,
            "metrics" : {
               "avg_bps_recv" : "88080",
               "avg_bps_sent" : "2703",
               "total_bytes_recv" : "2786780",
               "total_bytes_sent" : "89368"
            },
            "public_key" : "n9KfEhmmdxmjJdpbpRHGJ9ezoNzdyUepA11cT71jmq1fMDsZAcSh",
            "uptime" : 3,
            "version" : "rippled-1.3.1"
         },
         {
            "address" : "[::ffff:174.64.99.193]:51235",
            "complete_ledgers" : "51813091 - 51815091",
            "latency" : 16000,
            "ledger" : "CF72319DC762355C92BDD29E4CE066CEB03FF2A077A511D586B9FD7B74F55D94",
            "load" : 325,
            "metrics" : {
               "avg_bps_recv" : "19012",
               "avg_bps_sent" : "52053",
               "total_bytes_recv" : "586809",
               "total_bytes_sent" : "1678192"
            },
            "public_key" : "n9MH4Xu8FYPPoUFs679NQp7F6epFznM7x6bF4sAJWQvKkPBUHgd3",
            "uptime" : 26,
            "version" : "rippled-1.4.0-b8"
         },
         {
            "address" : "[::ffff:94.237.45.66]:51235",
            "complete_ledgers" : "51814966 - 51815093",
            "latency" : 8773,
            "ledger" : "61CF015A709122917B001367EE81E5E0D56E485A0BCAB53785A1CB830E0F9589",
            "load" : 3522,
            "metrics" : {
               "avg_bps_recv" : "368875",
               "avg_bps_sent" : "59308",
               "total_bytes_recv" : "11558753",
               "total_bytes_sent" : "2257872"
            },
            "public_key" : "n9Lg83FYh8YDivG9TcgXhq5Y3PwunmRqVfvibd19Ko9uu3DtqLBM",
            "uptime" : 37,
            "version" : "rippled-1.3.1"
         }
      ],
      "status" : "success"
   }
}

# Returns the result of a rippled 'peers' request or None if unable to retrieve that data
# Throws if there is no node running because there's nothing at the port_rpc_admin_local
def request_peers():
    request = {
        "id": 2,
        "method": "peers"
    }

    #TODO: Actually derive the url/port from the config file (port_rpc_admin_local)
    response = requests.post('http://0.0.0.0:5005', json=request)
    if(not(response.ok)):
        return None
    else: 
        json_content = json.loads(response._content.decode('utf-8'))
        
        #TODO: For the demo, return dummy_content here
        return json_content

def format_row(column_widths, entries):
    line = ""
    for i in range(len(entries)):
        line += entries[i]
        line = line.ljust(column_widths[i], " ")
        
        if(i < len(entries) - 1):
            line += " | "

    return line

def format_response_for_display(response: dict[str, any]) -> List[str]:
    if(response == None or response['result']['peers'] == None):
        formatted_lines = ['Currently no peers are connected.']
        return formatted_lines
    else:
        peers = response['result']['peers']
        formatted_lines: List[str] = []

        formatted_lines.append(f"Total peers: {len(peers)}")
        formatted_lines.append("")

        column_widths = [40, 80, 120]
        header = ['name/ip address', 'status', 'completed ledgers']
        formatted_lines.append(format_row(column_widths, header))
        formatted_lines.append("".ljust(column_widths[-1], '-'))
        for peer in peers:
            entries = []
            if(peer.get("name") != None):
                entries.append(peer.get("name"))
            else: 
                entries.append(peer.get("address"))

            if(peer.get("status")):
                entries.append(peer.get("status"))
            else:
                entries.append("No status found")

            entries.append(peer.get("complete_ledgers"))

            formatted_lines.append(format_row(column_widths, entries))

        return formatted_lines

def get_formatted_peers():
    try:
        return format_response_for_display(request_peers())
    except:
        return ["Error: Unable to connect to the rippled local admin rpc port to check for peers. Check if your node is running."]