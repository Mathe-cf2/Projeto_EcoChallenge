import streamlit as st
import pandas as pd
import time

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="EcoChallenge Pro",
    page_icon="🌎",
    layout="wide"
)

# =========================================================
# BANCO DE DADOS DO RANKING (INICIA VAZIO)
# =========================================================
if "ranking" not in st.session_state:
    st.session_state.ranking = []

# =========================================================
# CONTROLE DE TEMPO
# =========================================================
if "tempo_inicio" not in st.session_state:
    st.session_state.tempo_inicio = 0.0

# =========================================================
# PERGUNTAS
# =========================================================
perguntas = [
    {
        "tema": "⚡ Matriz Energética",
        "pergunta": "Qual fator limita significativamente a eficiência global do Hidrogênio Verde (H2V) como vetor energético?",
        "opcoes": [
            "A escassez crítica de água pura nas regiões de alta insolação",
            "A baixa densidade volumétrica somada à perda de carga na eletrólise",
            "A toxidade residual gerada no processo de conversão em amônia",
            "A falta de compatibilidade com turbinas elétricas de alta potência"
        ],
        "correta": "A baixa densidade volumétrica somada à perda de carga na eletrólise",
        "explicacao": "A produção de H2V exige muita eletricidade no processo de eletrólise e sua estocagem demanda compressão extrema, gerando perdas energéticas na cadeia."
    },
    {
        "tema": "📊 Mecanismos de Mercado",
        "pergunta": "No mercado de carbono, qual o papel do conceito de 'Adicionalidade' na validação de um projeto de compensação?",
        "opcoes": [
            "Provar que as reduções só ocorreriam devido aos créditos do projeto",
            "Garantir a permanência do estoque de carbono por no mínimo cem anos",
            "Aumentar proporcionalmente o valor do crédito a cada ano de contrato",
            "Incluir benefícios sociais obrigatórios para as comunidades vizinhas"
        ],
        "correta": "Provar que as reduções só ocorreriam devido aos créditos do projeto",
        "explicacao": "Se as emissões seriam evitadas de qualquer forma por exigência legal ou viabilidade financeira normal, o projeto não possui 'adicionalidade'."
    },
    {
        "tema": "🌡️ Química Atmosférica",
        "pergunta": "Como o dióxido de enxofre ($SO_2$) liberado em erupções vulcânicas afeta temporariamente a temperatura global?",
        "opcoes": [
            "Acelera a degradação do metano natural na troposfera baixa",
            "Forma aerossóis de sulfato que refletem a radiação solar ao espaço",
            "Absorve a radiação infravermelha emitida pela superfície terrestre",
            "Reduz drasticamente a formação de nuvens na alta atmosfera"
        ],
        "correta": "Forma aerossóis de sulfato que refletem a radiação solar ao espaço",
        "explicacao": "Os aerossóis de sulfato aumentam o albedo planetário na estratosfera, gerando um efeito de resfriamento temporário (forçante radiativa negativa)."
    },
    {
        "tema": "🏢 Governança e ESG",
        "pergunta": "Qual métrica da metodologia 'Scope 3' de emissões corporativas costuma ser a mais difícil de mensurar com precisão?",
        "opcoes": [
            "O consumo de energia elétrica em instalações industriais próprias",
            "A pegada de emissões associada a toda a cadeia de valor a montante e jusante",
            "A frota de veículos utilitários diretos operados pela própria empresa",
            "O vazamento residual de gases refrigerantes dos sistemas de ar-condicionado"
        ],
        "correta": "A pegada de emissões associada a toda a cadeia de valor a montante e jusante",
        "explicacao": "O Escopo 3 abrange emissões indiretas de fornecedores e do uso final dos produtos por consumidores, o que envolve dados externos complexos."
    },
    {
        "tema": "🌊 Acidificação dos Oceanos",
        "pergunta": "Qual impacto químico direto o aumento da concentração de $CO_2$ dissolvido causa nos oceanos?",
        "opcoes": [
            "Eleva o pH da água, acelerando a proliferação do fitoplâncton",
            "Consome íons carbonato ($CO_3^{2-}$), dificultando a calcificação marinha",
            "Aumenta a salinidade média da superfície em regiões tropicais",
            "Inibe totalmente a solubilidade do oxigênio nas correntes profundas"
        ],
        "correta": "Consome íons carbonato ($CO_3^{2-}$), dificultando a calcificação marinha",
        "explicacao": "A reação do $CO_2$ com a água reduz os íons de carbonato livres, essenciais para corais e moluscos construírem suas conchas e estruturas."
    },
    {
        "tema": "🌳 Ecologia Teórica",
        "pergunta": "A Hipótese do Distúrbio Intermediário prevê que a maior diversidade de espécies em um ecossistema ocorre quando:",
        "opcoes": [
            "Os distúrbios ambientais são completamente eliminados do habitat",
            "A frequência e a intensidade dos distúrbios ocorrem em níveis moderados",
            "A competição interespecífica atinge o seu nível máximo de saturação",
            "Os eventos destrutivos são extremamente severos e recorrentes"
        ],
        "correta": "A frequência e a intensidade dos distúrbios ocorrem em níveis moderados",
        "explicacao": "Distúrbios moderados impedem que poucas espécies dominantes excluam as outras, abrindo espaço sem extinguir as populações locais."
    },
    {
        "tema": "☣️ Ecotoxicologia",
        "pergunta": "Diferente da bioacumulação, o fenômeno da 'Biomagnificação' ecomutagênica se caracteriza por:",
        "opcoes": [
            "Absorção de poluentes através de membranas respiratórias aquáticas",
            "Aumento da concentração de toxinas ao longo dos níveis tróficos",
            "Retenção de metais pesados apenas nos tecidos adiposos vegetais",
            "Rápida degradação celular de pesticidas em organismos bentônicos"
        ],
        "correta": "Aumento da concentração de toxinas ao longo dos níveis tróficos",
        "explicacao": "Na biomagnificação, a concentração de compostos persistentes (como mercúrio) cresce à medida que subimos na cadeia alimentar (predadores do topo)."
    },
    {
        "tema": "🔄 Economia Industrial",
        "pergunta": "Na Simbiose Industrial, uma das abordagens centrais da Ecologia Industrial, qual o principal objetivo?",
        "opcoes": [
            "Substituir matérias-primas por insumos agrícolas biologicamente modificados",
            "Usar efluentes ou resíduos de uma indústria como matéria-prima de outra",
            "Padronizar o consumo de energia renovável entre empresas concorrentes",
            "Certificar a compensação de resíduos plásticos em áreas de preservação"
        ],
        "correta": "Usar efluentes ou resíduos de uma indústria como matéria-prima de outra",
        "explicacao": "Inspirada em ecossistemas naturais, a simbiose industrial conecta empresas para que o resíduo de um processo se torne recurso para outro."
    }
]

