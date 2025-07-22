# Alien Scape

## Descrição

Alien Scape é um jogo do gênero **Platformer** criado usando **PgZero**. O jogador controla um alienígena que deve atravessar plataformas, evitar inimigos móveis, coletar a chave e levar a porta para vencer o jogo.

## Funcionalidades

- Menu principal com botões clicáveis: iniciar jogo, ligar/desligar música, sair.
- Música de fundo e efeitos sonoros.
- Dois tipos de inimigos com movimentação dentro de territórios definidos.
- Animações de sprites para herói e inimigos nas ações de andar, pular e estar parado.
- Mecânica lógica consistente e sem bugs conhecidos.
- Código estruturado em classes claras e seguindo PEP8.

## Tecnologias e Bibliotecas

- Python 3.12
- PgZero (para engine e sprites)
- Importação da classe `Rect` do Pygame (exclusivamente para colisões)

## Requisitos atendidos

- Gênero: Platformer com visão lateral e plataformas.
- Estrutura com menu, sons e música.
- Implementação orientada a objetos para personagens e inimigos.
- Animações de sprite contínuas e diferenciadas para movimento e estado parado.
- Exclusivamente bibliotecas permitidas usadas.
- Código original, claro e limpo.

## Como executar

1. Instale as dependências:

        pip install pgzero pygame

2. Rode o jogo com: 

        pgzrun game.py
