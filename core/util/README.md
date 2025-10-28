# TerminalHUD

## Componentes Principais:

- Sistema de Display: Menus com navegação por setas ou números

- Controle de Terminal: Compatível com Windows (msvcrt) e Unix (termios)

- Sistema de Navegação: Pilha para histórico de menus

- Sistemas de Menu:

display_menu_with_arrows(): Navegação visual com setas

display_menu_from_options(): Menu numerado tradicional

## Inicialização e Configuração

```python
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

```

## 1. Sistema de Renderização e Organização de Opções

- Estrutura de Processamento de Opções
```python
def normalize_options(self, options: List[Any]) -> List[List[Any]]:
    result = []
    for opt in options:
        if isinstance(opt, list):  # Linha horizontal de opções
            normalized_line = []
            for item in opt:
                if isinstance(item, str):
                    normalized_line.append({'name': item})
                else:
                    normalized_line.append(item)
            result.append(normalized_line)
        elif isinstance(opt, dict) and opt.get('type') == 'options':
            # Grupo especial de opções
            normalized_line = []
            for item in opt.get('value', []):
                if isinstance(item, str):
                    normalized_line.append({'name': item})
                else:
                    normalized_line.append(item)
            result.append(normalized_line)
        else:  # Opção única (transforma em linha com um item)
            if isinstance(opt, str):
                result.append([{'name': opt}])
            else:
                result.append([opt])
    return result
```

- Sistema de Renderização Visual

```python
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
```

Fluxo de Renderização:

Normalização: Converte opções para formato padrão List[List[dict]]

Layout Grid: Organiza opções em linhas e colunas

Destaque Visual: → símbolo + cor para opção selecionada

Espaçamento: " " entre opções na mesma linha

Feedback: Mostra posição atual (Linha X, Opção Y)

Exemplo de Saída:
```text
Qual opção você prefere?

→ Opção A   Opção B   Opção C
  Opção D   Opção E   Opção F

Use arrow keys to navigate, Enter to select
Selected: Line 1, Option 1
```

## 2. Sistema de Captura de Teclas e Execução de Ações
- Loop Principal de Navegação

```python
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
        
        # Handle action - return special marker if action is present
        if isinstance(selected, dict) and selected.get('action'):
            return {'action': selected['action'], 'name': selected.get('name', str(selected))}
        
        result = selected if isinstance(selected, str) else selected.get('name', str(selected))
        return result
    elif key == 'ctrl_c':
        raise KeyboardInterrupt
    
    # Only re-render if selection changed
    if old_line != line or old_col != col:
        render_menu()
```

- Sistema de Captura de Teclado Multiplataforma
  
```python
def _get_key(self) -> str:
    if IS_WINDOWS:
        ch = msvcrt.getch()
        if ch == b'\xe0':  # Arrow keys prefix
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
```

- Processamento de Ações ao Pressionar Enter
```python
elif key == 'enter':
    self.last_selected_index = self.get_linear_index_from_coordinates(lines, line, col)
    selected = lines[line][col]
    
    # Handle action - return special marker if action is present
    if isinstance(selected, dict) and selected.get('action'):
        return {'action': selected['action'], 'name': selected.get('name', str(selected))}
    
    result = selected if isinstance(selected, str) else selected.get('name', str(selected))
    return result
```

Fluxo de Execução:

Captura: _get_key() detecta tecla pressionada

Navegação: ↑↓←→ atualizam coordenadas (line, col)

Seleção: Enter captura opção atual lines[line][col]

Verificação: Checa se opção tem action definida

Retorno:

Com ação: {'action': callback, 'name': 'Nome'}

Sem ação: string com nome da opção

Renderização Condicional: Só redesenha se posição mudou

Exemplo de Ação:

```python
# Quando usuário seleciona esta opção e pressiona Enter:
{'name': '📁 ABRIR ARQUIVO', 'action': lambda: print("Abrindo arquivo...")}

# O sistema retorna:
{'action': <function...>, 'name': '📁 ABRIR ARQUIVO'}

# E o menu principal processa a ação executando a função
```