# =========================================================
# ESTADO DO JOGO
# =========================================================
if "iniciado" not in st.session_state:
    st.session_state.iniciado = False
if "questao" not in st.session_state:
    st.session_state.questao = 0
if "pontos" not in st.session_state:
    st.session_state.pontos = 0
if "nome" not in st.session_state:
    st.session_state.nome = ""
if "respondida" not in st.session_state:
    st.session_state.respondida = False
if "acertou" not in st.session_state:
    st.session_state.acertou = False
if "respostas_certas" not in st.session_state:
    st.session_state.respostas_certas = 0

# =========================================================
# BARRA LATERAL (DASHBOARD & RANKING)
# =========================================================
with st.sidebar:
    st.header("📊 Dashboard EcoChallenge")
    st.divider()

    if st.session_state.iniciado:
        st.subheader("👤 Jogador Atual")
        st.write(f"**Nome:** {st.session_state.nome}")
        
        total_q = len(perguntas)
        q_atual = min(st.session_state.questao, total_q)
        
        st.metric("🌱 EcoPontos Acumulados", st.session_state.pontos)
        
        if q_atual > 0:
            taxa = (st.session_state.respostas_certas / q_atual) * 100
        else:
            taxa = 0.0
            
        st.metric("🎯 Taxa de Precisão", f"{taxa:.1f}%")
        st.write(f"**Progresso:** {q_atual}/{total_q} desafios")
        st.progress(q_atual / total_q)
    else:
        st.info("💡 Inicie o desafio para acompanhar suas métricas em tempo real.")

    st.divider()
    
    # RANKING REAL
    st.subheader("🏆 Ranking de Participantes")
    
    if len(st.session_state.ranking) > 0:
        df_rank = pd.DataFrame(st.session_state.ranking)
        df_rank = df_rank.sort_values(by=["Pontos", "Tempo (s)"], ascending=[False, True]).reset_index(drop=True)
        df_rank.index += 1
        df_rank.columns = ["Participante", "Pontos", "Tempo (s)"]
        
        st.dataframe(df_rank, use_container_width=True)
    else:
        st.caption("Nenhum participante finalizou o desafio ainda. Seja o primeiro!")

# =========================================================
# TELA INICIAL
# =========================================================
if not st.session_state.iniciado:
    st.title("🌎 EcoChallenge")
    st.subheader("Plataforma de Conhecimento Ambiental")

    st.markdown(
        """
        ### 🧪 Pronto para testar seus conhecimentos?

        Confira os temas presentes no quiz:

        - **Termodinâmica e Matriz Energética**
        - **Química Atmosférica e Geofísica**
        - **Ecotoxicologia e Dinâmica de Ecossistemas**
        - **Mecanismos de Mercado Carbono e Governança ESG**
        """
    )

    nome = st.text_input("👤 Digite seu nome para registrar no Ranking:", placeholder="Ex: Ana Silva")

    if st.button("🌱 INICIAR DESAFIO", use_container_width=True):
        if nome.strip() == "":
            st.warning("⚠️ Digite seu nome para continuar!")
        else:
            st.session_state.nome = nome.strip()
            st.session_state.iniciado = True
            st.session_state.questao = 0
            st.session_state.pontos = 0
            st.session_state.respostas_certas = 0
            st.session_state.respondida = False
            st.session_state.tempo_inicio = time.time()
            st.rerun()

