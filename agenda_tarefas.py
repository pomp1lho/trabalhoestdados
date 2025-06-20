# ==============================================================================
#                     AGENDA DE TAREFAS
# ==============================================================================

import functools
import random
import time
from datetime import datetime


@functools.total_ordering
class Task:
    """Representa uma tarefa com uma descrição e uma prioridade."""
    def __init__(self, description: str, priority: int):
        if not isinstance(priority, int):
            raise TypeError("A prioridade deve ser um número inteiro.")
        self.description = description
        self.priority = priority

    def __lt__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return self.priority < other.priority

    def __eq__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return self.priority == other.priority and self.description == other.description

    def __repr__(self):
        return f"Task(priority={self.priority}, description='{self.description}')"

    def __str__(self):
        return f"[Prioridade: {self.priority}] - {self.description}"


class BinaryHeap:
    """Implementação de um Heap Binário (Min-Heap) usando uma lista."""
    def __init__(self):
        self.items = [None] 
        self.size = 0

    def _sift_up(self, i):
        while (i // 2) > 0:
            if self.items[i] < self.items[i // 2]:
                self.items[i], self.items[i // 2] = self.items[i // 2], self.items[i]
            i = i // 2

    def insert(self, key):
        self.items.append(key)
        self.size += 1
        self._sift_up(self.size)

    def _sift_down(self, i):
        while (i * 2) <= self.size:
            mc = self._min_child(i)
            if self.items[i] > self.items[mc]:
                self.items[i], self.items[mc] = self.items[mc], self.items[i]
            i = mc

    def _min_child(self, i):
        if (i * 2 + 1) > self.size:
            return i * 2
        else:
            if self.items[i * 2] < self.items[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def extract_min(self):
        if self.is_empty(): return None
        min_val = self.items[1]
        self.items[1] = self.items[self.size]
        self.size -= 1
        self.items.pop()
        if not self.is_empty(): self._sift_down(1)
        return min_val

    def find_min(self):
        return self.items[1] if not self.is_empty() else None
        
    def is_empty(self):
        return self.size == 0

# Listas de frases para tornar a interação mais dinâmica e menos repetitiva
GREETINGS_ADD = ["Certo, o que você gostaria de adicionar à sua lista?", "Ok, qual é a nova tarefa?", "Pode falar, estou anotando a nova tarefa."]
CONFIRMATIONS_ADD = ["Anotado com sucesso!", "Prontinho, já está na lista.", "Tarefa guardada. O que mais?"]
MESSAGES_DONE = ["Ótimo trabalho! Uma coisa a menos para se preocupar.", "Parabéns por concluir esta tarefa!", "Excelente! Tarefa removida da sua lista de pendências."]
EMPTY_LIST_MESSAGES = ["Parece que você está em dia! Nenhum item na lista.", "Sua lista de tarefas está limpa. Momento de relaxar!", "Nada pendente por aqui. Bom trabalho!"]

def get_day_greeting():
    """Retorna uma saudação baseada na hora do dia."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "um ótimo dia"
    elif 12 <= hour < 18:
        return "uma ótima tarde"
    else:
        return "uma ótima noite"

def print_menu():
    """Exibe o menu de opções para o usuário."""
    print("\n--- Menu da Sua Agenda Inteligente ---")
    print("  'add'    -> Anotar uma nova tarefa.")
    print("  'next'   -> Ver qual é a próxima tarefa.")
    print("  'done'   -> Concluir a tarefa mais urgente.")
    print("  'list'   -> Mostrar todas as tarefas pendentes.")
    print("  'help'   -> Ver este menu novamente.")
    print("  'exit'   -> Sair da agenda.")
    print("----------------------------------------")

def main():
    """Função principal que executa o loop do programa de forma mais humana."""
    task_heap = BinaryHeap()
    
    print(f"Olá! Tenha {get_day_greeting()}. Vamos organizar suas tarefas.")
    print_menu()

    while True:
        command = input("\nO que você gostaria de fazer agora? > ").lower().strip()

        if command == "add":
            try:
                description = input(f"  {random.choice(GREETINGS_ADD)} ")
                priority_str = input(f"  Entendido. Qual a prioridade para '{description}'? (ex: 1, 2, 3...) ")
                priority = int(priority_str)
                
                new_task = Task(description, priority)
                task_heap.insert(new_task)
                
                time.sleep(0.5) # Simula o "pensamento" do assistente
                print(f"\n{random.choice(CONFIRMATIONS_ADD)}")

            except (ValueError, TypeError):
                print("\nOpa! A prioridade precisa ser um número inteiro, por favor. Vamos tentar de novo.")

        elif command == "next":
            if task_heap.is_empty():
                print(f"\n{random.choice(EMPTY_LIST_MESSAGES)}")
            else:
                min_task = task_heap.find_min()
                print(f"\nO próximo item na sua lista é: {min_task}")

        elif command == "done":
            if task_heap.is_empty():
                print(f"\n{random.choice(EMPTY_LIST_MESSAGES)}")
            else:
                completed_task = task_heap.extract_min()
                time.sleep(0.5)
                print(f"\n{random.choice(MESSAGES_DONE)}")
                print(f"   -> Concluído: {completed_task}")


        elif command == "list":
            if task_heap.is_empty():
                print(f"\n{random.choice(EMPTY_LIST_MESSAGES)}")
            else:
                print("\nCom certeza! Preparando sua lista, da mais para a menos urgente:")
                time.sleep(0.5)
                temp_tasks = []
                while not task_heap.is_empty():
                    task = task_heap.extract_min()
                    print(f"  - {task}")
                    temp_tasks.append(task)
                
                for task in temp_tasks:
                    task_heap.insert(task)
                print("\n(Sua lista foi recarregada e está pronta para uso!)")

        elif command == "help":
            print_menu()

        elif command == "exit":
            print("\nTudo bem. Agenda fechada por enquanto. Tenha um ótimo resto de dia!")
            break

        else:
            print(f"\nDesculpe, não entendi o comando '{command}'. Que tal tentar 'add', 'list' ou 'help'?")


if __name__ == "__main__":
    main()