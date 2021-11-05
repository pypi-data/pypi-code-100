import curses
import curses.textpad
import curses.ascii
from threading import Thread
from PyInquirer import style_from_dict, prompt, print_json
import os

from .api import Gitlab, Project, Variable

class Screen(object):
    # https://github.com/mingrammer/python-curses-scroll-example/blob/master/tui.py
    UP = -1
    DOWN = 1

    def __init__(self, gl : Gitlab):
        self.window = None

        self.width = 0
        self.height = 0

        self.init_curses()
        self._gl = gl

        self.items = []

        self.max_lines = curses.LINES
        self.top = 0
        self.bottom = len(self.items)
        self.current = 0
        self.page = self.bottom // self.max_lines

    def init_curses(self):
        """Setup the curses"""
        self.window = curses.initscr()
        self.window.keypad(True)
        self.window.nodelay(True)

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.current = curses.color_pair(2)

        self.height, self.width = self.window.getmaxyx()

    def run(self):
        """Continue running the TUI until get interrupted"""
        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass
        self._gl.stop()
        curses.endwin()

    def input_stream(self):
        self._gl.stop()
        raise NotImplementedError

    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""
        # next cursor position after scrolling
        next_line = self.current + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        if (direction == self.DOWN) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom):
            self.top += direction
            return
        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        # Scroll down
        # next cursor position is above max lines, and absolute position of next cursor could not touch the bottom
        if (direction == self.DOWN) and (next_line < self.max_lines) and (self.top + next_line < self.bottom):
            self.current = next_line
            return

    def paging(self, direction):
        """Paging the window when pressing left/right arrow keys"""
        current_page = (self.top + self.current) // self.max_lines
        next_page = current_page + direction
        # The last page may have fewer items than max lines,
        # so we should adjust the current cursor position as maximum item count on last page
        if next_page == self.page:
            self.current = min(self.current, self.bottom % self.max_lines - 1)

        # Page up
        # if current page is not a first page, page up is possible
        # top position can not be negative, so if top position is going to be negative, we should set it as 0
        if (direction == self.UP) and (current_page > 0):
            self.top = max(0, self.top - self.max_lines)
            return
        # Page down
        # if current page is not a last page, page down is possible
        if (direction == self.DOWN) and (current_page < self.page):
            self.top += self.max_lines
            return

    def display(self):
        """Display the items on window"""
        self.window.erase()
        for idx, item in enumerate(self.items[self.top:self.top + self.max_lines]):
            # Highlight the current cursor line
            if idx == self.current:
                self.window.addstr(idx, 0, item, curses.color_pair(2))
            else:
                self.window.addstr(idx, 0, item, curses.color_pair(1))
        self.window.refresh()

    # def input_text(self, command_help : str = None):
    #     curses.curs_set(1)
    #     curses.echo()
    #     self.window.nodelay(False)
    #     self.window.clear()
    #     if command_help != None:
    #         self.window.addstr(command_help)
    #     self.window.refresh()
    #     input_text = self.window.getstr()
    #     self.window.clear()
    #     self.window.nodelay(True)
    #     curses.noecho()
    #     curses.curs_set(0)
    #     return input_text

class ProjectsScreen(Screen):
    def __init__(self, gl: Gitlab):
        super().__init__(gl)

    def input_stream(self):
        selector = {}
        while True:
            self.display()

            ch = self.window.getch()
            if ch == curses.KEY_UP:
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif ch == curses.KEY_LEFT:
                self.paging(self.UP)
            elif ch == curses.KEY_RIGHT:
                self.paging(self.DOWN)
            elif ch == curses.ascii.ESC:
                self._gl.stop()
                break
            elif ch in [curses.KEY_ENTER, curses.ascii.NL] and len(list(self._gl.projects.keys())) > 0:
                VariablesScreen(self._gl, selector[self.current + self.top]["ref"]).run()

            for e, obj in enumerate(list(self._gl.projects.keys())):
                selector[e] = {"ref": self._gl.projects[obj], "display": f"{' ' * (len(str(len(self._gl.projects))) - len(str(e)))}{e}.- {self._gl.projects[obj].project_name}"}

            if len(list(selector.keys())) > 0:
                self.items = [selector[e]["display"] for e in list(selector.keys())]
            else:
                self.items = ["Fetching projects..."]

            self.bottom = len(self.items)
            self.page = self.bottom // self.max_lines

