from datetime import datetime
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Configuração da Página
st.set_page_config(
    page_title="SmartPrice Tracker | UX & Dados",
    page_icon="🛍️",
    layout="wide",
)

# 2. Inicialização do Banco de Dados (SQLite)
def inicializar_banco():
    conexao = sqlite3.connect("precos_ecommerce.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            url TEXT,
            preco_alvo REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            preco REAL,
            data_consulta TEXT,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    """)
    conexao.commit()
    conexao.close()

inicializar_banco()

# 3. Função para desenhar os Cards de Produto
def renderizar_card_produto(prod, df_historico):
    df_hist_prod = df_historico[df_historico['produto_id'] == prod['id']]

    with st.container(border=True):
        if not df_hist_prod.empty:
            ultimo_preco = float(df_hist_prod.iloc[-1]['preco'])
            preco_alvo = float(prod['preco_alvo'])
            diferenca = ultimo_preco - preco_alvo

            if ultimo_preco <= preco_alvo:
                cor_borda = "#10B981"
                cor_badge_bg = "rgba(16, 185, 129, 0.16)"
                cor_badge_txt = "#34D399"
                texto_badge = "Meta atingida"
                mensagem_status = "Preço ideal atingido ou abaixo da meta!"
                cor_msg_bg = "rgba(16, 185, 129, 0.14)"
                cor_msg_borda = "#10B981"
            elif preco_alvo > 0 and ultimo_preco <= preco_alvo * 1.15:
                cor_borda = "#F59E0B"
                cor_badge_bg = "rgba(245, 158, 11, 0.16)"
                cor_badge_txt = "#FBBF24"
                texto_badge = "Perto da meta"
                mensagem_status = f"Faltam R$ {diferenca:.2f} para alcançar a meta."
                cor_msg_bg = "rgba(245, 158, 11, 0.14)"
                cor_msg_borda = "#F59E0B"
            else:
                cor_borda = "#3B82F6"
                cor_badge_bg = "rgba(59, 130, 246, 0.16)"
                cor_badge_txt = "#60A5FA"
                texto_badge = "Acima da meta"
                mensagem_status = f"Faltam R$ {diferenca:.2f} para alcançar a meta."
                cor_msg_bg = "rgba(59, 130, 246, 0.14)"
                cor_msg_borda = "#3B82F6"

            st.markdown(
                f"""
                <div style="
                    border-left: 4px solid {cor_borda};
                    padding: 10px 14px;
                    border-radius: 8px;
                    background-color: rgba(255, 255, 255, 0.02);
                    margin-bottom: 10px;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap;">
                        <span style="font-size: 1.08rem; font-weight: 700;">🛍️ {prod['nome']}</span>
                        <span style="
                            font-size: 0.78rem;
                            font-weight: 600;
                            padding: 3px 10px;
                            border-radius: 999px;
                            background-color: {cor_badge_bg};
                            color: {cor_badge_txt};
                        ">{texto_badge}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 12px; gap: 12px;">
                        <div>
                            <div style="font-size: 0.78rem; opacity: 0.75;">Preço Atual</div>
                            <div style="font-size: 1.35rem; font-weight: 700;">R$ {ultimo_preco:.2f}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.78rem; opacity: 0.75;">Preço Alvo</div>
                            <div style="font-size: 1.35rem; font-weight: 700;">R$ {preco_alvo:.2f}</div>
                        </div>
                    </div>
                    <div style="
                        margin-top: 12px;
                        padding: 8px 12px;
                        border-radius: 6px;
                        background-color: {cor_msg_bg};
                        border: 1px solid {cor_msg_borda};
                        font-size: 0.88rem;
                        font-weight: 500;
                    ">{mensagem_status}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"#### 🛍️ {prod['nome']}")
            st.info("Sem histórico de preços ainda.")

        if prod.get('url'):
            st.markdown(f"🔗 [Acessar Loja]({prod['url']})")

# 4. Cabeçalho da Aplicação
st.title("🛍️ SmartPrice Tracker")
st.markdown("Monitoramento Inteligente de Preços e Tendências.")

# 5. Barra Lateral (Cadastrar Novo Produto ou Registrar Novo Preço)
st.sidebar.header("Gerenciar Rastreamento")

conexao = sqlite3.connect("precos_ecommerce.db")
df_produtos_sidebar = pd.read_sql("SELECT * FROM produtos", conexao)
conexao.close()

modo = st.sidebar.radio(
    "O que você quer fazer?",
    ["Cadastrar Novo Produto", "Registrar Novo Preço em Produto Existente"]
)

if modo == "Cadastrar Novo Produto":
    with st.sidebar.form("form_novo_produto"):
        nome_input = st.text_input("Nome do Produto", placeholder="Ex: Notebook Ultrafino")
        url_input = st.text_input("Link (URL) do Produto", placeholder="https://...")
        preco_atual_input = st.number_input("Preço Atual na Loja (R$)", min_value=0.0, format="%.2f")
        preco_alvo_input = st.number_input("Preço Alvo Desejado (R$)", min_value=0.0, format="%.2f")
        botao_cadastrar = st.form_submit_button("Cadastrar e Rastrear")

    if botao_cadastrar:
        if nome_input and url_input and preco_atual_input > 0:
            conexao = sqlite3.connect("precos_ecommerce.db")
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO produtos (nome, url, preco_alvo) VALUES (?, ?, ?)",
                (nome_input.strip(), url_input.strip(), preco_alvo_input)
            )
            produto_id = cursor.lastrowid
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO historico_precos (produto_id, preco, data_consulta) VALUES (?, ?, ?)",
                (produto_id, preco_atual_input, data_atual)
            )
            conexao.commit()
            conexao.close()
            st.sidebar.success("Produto cadastrado com sucesso!")
            st.rerun()
        else:
            st.sidebar.error("Por favor, preencha o nome, o link e um preço maior que zero.")

