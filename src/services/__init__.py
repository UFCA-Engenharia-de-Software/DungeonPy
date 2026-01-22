"""
Módulo Services - Orquestração e Regras de Negócio do DungeonPy.

Este pacote é responsável por coordenar as interações entre as entidades 
do domínio, implementando o fluxo lógico das mecânicas de jogo.

Componentes principais:
    - Combate: Orquestra o fluxo de turnos, aplicação de estados e cálculo 
      de dano final.
    - Sistema de Progressão: Gerencia a evolução do Herói através da 
      aquisição de equipamentos (Loot).
    - Gerenciador de Masmorra: Coordena a transição entre salas e a 
      preparação do contexto de jogo.
"""