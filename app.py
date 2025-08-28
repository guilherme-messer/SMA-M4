import random

class FilaGG:
    def __init__(self, servidores, capacidade, chegada_min, chegada_max, atendimento_min, atendimento_max, seed=42):
        self.servidores = servidores
        self.capacidade = capacidade
        self.chegada_min = chegada_min
        self.chegada_max = chegada_max
        self.atendimento_min = atendimento_min
        self.atendimento_max = atendimento_max
        self.relogio = 0.0
        self.eventos = []
        self.estado_fila = 0
        self.estados_tempo = [0] * (capacidade + 1)
        self.ultimo_evento = 0.0
        self.perdas = 0
        self.randoms_usados = 0
        random.seed(seed)

    def proximo_num(self):
        self.randoms_usados += 1
        return random.random()

    def tempo_chegada(self):
        return self.chegada_min + (self.chegada_max - self.chegada_min) * self.proximo_num()

    def tempo_atendimento(self):
        return self.atendimento_min + (self.atendimento_max - self.atendimento_min) * self.proximo_num()

    def simular(self, limite_randoms=100000):
        # agenda primeira chegada no tempo 2
        self.eventos.append((2.0, 'chegada'))
        self.randoms_usados = 0

        while self.randoms_usados < limite_randoms and self.eventos:
            self.eventos.sort(key=lambda x: x[0])
            tempo, tipo = self.eventos.pop(0)
            # acumula tempo no estado anterior
            self.estados_tempo[self.estado_fila] += tempo - self.relogio
            self.relogio = tempo

            if tipo == 'chegada':
                if self.estado_fila < self.capacidade:
                    self.estado_fila += 1
                    if self.estado_fila <= self.servidores:
                        self.eventos.append((self.relogio + self.tempo_atendimento(), 'saida'))
                else:
                    self.perdas += 1
                # agenda próxima chegada
                self.eventos.append((self.relogio + self.tempo_chegada(), 'chegada'))

            elif tipo == 'saida':
                self.estado_fila -= 1
                if self.estado_fila >= self.servidores:
                    self.eventos.append((self.relogio + self.tempo_atendimento(), 'saida'))

        # normaliza probabilidades
        total_tempo = sum(self.estados_tempo)
        probs = [t / total_tempo for t in self.estados_tempo]

        return {
            "tempo_total": self.relogio,
            "estados_tempo": self.estados_tempo,
            "probs": probs,
            "perdas": self.perdas,
            "randoms_usados": self.randoms_usados
        }


# Exemplo de execução
if __name__ == "__main__":
    fila1 = FilaGG(servidores=1, capacidade=5, chegada_min=2, chegada_max=5, atendimento_min=3, atendimento_max=5)
    resultado1 = fila1.simular()
    print("G/G/1/5:", resultado1)

    fila2 = FilaGG(servidores=2, capacidade=5, chegada_min=2, chegada_max=5, atendimento_min=3, atendimento_max=5)
    resultado2 = fila2.simular()
    print("G/G/2/5:", resultado2)
