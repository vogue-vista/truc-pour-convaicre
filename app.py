import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="Optimiseur Cross-Sell IA Pro", page_icon="💸", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
@import url('https://googleapis.com');
html, body, div, p, h1, h2, h3, h4, h5, h6, span {
    font-family: 'Poppins', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

PAYPAL_CLIENT_ID = "DEMO"
PAYPAL_PLAN_ID = "DEMO"

if "est_abonne" not in st.session_state:
    st.session_state.est_abonne = False

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = ""

st.title("💸 Optimiseur d'Offres Cross-Sell & Bundles")

if not st.session_state.est_abonne:
    st.warning("🔒 Application réservée aux membres Premium.")
    col_offre, col_connexion = st.columns(2, gap="large")
    
    with col_offre:
        st.subheader("🚀 Débloquez l'IA pour 30 $/mois")
        st.write("Augmentez l'AOV de vos paniers grâce à des stratégies de bundles psychologiques.")
        paypal_html = """
        <a href="https://paypal.com" target="_blank" style="text-decoration: none;">
            <div style="background-color: #ffc439; color: #003087; text-align: center; padding: 12px; font-weight: bold; border-radius: 4px; max-width: 300px;">
                🟨 S'abonner avec PayPal (Démo)
            </div>
        </a>
        """
        components.html(paypal_html, height=150, scrolling=False)
        
    with col_connexion:
        st.subheader("🔑 Déjà abonné ?")
        email = st.text_input("Adresse e-mail")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter", use_container_width=True):
            if email == "test@client.com" and mot_de_passe == "access30":
                st.session_state.est_abonne = True
                st.rerun()
            else:
                st.error("Identifiants incorrects.")
else:
    st.write("✨ Espace Premium Actif.")
    if st.button("🚪 Se déconnecter"):
        st.session_state.est_abonne = False
        st.rerun()

    with st.container(border=True):
        col_prod, col_strat = st.columns(2)
        with col_prod:
            produit_principal = st.text_input("Produit phare", placeholder="Ex: Crème hydratante bio...")
            prix_principal = st.number_input("Prix ($)", min_value=1.0, value=40.0)
            details = st.text_area("Description courte", placeholder="Bénéfices clés...")
        with col_strat:
            type_offre = st.selectbox("Stratégie", ["🔥 Le Bundle Parfait", "⚡ L'Upsell Post-Achat", "🤝 Le Cross-Sell de Panier"])
            agressivite = st.select_slider("Persuasion", options=["Discret", "Équilibré", "Très Persuasif"])

        generer = st.button("🚀 Générer la Stratégie", use_container_width=True)

    if generer:
        if not API_KEY:
            st.error("⚠️ Clé manquante.")
        elif not produit_principal:
            st.error("⚠️ Indiquez le produit.")
        else:
            with st.spinner("Génération des offres..."):
                try:
                    client = Groq(api_key=API_KEY)
                    prompt_systeme = "Tu es un expert CRO. Rédige une offre de bundle, la liste des produits complémentaires et le script de vente. Pas de blabla, va droit au but."
                    reponse = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": prompt_systeme},
                            {"role": "user", "content": f"Produit: {produit_principal} ({prix_principal}$). Description: {details}. Stratégie: {type_offre}. Force: {agressivite}."}
                        ],
                        temperature=0.7
                    )
                    strategie_generee = reponse.choices[0].message.content
                    st.success("✨ Stratégie prête !")
                    st.markdown(strategie_generee)
                except Exception as e:
                    st.error(f"Erreur : {str(e)}")
