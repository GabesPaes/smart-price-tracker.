# 🛒 SmartPrice Tracker

Aplicação web interativa desenvolvida em **Python** e **Streamlit** para monitoramento de preços de produtos, acompanhamento de metas e visualização de histórico com **SQLite**, **Pandas** e **Plotly**.

## 📌 Sobre o Projeto

O **SmartPrice Tracker** centraliza o acompanhamento de preços de produtos de interesse, permitindo comparar o preço atual com um preço alvo definido pelo usuário, registrar novas consultas ao longo do tempo e visualizar a evolução dos valores em um gráfico interativo.

O projeto foi pensado para unir **organização de dados** e **clareza visual (UI/UX)**, facilitando a leitura rápida do status de cada item e a tomada de decisão de compra.

## ✨ Principais Funcionalidades

- **Painel de KPIs no topo:** visão geral rápida dos itens monitorados, volume de checagens e status do sistema.
- **Cards de produtos com destaque visual por meta:** indicação visual e etiquetas de status (*Meta atingida*, *Perto da meta* ou *Acima da meta*) com base na comparação entre preço atual e preço alvo.
- **Cadastro e registro de histórico:** possibilidade de cadastrar novos produtos ou adicionar novos preços a produtos já existentes sem duplicar o item principal.
- **Gerenciamento e exclusão:** remoção de produtos indesejados ou duplicados diretamente na interface, mantendo a base limpa.
- **Análise gráfica interativa:** gráfico de evolução de preços ao longo do tempo com linha de referência do preço alvo.

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Streamlit** (interface web e layout interativo)
- **SQLite** (`precos_ecommerce.db` para persistência local de produtos e histórico)
- **Pandas** (manipulação e filtragem dos dados tabulares)
- **Plotly** (visualização gráfica interativa)

## 🚀 Como Executar Localmente

1. Clone ou baixe este repositório:
   ```bash
   git clone https://github.com/GabesPaes/smart-price-tracker..git
   cd smart-price-tracker