# =========================================================
# QUIZ
# =========================================================
else:
    numero = st.session_state.questao

    # -----------------------------------------------------
    # AINDA EXISTEM PERGUNTAS
    # -----------------------------------------------------
    if numero < len(perguntas):
        pergunta_atual = perguntas[numero]

        st.title("🌎 EcoChallenge")
        st.caption(f"Tema em análise: {pergunta_atual['tema']}")
        st.divider()

        st.markdown(f"### Desafio {numero + 1}: {pergunta_atual['pergunta']}")

        # -------------------------------------------------
        # USUÁRIO AINDA NÃO RESPONDEU
        # -------------------------------------------------
        if not st.session_state.respondida:
            resposta = st.radio(
                "Selecione a alternativa correta:",
                pergunta_atual["opcoes"],
                index=None,
                key=f"resposta_{numero}"
            )

            if st.button("✅ Confirmar e Enviar", use_container_width=True):
                if resposta is None:
                    st.warning("⚠️ Selecione uma alternativa antes de confirmar!")
                else:
                    if resposta == pergunta_atual["correta"]:
                        st.session_state.pontos += 100
                        st.session_state.respostas_certas += 1
                        st.session_state.acertou = True
                    else:
                        st.session_state.acertou = False

                    st.session_state.respondida = True
                    st.rerun()

        # -------------------------------------------------
        # MOSTRA O RESULTADO DA RESPOSTA
        # -------------------------------------------------
        else:
            if st.session_state.acertou:
                st.success("🎉 Resposta correta! +100 EcoPontos computados.")
            else:
                st.error("❌ Resposta incorreta!")
                st.write(f"**Gabarito técnico:** {pergunta_atual['correta']}")

            st.info(f"💡 **Explicando:** {pergunta_atual['explicacao']}")
            st.divider()

            if numero + 1 < len(perguntas):
                if st.button("➡️ Próxima Questão", use_container_width=True):
                    st.session_state.questao += 1
                    st.session_state.respondida = False
                    st.session_state.acertou = False
                    st.rerun()
            else:
                if st.button("🏆 Finalizar e Ver Desempenho", use_container_width=True):
                    st.session_state.questao += 1
                    
                    tempo_fim = time.time()
                    tempo_total = round(tempo_fim - st.session_state.tempo_inicio, 1)
                    
                    st.session_state.ranking.append({
                        "Participante": st.session_state.nome,
                        "Pontos": st.session_state.pontos,
                        "Tempo (s)": tempo_total
                    })
                    st.rerun()

    # =====================================================
    # RESULTADO FINAL
    # =====================================================
    else:
        st.title("🏆 Resultado Final")
        st.markdown(f"## Parabéns pelo empenho, {st.session_state.nome}!")

        pontos = st.session_state.pontos
        total_p = len(perguntas) * 100
        acertos = st.session_state.respostas_certas
        
        tempo_usuario = [r["Tempo (s)"] for r in st.session_state.ranking if r["Participante"] == st.session_state.nome][-1]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pontuação Total", f"{pontos} pts")
        with col2:
            st.metric("Aproveitamento", f"{(pontos/total_p)*100:.1f}%")
        with col3:
            st.metric("Tempo de Prova", f"{tempo_usuario} s")

        st.write(f"Você acertou **{acertos} de {len(perguntas)}** questões em **{tempo_usuario} segundos**.")

        st.divider()

        # CLASSIFICAÇÃO
        if pontos == total_p:
            st.success("🥇 NÍVEL: ESPECIALISTA AMBIENTAL")
            st.write("Excelente! Domínio completo dos temas e análises de sistema.")
        elif pontos >= total_p * 0.7:
            st.success("🥈 NÍVEL: ANALISTA AMBIENTAL")
            st.write("Ótimo resultado! Grande compreensão de dinâmicas ecológicas e corporativas.")
        elif pontos >= total_p * 0.4:
            st.warning("🥉 NÍVEL: CONSULTOR")
            st.write("Bom trabalho! Vale a pena continuar explorando alguns conceitos.")
        else:
            st.info("📘 NÍVEL: APRENDIZ ECOLÓGICO")
            st.write("Excelente oportunidade para aprender mais! Continue praticando.")

        st.divider()

        if st.button("🔄 Reiniciar e Tentar Novamente", use_container_width=True):
            st.session_state.iniciado = False
            st.session_state.questao = 0
            st.session_state.pontos = 0
            st.session_state.respostas_certas = 0
            st.session_state.nome = ""
            st.session_state.respondida = False
            st.session_state.acertou = False
            st.rerun()