else:
    if df_produtos_sidebar.empty:
        st.sidebar.info("Cadastre um produto primeiro para registrar novos preços.")
    else:
        with st.sidebar.form("form_novo_preco"):
            opcoes_produtos = {
                f"#{row['id']} - {row['nome']} (Alvo: R$ {row['preco_alvo']:.2f})": int(row['id'])
                for _, row in df_produtos_sidebar.iterrows()
            }
            produto_escolhido_label = st.selectbox("Escolha o Produto", list(opcoes_produtos.keys()))
            novo_preco_input = st.number_input("Novo Preço Encontrado (R$)", min_value=0.0, format="%.2f")
            atualizar_alvo = st.checkbox("Atualizar também o Preço Alvo deste produto?")
            novo_alvo_input = st.number_input("Novo Preço Alvo (R$)", min_value=0.0, format="%.2f")
            botao_add_preco = st.form_submit_button("Salvar Novo Preço")

        if botao_add_preco:
            if novo_preco_input > 0:
                prod_id_alvo = opcoes_produtos[produto_escolhido_label]
                conexao = sqlite3.connect("precos_ecommerce.db")
                cursor = conexao.cursor()
                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    "INSERT INTO historico_precos (produto_id, preco, data_consulta) VALUES (?, ?, ?)",
                    (prod_id_alvo, novo_preco_input, data_atual)
                )
                if atualizar_alvo and novo_alvo_input > 0:
                    cursor.execute(
                        "UPDATE produtos SET preco_alvo = ? WHERE id = ?",
                        (novo_alvo_input, prod_id_alvo)
                    )
                conexao.commit()
                conexao.close()
                st.sidebar.success("Novo preço adicionado ao histórico!")
                st.rerun()
            else:
                st.sidebar.error("Digite um preço maior que zero.")

# 6. Área Principal: Painel de Monitoramento
st.divider()
st.subheader("📊 Painel de Monitoramento de Produtos")

conexao = sqlite3.connect("precos_ecommerce.db")
df_produtos = pd.read_sql("SELECT * FROM produtos", conexao)
df_historico = pd.read_sql("SELECT * FROM historico_precos", conexao)
conexao.close()

if df_produtos.empty:
    st.info("🛍️ Nenhum produto cadastrado ainda. Use a barra lateral à esquerda para adicionar o primeiro produto!")
else:
    # Métricas Gerais no Topo
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("📦 Total Rastreado", len(df_produtos))
    col_m2.metric("🔄 Checagens Realizadas", len(df_historico))
    col_m3.metric("🎯 Status do Sistema", "Ativo 🟢", "100% online")

    st.markdown("---")
    st.markdown("### 🏷️ Seus Produtos em Destaque")

    # Grade de cards (2 colunas por linha)
    produtos_lista = df_produtos.to_dict('records')
    for i in range(0, len(produtos_lista), 2):
        col_card1, col_card2 = st.columns(2)
        with col_card1:
            renderizar_card_produto(produtos_lista[i], df_historico)
        if i + 1 < len(produtos_lista):
            with col_card2:
                renderizar_card_produto(produtos_lista[i + 1], df_historico)

    st.markdown("---")
        # 6.5. Gerenciar / Remover Produto
    with st.expander("🛠️ Gerenciar ou Remover Produtos Cadastrados"):
        opcoes_gerenciar = {
            f"#{row['id']} - {row['nome']} (Atual/Alvo: R$ {row['preco_alvo']:.2f})": int(row['id'])
            for _, row in df_produtos.iterrows()
        }
        item_gerenciar = st.selectbox("Selecione um produto para gerenciar", list(opcoes_gerenciar.keys()))
        id_gerenciar = opcoes_gerenciar[item_gerenciar]

        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            if st.button("🗑️ Excluir Produto", type="secondary"):
                conexao = sqlite3.connect("precos_ecommerce.db")
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM historico_precos WHERE produto_id = ?", (id_gerenciar,))
                cursor.execute("DELETE FROM produtos WHERE id = ?", (id_gerenciar,))
                conexao.commit()
                conexao.close()
                st.success("Produto removido!")
                st.rerun()
    # 7. Análise Gráfica Detalhada
    st.subheader("📈 Análise Gráfica de Variação")
    produto_selecionado = st.selectbox(
        "Selecione um produto para visualizar o histórico detalhado de preços:",
        df_produtos['nome'].tolist()
    )
    
    if produto_selecionado:
        prod_info = df_produtos[df_produtos['nome'] == produto_selecionado].iloc[0]
        prod_id = prod_info['id']
        preco_alvo = prod_info['preco_alvo']
        
        df_hist_prod = df_historico[df_historico['produto_id'] == prod_id]
        
        if not df_hist_prod.empty:
            fig = px.area(
                df_hist_prod, 
                x='data_consulta', 
                y='preco', 
                markers=True,
                title=f"Evolução de Preço: {produto_selecionado}",
                labels={'preco': 'Preço (R$)', 'data_consulta': 'Data da Consulta'}
            )
            fig.update_traces(line_color='#10B981', fillcolor='rgba(16, 185, 129, 0.1)')
            fig.add_hline(y=preco_alvo, line_dash="dash", line_color="#EF4444", annotation_text="Preço Alvo Desejado")
            
            st.plotly_chart(fig, use_container_width=True)