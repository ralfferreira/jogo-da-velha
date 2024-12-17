from jogador import Jogador
from tabuleiro import Tabuleiro

class JogadorIA(Jogador):
    def __init__(self, tabuleiro: Tabuleiro, tipo: int):
        super().__init__(tabuleiro, tipo)
        self.oponente = Tabuleiro.JOGADOR_X if tipo == Tabuleiro.JOGADOR_0 else Tabuleiro.JOGADOR_0

    def check_sequence(self, jogador):
        for i in range(3):
            if self.matriz[i].count(jogador) == 2 and self.matriz[i].count(Tabuleiro.DESCONHECIDO) == 1:
                return (i, self.matriz[i].index(Tabuleiro.DESCONHECIDO))
            
            col = [self.matriz[j][i] for j in range(3)]
            if col.count(jogador) == 2 and col.count(Tabuleiro.DESCONHECIDO) == 1:
                return (col.index(Tabuleiro.DESCONHECIDO), i)

        diag1 = [self.matriz[i][i] for i in range(3)]
        if diag1.count(jogador) == 2 and diag1.count(Tabuleiro.DESCONHECIDO) == 1:
            pos = diag1.index(Tabuleiro.DESCONHECIDO)
            return (pos, pos)

        diag2 = [self.matriz[i][2-i] for i in range(3)]
        if diag2.count(jogador) == 2 and diag2.count(Tabuleiro.DESCONHECIDO) == 1:
            pos = diag2.index(Tabuleiro.DESCONHECIDO)
            return (pos, 2-pos)

        return None

    def R1_completar_sequencia(self):
        """R1: Se você ou seu oponente tiver duas marcações em sequência, marque o quadrado restante"""
        move = self.check_sequence(self.tipo)
        if move:
            return move
        
        move = self.check_sequence(self.oponente)
        if move:
            return move
        
        return None

    def R2_criar_dupla_ameaca(self):
        """R2: Se houver uma jogada que crie duas sequências de duas marcações, use-a"""
        for i in range(3):
            for j in range(3):
                if self.matriz[i][j] == Tabuleiro.DESCONHECIDO:
                    count = 0
                    row = self.matriz[i].count(self.tipo)
                    if row == 1 and self.matriz[i].count(Tabuleiro.DESCONHECIDO) == 2:
                        count += 1
                    col = [self.matriz[k][j] for k in range(3)].count(self.tipo)
                    if col == 1 and [self.matriz[k][j] for k in range(3)].count(Tabuleiro.DESCONHECIDO) == 2:
                        count += 1
                    if (i == j) or (i + j == 2):
                        if i == j:
                            diag = [self.matriz[k][k] for k in range(3)]
                        else:
                            diag = [self.matriz[k][2-k] for k in range(3)]
                        if diag.count(self.tipo) == 1 and diag.count(Tabuleiro.DESCONHECIDO) == 2:
                            count += 1
                    if count >= 2:
                        return (i, j)
        return None

    def R3_marcar_centro(self):
        """R3: Se o quadrado central estiver livre, marque-o"""
        if self.matriz[1][1] == Tabuleiro.DESCONHECIDO:
            return (1, 1)
        return None

    def R4_marcar_canto_oposto(self):
        """R4: Se seu oponente tiver marcado um dos cantos, marque o canto oposto"""
        corners = [(0,0), (0,2), (2,0), (2,2)]
        for i, j in corners:
            if self.matriz[i][j] == self.oponente:
                opposite_i, opposite_j = 2-i, 2-j
                if self.matriz[opposite_i][opposite_j] == Tabuleiro.DESCONHECIDO:
                    return (opposite_i, opposite_j)
        return None

    def R5_marcar_canto_vazio(self):
        """R5: Se houver um canto vazio, marque-o"""
        corners = [(0,0), (0,2), (2,0), (2,2)]
        for i, j in corners:
            if self.matriz[i][j] == Tabuleiro.DESCONHECIDO:
                return (i, j)
        return None

    def R6_marcar_qualquer_posicao(self):
        """R6: Marque arbitrariamente um quadrado vazio"""
        for i in range(3):
            for j in range(3):
                if self.matriz[i][j] == Tabuleiro.DESCONHECIDO:
                    return (i, j)
        return None

    def getJogada(self) -> (int, int): # type: ignore
        """Aplica as regras em ordem até encontrar uma jogada válida"""
        regras = [
            self.R1_completar_sequencia,
            self.R2_criar_dupla_ameaca,
            self.R3_marcar_centro,
            self.R4_marcar_canto_oposto,
            self.R5_marcar_canto_vazio,
            self.R6_marcar_qualquer_posicao
        ]

        for regra in regras:
            jogada = regra()
            if jogada is not None:
                return jogada

        return None