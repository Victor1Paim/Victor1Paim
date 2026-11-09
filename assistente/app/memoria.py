"""Memória da conversa e controle de mensagens já processadas (SQLite)."""

from __future__ import annotations

import sqlite3
import threading
import time
from pathlib import Path


class Memoria:
    def __init__(self, caminho: Path | str):
        if str(caminho) != ":memory:":
            Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        self._con = sqlite3.connect(str(caminho), check_same_thread=False)
        self._trava = threading.Lock()
        with self._trava:
            self._con.executescript(
                """
                CREATE TABLE IF NOT EXISTS mensagens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero TEXT NOT NULL,
                    papel TEXT NOT NULL,
                    conteudo TEXT NOT NULL,
                    criado_em REAL NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_msg_numero ON mensagens(numero, id);
                CREATE TABLE IF NOT EXISTS processadas (
                    whatsapp_id TEXT PRIMARY KEY,
                    criado_em REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS rascunhos (
                    rascunho_id TEXT PRIMARY KEY,
                    numero TEXT NOT NULL,
                    turno INTEGER NOT NULL
                );
                """
            )
            self._con.commit()

    # --- deduplicação (a Meta reenvia webhooks) ---
    def marcar_processada(self, whatsapp_id: str) -> bool:
        """Retorna True se a mensagem é nova; False se já tinha sido vista."""
        with self._trava:
            try:
                self._con.execute(
                    "INSERT INTO processadas (whatsapp_id, criado_em) VALUES (?, ?)",
                    (whatsapp_id, time.time()),
                )
                self._con.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    # --- histórico ---
    def adicionar(self, numero: str, papel: str, conteudo: str) -> int:
        with self._trava:
            cur = self._con.execute(
                "INSERT INTO mensagens (numero, papel, conteudo, criado_em) VALUES (?, ?, ?, ?)",
                (numero, papel, conteudo, time.time()),
            )
            self._con.commit()
            return int(cur.lastrowid)

    def historico(self, numero: str, limite: int) -> list[dict]:
        with self._trava:
            linhas = self._con.execute(
                "SELECT papel, conteudo FROM mensagens WHERE numero = ? ORDER BY id DESC LIMIT ?",
                (numero, limite),
            ).fetchall()
        linhas.reverse()
        # O histórico precisa começar com uma mensagem do usuário.
        while linhas and linhas[0][0] != "user":
            linhas.pop(0)
        return [{"role": p, "content": c} for p, c in linhas]

    def limpar(self, numero: str) -> None:
        with self._trava:
            self._con.execute("DELETE FROM mensagens WHERE numero = ?", (numero,))
            self._con.execute("DELETE FROM rascunhos WHERE numero = ?", (numero,))
            self._con.commit()

    # --- rascunhos de e-mail (trava de confirmação) ---
    def registrar_rascunho(self, numero: str, rascunho_id: str, turno: int) -> None:
        with self._trava:
            self._con.execute(
                "INSERT OR REPLACE INTO rascunhos (rascunho_id, numero, turno) VALUES (?, ?, ?)",
                (rascunho_id, numero, turno),
            )
            self._con.commit()

    def ultimo_rascunho(self, numero: str) -> tuple[str, int] | None:
        """(rascunho_id, turno) do rascunho mais recente ainda não enviado."""
        with self._trava:
            linha = self._con.execute(
                "SELECT rascunho_id, turno FROM rascunhos WHERE numero = ? ORDER BY turno DESC LIMIT 1",
                (numero,),
            ).fetchone()
        return (linha[0], int(linha[1])) if linha else None

    def remover_rascunho(self, rascunho_id: str) -> None:
        with self._trava:
            self._con.execute("DELETE FROM rascunhos WHERE rascunho_id = ?", (rascunho_id,))
            self._con.commit()
