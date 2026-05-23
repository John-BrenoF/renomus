from blessed import Terminal
from pathlib import Path

class RenonusTUI:
    def __init__(self):
        self.term = Terminal()

    def obter_configuracoes_nome(self) -> tuple[str | None, bool]:
        print(self.term.clear)
        print(self.term.bold_magenta("=== CONFIGURAÇÃO DO LOTE ==="))
        
        titulo = input(f"\n{self.term.bold('1.')} Digite o novo título base (sem extensão): ").strip()
        if not titulo:
            print(self.term.red("\n[Erro] O título não pode ser vazio."))
            return None, False
            
        usar_pt = input(f"{self.term.bold('2.')} Deseja usar o prefixo 'pt' antes do número? (s/n): ").strip().lower() == 's'
        return titulo, usar_pt

    def renderizar_lista(self, arquivos: list[Path], titulo_base: str, usar_pt: bool) -> dict[int, int] | None:
        selecao = {i: 0 for i in range(len(arquivos))}
        cursor = 0
        proxima_parte = 1

        with self.term.cbreak(), self.term.hidden_cursor():
            print(self.term.clear)
            while True:
                selecionados = sum(1 for v in selecao.values() if v > 0)
                
                with self.term.location(0, 0):
                    header = f"  RENOVA-MIDIA TUI  |  Título: {titulo_base}  |  Modo: {'Nome + pt + X' if usar_pt else 'Nome + X'}"
                    print(self.term.bold_white_on_darkviolet(header.ljust(self.term.width)) + self.term.clear_eol)
                    print(self.term.clear_eol)

                    for idx, arquivo in enumerate(arquivos):
                        if idx == cursor:
                            prefixo = self.term.bold_cyan(" ➔ ")
                            bg_inicio, bg_fim = self.term.on_gray20, self.term.normal
                        else:
                            prefixo = "   "
                            bg_inicio, bg_fim = "", ""

                        parte = selecao[idx]
                        if parte > 0:
                            sufixo = f" pt {parte}" if usar_pt else f" {parte}"
                            marcador = self.term.bold_black_on_green(f" PARTE {parte} ")
                            preview = f" ➔ {titulo_base}{sufixo}{arquivo.suffix}"
                            conteudo = f"{marcador} {self.term.white(arquivo.name)}{self.term.darkgray(preview)}"
                        else:
                            marcador = self.term.bold_black_on_bright_black(" IGNORAR ")
                            conteudo = f"{marcador} {self.term.dimgray(arquivo.name)}"

                        print(f"{prefixo}{bg_inicio}{conteudo}{bg_fim}" + self.term.clear_eol)

                    linha_controles = self.term.height - 4
                    print(self.term.move_xy(0, linha_controles) + self.term.darkgray("━" * self.term.width) + self.term.clear_eol)
                    print(self.term.move_xy(0, linha_controles + 1) + 
                          f" {self.term.bold_yellow('Setas ⬆⬇')} Mover | "
                          f" {self.term.bold_yellow('Espaço')} Alternar Seleção | "
                          f" {self.term.bold_yellow('1-9')} Forçar número" + self.term.clear_eol)
                    print(self.term.move_xy(0, linha_controles + 2) + 
                          f" {self.term.bold_green('Enter')} Aplicar Alterações | "
                          f" {self.term.bold_red('ESC')} Abortar Operação" + self.term.clear_eol)
                    
                    status = f" Progresso: {selecionados}/{len(arquivos)} arquivos marcados para renomeação."
                    print(self.term.move_xy(0, self.term.height - 1) + self.term.bold_white_on_deepskyblue(status.ljust(self.term.width)), end="")

                    val = self.term.inkey()

                    if val.name == 'KEY_DOWN':
                        cursor = (cursor + 1) % len(arquivos)
                    elif val.name == 'KEY_UP':
                        cursor = (cursor - 1) % len(arquivos)
                    elif val == ' ':
                        if selecao[cursor] > 0:
                            selecao[cursor] = 0
                        else:
                            selecao[cursor] = proxima_parte
                            proxima_parte += 1
                    elif val.isdigit() and val != '0':
                        selecao[cursor] = int(val)
                        if int(val) >= proxima_parte:
                            proxima_parte = int(val) + 1
                    elif val.name == 'KEY_ENTER':
                        break
                    elif val.name == 'KEY_ESCAPE':
                        return None
        return selecao
