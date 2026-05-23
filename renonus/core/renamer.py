import os
from pathlib import Path

class VideoRenamer:
    def __init__(self, caminho_pasta: str):
        self.pasta = Path(caminho_pasta.strip()) if isinstance(caminho_pasta, str) else caminho_pasta
        
    def validar_diretorio(self) -> bool:
        return self.pasta.is_dir()

    def listar_videos(self) -> list[Path]:
        """Retorna os vídeos .mp4 ordenados pela data de modificação."""
        if not self.validar_diretorio():
            return []
        arquivos = [f for f in self.pasta.iterdir() if f.is_file() and f.suffix.lower() == '.mp4']
        arquivos.sort(key=lambda x: x.stat().st_mtime)
        return arquivos

    def gerar_novo_nome(self, nome_arquivo: str, titulo_base: str, usar_pt: bool, parte: int) -> str:
        """Apenas calcula a string do novo nome com base nas regras."""
        extensao = Path(nome_arquivo).suffix
        sufixo = f" pt {parte}" if usar_pt else f" {parte}"
        return f"{titulo_base}{sufixo}{extensao}"

    def aplicar_renomeacao(self, arquivo: Path, novo_nome: str) -> None:
        """Executa a alteração física no sistema de arquivos."""
        novo_caminho = arquivo.with_name(novo_nome)
        arquivo.rename(novo_caminho)
