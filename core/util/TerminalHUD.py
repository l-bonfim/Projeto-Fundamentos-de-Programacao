import sys
import os
import time
import threading
import asyncio
from typing import List, Dict, Any, Callable, Optional, Union

# Windows vs Unix compatibility
try:
    import msvcrt  # Windows
    IS_WINDOWS = True
except ImportError:
    import select
    import termios
    import tty
    IS_WINDOWS = False

class TerminalHUD:
    """
    TerminalHUD - A framework for creating HUD interfaces in terminal
    Exact replica of Node.js version in Python
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {}
        
        self.loading = False
        self.numbered_menus = config.get('numbered_menus', False)
        self.highlight_color = config.get('highlight_color', 'cyan')
        self.last_menu_generator = None
        self.last_selected_index = 0
        self.loading_thread = None
        self.stop_loading_flag = False
        self.original_terminal_settings = None

    def get_color_code(self, color: str) -> str:
        colors = {
            'red': '\033[91m',
            'green': '\033[92m', 
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m'
        }
        return colors.get(color, '\033[96m')

    def reset_color(self) -> str:
        return '\033[0m'

    def clear_screen(self):
        """Clear the entire terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def start_loading(self):
        self.loading = True
        self.stop_loading_flag = False
        
        def loading_animation():
            i = 0
            while not self.stop_loading_flag:
                sys.stdout.write('\r\033[K')  # Clear line
                sys.stdout.write(f"⏳ Loading{'.' * i}")
                sys.stdout.flush()
                i = (i + 1) % 4
                time.sleep(0.5)
        
        self.loading_thread = threading.Thread(target=loading_animation)
        self.loading_thread.daemon = True
        self.loading_thread.start()

    def stop_loading(self):
        self.loading = False
        self.stop_loading_flag = True
        if self.loading_thread and self.loading_thread.is_alive():
            self.loading_thread.join(timeout=0.5)
        sys.stdout.write('\r\033[K')  # Clear loading line
        sys.stdout.flush()

    async def ask(self, question: str, config: Dict[str, Any] = None) -> str:
        if config is None:
            config = {}
        
        if config.get('options'):
            if self.numbered_menus:
                return await self.display_menu_from_options(question, config['options'], config)
            else:
                return await self.display_menu_with_arrows(question, config['options'], config)
        
        # Simple question input
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: input(f"\n{question}"))

    async def display_menu_with_arrows(self, question: str, options: List[Any] = None, 
                                     config: Dict[str, Any] = None, initial_index: int = 0) -> str:
        if options is None:
            options = []
        if config is None:
            config = {}
        
        lines = self.normalize_options(options)
        line, col = self.get_coordinates_from_linear_index(lines, initial_index)

        def render_menu():
            # Clear screen and position cursor at top
            self.clear_screen()
            
            # Print question
            if question:
                print(f"{question}\n")
            
            # Print menu options
            for i, line_opts in enumerate(lines):
                line_str = ""
                for j, opt in enumerate(line_opts):
                    text = opt if isinstance(opt, str) else opt.get('name', str(opt))
                    
                    if i == line and j == col:
                        # Selected option: colored text with arrow
                        color = self.get_color_code(self.highlight_color)
                        line_str += f"{color}→ {text}{self.reset_color()}"
                    else:
                        # Normal option
                        line_str += f"  {text}"
                    
                    if j < len(line_opts) - 1:
                        line_str += "   "  # Space between options
                print(line_str)
            
            # Print instructions
            print(f"\nUse arrow keys to navigate, Enter to select")
            print(f"Selected: Line {line + 1}, Option {col + 1}")

        # Set up terminal for raw input
        self._setup_terminal()
        
        try:
            # Initial render
            render_menu()
            
            while True:
                key = self._get_key()
                
                old_line, old_col = line, col
                
                # Handle navigation
                if key == 'up': 
                    if line > 0:
                        line -= 1
                    # Ensure column is within bounds for the new line
                    if col >= len(lines[line]):
                        col = len(lines[line]) - 1
                elif key == 'down':
                    if line < len(lines) - 1:
                        line += 1
                    # Ensure column is within bounds for the new line
                    if col >= len(lines[line]):
                        col = len(lines[line]) - 1
                elif key == 'left':
                    if col > 0:
                        col -= 1
                elif key == 'right':
                    if col < len(lines[line]) - 1:
                        col += 1
                elif key == 'enter':
                    self.last_selected_index = self.get_linear_index_from_coordinates(lines, line, col)
                    selected = lines[line][col]
                    
                    # Handle action
                    if isinstance(selected, dict) and selected.get('action'):
                        action = selected['action']
                        if asyncio.iscoroutinefunction(action):
                            await action()
                        else:
                            action()
                    
                    result = selected if isinstance(selected, str) else selected.get('name', str(selected))
                    return result
                elif key == 'ctrl_c':
                    raise KeyboardInterrupt
                
                # Only re-render if selection changed
                if old_line != line or old_col != col:
                    render_menu()
                
        finally:
            self._restore_terminal()

    async def display_menu_from_options(self, question: str, options: List[Any], 
                                      config: Dict[str, Any] = None) -> str:
        if not self.numbered_menus:
            return await self.display_menu_with_arrows(question, options, config)

        if config is None:
            config = {}

        self.clear_screen()
            
        if question:
            print(f"{question}\n")

        option_map = {}
        index = 1
        
        def print_option(opt):
            nonlocal index
            text = opt if isinstance(opt, str) else opt.get('name', str(opt))
            print(f"{index}. {text}")
            option_map[index] = opt
            index += 1

        for opt in options:
            if isinstance(opt, list):
                for sub_opt in opt:
                    print_option(sub_opt)
            else:
                print_option(opt)

        while True:
            try:
                choice_input = await self.ask('\nChoose an option: ')
                if not choice_input:
                    continue
                choice = int(choice_input)
                selected = option_map.get(choice)
                
                if not selected:
                    print('Invalid option, try again.')
                    return await self.display_menu_from_options(question, options, config)

                if isinstance(selected, str):
                    return selected
                
                if selected.get('action'):
                    action = selected['action']
                    if asyncio.iscoroutinefunction(action):
                        await action()
                    else:
                        action()
                
                return selected.get('name', str(selected))
                
            except ValueError:
                print('Please enter a valid number.')

    def normalize_options(self, options: List[Any]) -> List[List[Any]]:
        result = []
        for opt in options:
            if isinstance(opt, list):
                normalized_line = []
                for item in opt:
                    if isinstance(item, str):
                        normalized_line.append({'name': item})
                    else:
                        normalized_line.append(item)
                result.append(normalized_line)
            elif isinstance(opt, dict) and opt.get('type') == 'options':
                normalized_line = []
                for item in opt.get('value', []):
                    if isinstance(item, str):
                        normalized_line.append({'name': item})
                    else:
                        normalized_line.append(item)
                result.append(normalized_line)
            else:
                if isinstance(opt, str):
                    result.append([{'name': opt}])
                else:
                    result.append([opt])
        return result

    def get_coordinates_from_linear_index(self, lines: List[List[Any]], index: int) -> tuple:
        count = 0
        for i, line in enumerate(lines):
            if index < count + len(line):
                return i, index - count
            count += len(line)
        return len(lines) - 1, len(lines[-1]) - 1

    def get_linear_index_from_coordinates(self, lines: List[List[Any]], line: int, col: int) -> int:
        return sum(len(l) for l in lines[:line]) + col

    async def display_menu(self, menu_generator: Callable, config: Dict[str, Any] = None) -> str:
        if config is None:
            config = {}
        
        props = config.get('props', {})
        clear_screen = config.get('clear_screen', True)
        alert = config.get('alert')
        alert_emoji = config.get('alert_emoji', '⚠️')
        initial_selected_index = config.get('initial_selected_index', 0)
        selected_inc = config.get('selected_inc', 0)
        
        if clear_screen:
            self.clear_screen()
        
        self.start_loading()
        
        # Get menu data
        menu_result = menu_generator(props)
        if asyncio.iscoroutine(menu_result):
            menu = await menu_result
        else:
            menu = menu_result
            
        self.stop_loading()

        if alert:
            print(f"{alert_emoji}  {alert}\n")

        # Get title
        menu_title = menu.get('title', '')
        if asyncio.iscoroutine(menu_title):
            menu_title = await menu_title

        # Calculate initial index
        if menu_generator == self.last_menu_generator:
            initial_index = self.last_selected_index
        else:
            initial_index = initial_selected_index

        if selected_inc:
            initial_index += selected_inc
        
        self.last_menu_generator = menu_generator

        if self.numbered_menus:
            return await self.display_numbered_menu(menu_title, menu.get('options', []))
        else:
            return await self.display_menu_with_arrows(menu_title, menu.get('options', []), 
                                                     {'clear': True}, initial_index)

    async def display_numbered_menu(self, title: str, options: List[Any]) -> str:
        self.clear_screen()
        if title:
            print(f"{title}\n")

        option_map = {}
        index = 1
        
        for opt in options:
            if isinstance(opt, dict) and opt.get('type') == 'options' and isinstance(opt.get('value'), list):
                opt_values = opt['value']
                option_texts = []
                for i, item in enumerate(opt_values):
                    item_name = item.get('name', str(item))
                    option_texts.append(f"{index + i}. {item_name}")
                    option_map[index + i] = item
                print(" ".join(option_texts))
                index += len(opt_values)
            elif isinstance(opt, dict) and opt.get('type') == 'text' and 'value' in opt:
                print(opt['value'])
            elif isinstance(opt, dict) and 'name' in opt:
                print(f"{index}. {opt['name']}")
                option_map[index] = opt
                index += 1

        while True:
            try:
                choice_input = await self.ask('\nChoose an option: ')
                if not choice_input:
                    continue
                choice = int(choice_input)
                selected = option_map.get(choice)

                if not selected:
                    print('Invalid option, try again.')
                    return await self.display_numbered_menu(title, options)

                if selected.get('action'):
                    action = selected['action']
                    if asyncio.iscoroutinefunction(action):
                        await action()
                    else:
                        action()

                return selected.get('name', str(selected))

            except ValueError:
                print('Please enter a valid number.')

    async def press_wait(self):
        print('\nPress any key to continue...')
        self._setup_terminal()
        try:
            self._get_key()  # Wait for any key
        finally:
            self._restore_terminal()

    def close(self):
        self._restore_terminal()

    # Terminal control methods
    def _setup_terminal(self):
        if not IS_WINDOWS and sys.stdin.isatty():
            self.original_terminal_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())

    def _restore_terminal(self):
        if not IS_WINDOWS and self.original_terminal_settings and sys.stdin.isatty():
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.original_terminal_settings)
            self.original_terminal_settings = None

    def _get_key(self) -> str:
        if IS_WINDOWS:
            ch = msvcrt.getch()
            if ch == b'\xe0':  # Arrow keys
                ch = msvcrt.getch()
                if ch == b'H': return 'up'
                if ch == b'P': return 'down'
                if ch == b'K': return 'left'
                if ch == b'M': return 'right'
            elif ch == b'\r': return 'enter'
            elif ch == b'\x03': return 'ctrl_c'
            return 'unknown'
        else:
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # Escape sequence
                ch += sys.stdin.read(2)
                if ch == '\x1b[A': return 'up'
                if ch == '\x1b[B': return 'down'
                if ch == '\x1b[C': return 'right'
                if ch == '\x1b[D': return 'left'
            elif ch == '\r' or ch == '\n': return 'enter'
            elif ch == '\x03': return 'ctrl_c'
            return 'unknown'


# TEST CODE
async def test_menu_generator(props):
    """Test menu generator"""
    return {
        'title': '🏠 MAIN MENU',
        'options': [
            [
                {'name': '📁 OPEN FILE', 'action': lambda: print("Opening file...")},
                {'name': '💾 SAVE FILE', 'action': lambda: print("Saving file...")}
            ],
            [
                {'name': '⚙️ SETTINGS', 'action': lambda: print("Opening settings...")},
                {'name': '🔧 TOOLS', 'action': lambda: print("Opening tools...")}
            ],
            {'name': '🚪 EXIT', 'action': lambda: print("Goodbye!")}
        ]
    }

async def main():
    hud = TerminalHUD({'highlight_color': 'cyan'})
    
    try:
        result = await hud.display_menu(test_menu_generator, {
            'clear_screen': True,
            'alert': 'Welcome to the fixed TerminalHUD!',
            'alert_emoji': '🎯'
        })
        print(f"\nSelected: {result}")
        
        await hud.press_wait()
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        hud.close()

if __name__ == "__main__":
    asyncio.run(main())
