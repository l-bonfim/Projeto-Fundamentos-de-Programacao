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
    With navigation support between menus
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
        self.menu_stack = []  # Track menu navigation history

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
        
        # Convert all options to a flat list for simpler navigation
        flat_options = []
        for opt in options:
            if isinstance(opt, list):
                flat_options.extend(opt)
            else:
                flat_options.append(opt)
        
        current_index = initial_index
        if current_index >= len(flat_options):
            current_index = 0

        def render_menu():
            # Use normal print statements without raw mode interference
            self.clear_screen()
            
            if question:
                print(f"{question}\n")
            
            # Render all options with proper line breaks
            for i, opt in enumerate(flat_options):
                text = opt if isinstance(opt, str) else opt.get('name', str(opt))
                
                if i == current_index:
                    # Selected option
                    color = self.get_color_code(self.highlight_color)
                    print(f"{color}→ {text}{self.reset_color()}")
                else:
                    # Normal option
                    print(f"  {text}")
            
            # Removed the "Selected:" line - only show instructions
            print(f"\nUse ↑↓ arrows to navigate, Enter to select")

        # Initial render with normal terminal mode
        render_menu()
        
        # Setup terminal for key reading only
        self._setup_terminal()
        
        try:
            while True:
                key = self._get_key()
                
                old_index = current_index
                
                if key == 'up':
                    if current_index > 0:
                        current_index -= 1
                    else:
                        current_index = len(flat_options) - 1  # Wrap to bottom
                elif key == 'down':
                    if current_index < len(flat_options) - 1:
                        current_index += 1
                    else:
                        current_index = 0  # Wrap to top
                elif key == 'enter':
                    self.last_selected_index = current_index
                    selected = flat_options[current_index]
                    
                    if isinstance(selected, dict) and selected.get('action'):
                        return {'action': selected['action'], 'name': selected.get('name', str(selected))}
                    
                    result = selected if isinstance(selected, str) else selected.get('name', str(selected))
                    return result
                elif key == 'ctrl_c':
                    raise KeyboardInterrupt
                elif key == 'esc':
                    return 'back'
                
                if old_index != current_index:
                    # Restore terminal for proper rendering, then put back in raw mode
                    self._restore_terminal()
                    render_menu()
                    self._setup_terminal()
                
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
        
        # Flatten options for simple display
        flat_options = []
        for opt in options:
            if isinstance(opt, list):
                flat_options.extend(opt)
            else:
                flat_options.append(opt)
        
        for opt in flat_options:
            text = opt if isinstance(opt, str) else opt.get('name', str(opt))
            print(f"{index}. {text}")
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
                    return await self.display_menu_from_options(question, options, config)

                if isinstance(selected, dict) and selected.get('action'):
                    return {'action': selected['action'], 'name': selected.get('name', str(selected))}
                
                if isinstance(selected, str):
                    return selected
                
                return selected.get('name', str(selected))
                
            except ValueError:
                print('Please enter a valid number.')

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
        if asyncio.iscoroutinefunction(menu_generator):
            menu = await menu_generator(props)
        else:
            menu = menu_generator(props)
            
        self.stop_loading()

        if alert:
            print(f"{alert_emoji}  {alert}\n")

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
        self.menu_stack.append((menu_generator, config))

        if self.numbered_menus:
            result = await self.display_numbered_menu(menu_title, menu.get('options', []))
        else:
            result = await self.display_menu_with_arrows(menu_title, menu.get('options', []), 
                                                       {'clear': True}, initial_index)

        if result == 'back':
            return await self.go_back()

        if isinstance(result, dict) and 'action' in result:
            action_result = result['action']
            
            if asyncio.iscoroutinefunction(action_result):
                action_result = await action_result()
            elif callable(action_result):
                action_result = action_result()
            else:
                action_result = action_result
            
            if callable(action_result):
                return await self.display_menu(action_result, config)
            elif asyncio.iscoroutinefunction(action_result):
                menu_data = await action_result()
                if callable(menu_data):
                    return await self.display_menu(menu_data, config)
            
            return result['name']
        
        return result

    async def display_numbered_menu(self, title: str, options: List[Any]) -> str:
        self.clear_screen()
        if title:
            print(f"{title}\n")

        option_map = {}
        index = 1
        
        # Flatten options
        flat_options = []
        for opt in options:
            if isinstance(opt, list):
                flat_options.extend(opt)
            else:
                flat_options.append(opt)
        
        for opt in flat_options:
            if isinstance(opt, dict) and opt.get('type') == 'text' and 'value' in opt:
                print(opt['value'])
            else:
                text = opt if isinstance(opt, str) else opt.get('name', str(opt))
                print(f"{index}. {text}")
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

                if isinstance(selected, dict) and selected.get('action'):
                    return {'action': selected['action'], 'name': selected.get('name', str(selected))}

                if selected.get('action'):
                    action = selected['action']
                    if asyncio.iscoroutinefunction(action):
                        await action()
                    else:
                        action()

                return selected.get('name', str(selected))

            except ValueError:
                print('Please enter a valid number.')

    async def go_back(self):
        """Go back to previous menu in navigation stack"""
        if len(self.menu_stack) > 1:
            self.menu_stack.pop()
            previous_menu_generator, previous_config = self.menu_stack.pop()
            return await self.display_menu(previous_menu_generator, previous_config)
        return None

    async def navigate_to_menu(self, menu_generator: Callable, config: Dict[str, Any] = None):
        return await self.display_menu(menu_generator, config)

    async def press_wait(self):
        print('\nPress any key to continue...')
        self._setup_terminal()
        try:
            self._get_key()
        finally:
            self._restore_terminal()

    def close(self):
        self._restore_terminal()

    def _setup_terminal(self):
        """Setup terminal for single character input without echo"""
        if not IS_WINDOWS and sys.stdin.isatty():
            try:
                self.original_terminal_settings = termios.tcgetattr(sys.stdin)
                new_settings = termios.tcgetattr(sys.stdin)
                new_settings[3] = new_settings[3] & ~(termios.ICANON | termios.ECHO)
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)
            except Exception as e:
                pass

    def _restore_terminal(self):
        """Restore terminal to original settings"""
        if not IS_WINDOWS and self.original_terminal_settings and sys.stdin.isatty():
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.original_terminal_settings)
                self.original_terminal_settings = None
            except Exception as e:
                pass

    def _get_key(self) -> str:
        """Get a single key press with proper blocking"""
        if IS_WINDOWS:
            ch = msvcrt.getch()
            if ch == b'\xe0':
                ch = msvcrt.getch()
                if ch == b'H': return 'up'
                if ch == b'P': return 'down'
                if ch == b'K': return 'left'
                if ch == b'M': return 'right'
            elif ch == b'\r': return 'enter'
            elif ch == b'\x03': return 'ctrl_c'
            elif ch == b'\x1b': return 'esc'
            return 'unknown'
        else:
            # Block until we get a key
            while True:
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    # Escape sequence - read more
                    ch2 = sys.stdin.read(1)
                    if ch2 == '[':
                        ch3 = sys.stdin.read(1)
                        if ch3 == 'A': return 'up'
                        if ch3 == 'B': return 'down'
                        if ch3 == 'C': return 'right'
                        if ch3 == 'D': return 'left'
                    return 'esc'
                elif ch == '\r' or ch == '\n': 
                    return 'enter'
                elif ch == '\x03': 
                    return 'ctrl_c'
                # Ignore other keys


# Test with a simpler menu structure
async def test_menu_generator(props):
    return {
        'title': '🏠 MAIN MENU',
        'options': [
            '📁 OPEN FILE',
            '💾 SAVE FILE', 
            '⚙️ SETTINGS',
            '🔧 TOOLS',
            '🚪 EXIT'
        ]
    }

async def main():
    hud = TerminalHUD({'highlight_color': 'cyan'})
    
    try:
        result = await hud.display_menu(test_menu_generator, {
            'clear_screen': True,
            'alert': 'Welcome to TerminalHUD!',
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
