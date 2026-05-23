import sys
from renonus.core.renamer import VideoRenamer
from renonus.tui.interface import RenonusTUI

def executar():
    tui = RenonusTUI()
    
    caminho_input = input("Digite o caminho completo da pasta dos vídeos: ").strip()
    core = VideoRenamer(caminho_input)

    if not core.validar_diretorio():
        print(tui.term.red("\n[Erro] Diretório inválido."))
        return

    arquivos = core.listar_videos()
    if not arquivos:
        print(tui.term.red("\n[Erro] Nenhum vídeo .mp4 encontrado."))
        return

    titulo_base, usar_pt = tui.obter_configuracoes_nome()
    if not titulo_base:
        return

    # Entrega os arquivos puros do Core para serem renderizados pela TUI
    mapa_selecao = tui.renderizar_lista(arquivos, titulo_base, usar_pt)
    
    print(tui.term.clear)
    if mapa_selecao is None:
        print(tui.term.bold_yellow("Operação abortada. Nenhum arquivo foi alterado."))
        return

    print(tui.term.bold_green("=== PROCESSANDO ALTERAÇÕES NO DISCO ===\n"))

    for idx, arquivo in enumerate(arquivos):
        parte = mapa_selecao[idx]
        if parte > 0:
            novo_nome = core.gerar_novo_nome(arquivo.name, titulo_base, usar_pt, parte)
            try:
                core.aplicar_renomeacao(arquivo, novo_nome)
                print(f"{tui.term.green('✔')} {arquivo.name} ➔ {tui.term.bold(novo_nome)}")
            except Exception as e:
                print(f"{tui.term.red('✘')} Falha ao renomear {arquivo.name}: {e}")
        else:
            print(f"{tui.term.darkgray('○ Ignorado:')} {tui.term.darkgray(arquivo.name)}")

    print(tui.term.bold_green("\n[Sucesso] Script finalizado com êxito!"))

if __name__ == "__main__":
    executar()
