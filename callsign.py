import curses
import requests

instructions = 'Enter an FCC callsign to lookup.'
menu = ['Callsign', 'Exit']

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    x_start = w // 2 - len(instructions) // 2
    y_start = h // 2 - len(menu) // 2

    stdscr.addstr(y_start, x_start, instructions)

    x_start += 4

    for idx, row in enumerate(menu):
        x = x_start
        y = y_start + idx + 1

        if idx == selected_row_idx:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()

def build_output_callsign(data, indent=0, json_lines=None):
    if json_lines is None:
        json_lines = []
    for k, v in data.items():
        if isinstance (v, dict):
            json_lines.append(" " * indent + k)
            build_output_callsign(v, indent + 4, json_lines)
        else:
            kv_pair = f"{k} : {v}"
            json_lines.append(" " * indent + kv_pair)
    return json_lines
    
def output_callsign(stdscr, callsign):
    call_data = lookup_callsign(callsign)

    h, w = stdscr.getmaxyx()
    if isinstance(call_data, int):
        x = w // 2 - len(call_data) // 2
        y = h // 2 - 1 // 2
        stdscr.addstr(y, x, "http status code from callook.info : " + call_data)
        stdscr.refresh()
    else:
        y = h // 20
        x = w // 5
        page_size = h - 4
        current_page = 0

        json_callsign_build = build_output_callsign(call_data)

        while True:
            stdscr.clear()

            # calculate start and end for current page size
            start_idx = current_page * page_size
            end_idx = min(start_idx + page_size, len(json_callsign_build))

            # print it out
            y = 0
            for i in range(start_idx, end_idx):
                line = json_callsign_build[i]
                # ensure it fits
                #if len(line) >= w:
                #    line = line[:w-1]
                stdscr.addstr(y, x, line)
                y += 1

            # show pagination and controls
            page_info = f"Page {current_page + 1} of {len(json_callsign_build) // page_size + 1}"
            stdscr.addstr(h - 2, w // 2 - len(page_info) // 2, page_info)

            controls = "Press 'n' for next, 'p' for previous, or 'q' to quit."
            stdscr.addstr(h - 1, w // 2 - len(controls) // 2, controls)

            stdscr.refresh()

            key = stdscr.getch()

            if key == ord('q'):
                break
            elif key == ord('n') and end_idx < len(json_callsign_build):
                current_page += 1
            elif key == ord('p') and current_page > 0:
                current_page -= 1

def lookup_callsign(callsign):
    apiGet = 'https://callook.info/' + callsign + '/json'
    try:
        r = requests.get(apiGet)
        output = r.json()
        return output
    except:
        return(r.status_code)

def main(stdscr):
    # turn off blinking cursor
    curses.curs_set(0)
    # set up initial state
    current_row_idx = 0
    # initial rendering of menu
    print_menu(stdscr, current_row_idx)
    # main ui loop to handle user input
    while True:
        key = stdscr.getch() # get a single char from the user
        # check for key presses
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]: # 10 and 13 are return/enter keys
            if menu[current_row_idx] == 'Exit':
                break

            # do it lady
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            
            selected_option_msg = f"{menu[current_row_idx]} : "
            x = w // 2 - len(selected_option_msg) // 2
            y = h // 2
            stdscr.addstr(y, x, selected_option_msg)
            # enable echo
            curses.echo()
            stdscr.move(y, x + len(selected_option_msg))
            callsign = stdscr.getstr().decode(encoding="utf-8")
            # disable echo
            curses.noecho()
            stdscr.clear()
            # output callsign
            output_callsign(stdscr, callsign)

        print_menu(stdscr, current_row_idx)

if __name__ == "__main__":
    curses.wrapper(main)
            