class VariablesScreen(Screen):
    def __init__(self, gl: Gitlab, project : Project):
        super().__init__(gl)
        self.__project = project
        self.__active = True
        self.__fetched_once = False
        self.__vars = {}
    
    def input_stream(self):
        Thread(target = self.fetch_vars).start()
        self.__selector = {}
        while True:
            self.display()

            ch = self.window.getch()
            if ch == curses.KEY_UP:
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif ch == curses.KEY_LEFT:
                self.paging(self.UP)
            elif ch == curses.KEY_RIGHT:
                self.paging(self.DOWN)
            elif ch == curses.ascii.ESC:
                self.__active = False
                break
            elif ch in [curses.KEY_ENTER, curses.ascii.NL] and len(list(self.__vars.keys())) > 0:
                VariableEditorScreen(self._gl, self.__selector[self.current + self.top]["ref"]).run()
            elif ch == ord('c'):
                self.create_variable()
            elif ch == ord('x'):
                while True:
                    self.create_variable()
            elif ch == ord('d'):
                self.delete_variable(self.current + self.top)

            for e, obj in enumerate(list(self.__vars.keys())):
                self.__selector[e] = {"ref": self.__vars[obj], "display": f"{' ' * (len(str(len(self.__vars))) - len(str(e)))}{e}.- {self.__vars[obj].name} ({self.__vars[obj].present_envs})"}
            
            self.__vars = self.__project.variables
            if len(list(self.__vars.keys())) > 0:
                for e in list(self.__selector.keys()):
                    if len(list(self.__selector[e]["ref"].envs.keys())) == 0:
                        del self.__selector[e]
                        if self.current + self.top == e:
                            self.scroll(self.UP)
                self.items = [self.__selector[e]["display"] for e in list(self.__selector.keys())]
            elif not self.__fetched_once:
                self.items = ["Fetching variables..."]
            else:
                self.items = ["There are no variables"]
            
            self.bottom = len(self.items)
            self.page = self.bottom // self.max_lines
    
    def fetch_vars(self):
        while self.__active:
            self.__project.fetch_project().join()
            self.__fetched_once = True
    
    def create_variable(self):
        curses.endwin()
        os.system("cls||clear")
        questions = [
            {
                'type': 'input',
                'name': 'var_name',
                'message': 'Variable name',
            },
            {
                'type': 'input',
                'name': 'var_env',
                'message': 'Variable environment',
            },
            {
                'type': 'input',
                'name': 'var_value',
                'message': 'Variable value',
            },
        ]
        var_data = prompt(questions = questions)
        os.system("cls||clear")
        if var_data != {}:
            Thread(target = self.__project.create_variable, kwargs = var_data).start()
    
    def delete_variable(self, selector_index : int):
        curses.endwin()
        os.system("cls||clear")
        questions = [
            {
                'type': 'confirm',
                'name': 'confirm',
                'message': f"Delete variable {self.__selector[selector_index]['ref'].name}?",
                "default": True
            }
        ]
        conf = prompt(questions=questions)
        os.system("cls||clear")
        if "confirm" in conf and conf["confirm"]:
            self.__selector[selector_index]["ref"].full_delete()
            del self.__selector[selector_index]
            self.scroll(self.UP)

class VariableEditorScreen(Screen):
    def __init__(self, gl: Gitlab, variable : Variable):
        super().__init__(gl)
        self.__variable = variable
    
    def input_stream(self):
        self.__selector = {}
        while True:
            self.display()

            ch = self.window.getch()
            if ch == curses.KEY_UP:
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif ch == curses.KEY_LEFT:
                self.paging(self.UP)
            elif ch == curses.KEY_RIGHT:
                self.paging(self.DOWN)
            elif ch == curses.ascii.ESC:
                break
            elif ch == ord('c'):
                self.create_variable_env()
            elif ch == ord('x'):
                while True:
                    self.create_variable_env()
            elif ch == ord('d'):
                selector_index = self.current + self.top
                if self.delete_environment(selector_index):
                    del self.__selector[selector_index]
                    return
                self.__selector = {}
                self.items = []
                self.scroll(self.UP)
            elif ch == curses.ascii.NL:
                selector_index = self.current + self.top
                curses.endwin()
                os.system("cls||clear")
                questions = [
                    {
                        'type': 'input',
                        'name': 'edit',
                        'message': f"Edit value for {self.__variable.name} on environment {self.__selector[selector_index]['ref']}\n",
                        'default': self.__variable.get_env_value(self.__selector[selector_index]["ref"]),
                    }
                ]
                answer = prompt(questions)
                os.system("cls||clear")
                if answer != {}:
                    Thread(target = self.__variable.edit, kwargs = {"env": self.__selector[selector_index]['ref'], "new_value": answer["edit"]}).start()

            for e, obj in enumerate(list(self.__variable.envs.keys())):
                self.__selector[e] = {"ref": obj, "display": f"{obj} -> {self.__variable.get_env_value(obj)}"}

            if len(list(self.__variable.envs.keys())) > 0:
                self.items = [self.__selector[e]["display"] for e in list(self.__selector.keys())]
            else:
                self.items = ["Fetching environments..."]
            
            self.bottom = len(self.items)
            self.page = self.bottom // self.max_lines
    
    def create_variable_env(self):
        curses.endwin()
        os.system("cls||clear")
        questions = [
            {
                'type': 'input',
                'name': 'var_env',
                'message': 'Variable environment',
            },
            {
                'type': 'input',
                'name': 'var_value',
                'message': 'Variable value',
            },
        ]
        var_data = prompt(questions = questions)
        os.system("cls||clear")
        if var_data != {}:
            Thread(target = self.__variable.create_env, kwargs = var_data).start()
    
    def delete_environment(self, selector_index : int):
        curses.endwin()
        os.system("cls||clear")
        env = self.__selector[selector_index]["ref"]
        questions = [
            {
                'type': 'confirm',
                'name': 'confirm',
                'message': f"Delete environment {env} from variable {self.__variable.name}?",
                "default": True
            }
        ]
        conf = prompt(questions=questions)
        os.system("cls||clear")
        if "confirm" in conf and conf["confirm"]:
            return self.__variable.delete_env(env)
        return False