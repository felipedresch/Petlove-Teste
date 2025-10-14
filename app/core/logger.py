import csv
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """
    Utilitário de logging para salvar logs em arquivos TXT e CSV.
    Garante que erros de log não interrompam a aplicação.
    """
    
    def __init__(self):
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        self.txt_log_path = self.logs_dir / "api_requests.txt"
        self.csv_log_path = self.logs_dir / "questions_answers.csv"
        self._init_csv()
    
    def _init_csv(self):
        """Inicializa o arquivo CSV com cabeçalho se não existir."""
        try:
            if not self.csv_log_path.exists():
                with open(self.csv_log_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['timestamp', 'pergunta', 'resposta_inicial'])
        except Exception as e:
            print(f"Aviso: Erro ao inicializar CSV: {e}")
    
    def log_request(
        self, 
        method: str, 
        path: str, 
        status_code: int, 
        duration_ms: float,
        error: Optional[str] = None
    ):
        """
        Registra uma requisição HTTP no arquivo TXT.
        
        Args:
            method: Método HTTP (GET, POST, etc)
            path: Caminho da requisição
            status_code: Código de status da resposta
            duration_ms: Duração da requisição em milissegundos
            error: Mensagem de erro opcional
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_msg = f" | Erro: {error}" if error else ""
            log_line = (
                f"[{timestamp}] {method} {path} | "
                f"Status: {status_code} | "
                f"Duração: {duration_ms:.2f}ms{error_msg}\n"
            )
            
            with open(self.txt_log_path, 'a', encoding='utf-8') as f:
                f.write(log_line)
        except Exception as e:
            print(f"Aviso: Erro ao salvar log TXT: {e}")
    
    def log_question_answer(self, question: str, answer: str):
        """
        Registra uma pergunta e resposta no arquivo CSV.
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            answer_preview = answer[:200] if answer else ""
            if len(answer) > 200:
                answer_preview += "..."
            
            with open(self.csv_log_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, question, answer_preview])
        except Exception as e:
            print(f"Aviso: Erro ao salvar log CSV: {e}")


logger = Logger()

