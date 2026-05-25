import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="Optimiseur Cross-Sell IA Pro", page_icon="💸", layout="wide")

# Masquer la sidebar par défaut et injecter le style épuré
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

# -------------------------
# CONFIGURATION PAYPAL
# -------------------------
PAYPAL_CLIENT_ID = "DEMO"  # Mettez votre Client ID ici plus tard
PAYPAL_PLAN_ID = "DEMO"    # Mettez votre Plan ID ici plus tard

# -------------------------
# GESTION DE L'ACCÈS (SESSION STATE)
# -------------------------
if "est_abonne" not in st.session_state:
    st.session_state.est_abonne = False

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = ""

# -------------------------
# INTERFACE SÉCURISÉE
# -------------------------
st.title("💸 Optimiseur d'Offres Cross-Sell & Bundles — Version Pro")

# CAS 1 : L'UTILISATEUR N'A PAS PAYÉ
if not st.session_state.est_abonne:
    st.warning("🔒 Cette application est réservée aux membres de la version Premium.")
    
    col_offre, col_connexion = st.columns(2, gap="large")
    
    with col_offre:
        st.subheader("🚀 Débloquez l'IA pour 30 $/mois")
        st.write("Augmentez instantanément la valeur moyenne de vos paniers (AOV). L'IA conçoit des offres groupées et des stratégies de vente croisée psychologiques pour multiplier vos profits sans dépenser un dollar de plus en publicité.")
        st.write("Le paiement est entièrement sécurisé par **PayPal**.")
        
        if PAYPAL_CLIENT_ID == "DEMO":
            paypal_html = """
            <a href="https://paypal.com" target="_blank" style="text-decoration: none;">
                <div style="background-color: #ffc439; color: #003087; text-align: center; 
                            padding: 12px; font-family: Arial, sans-serif; font-weight: bold; 
                            border-radius: 4px; max-width: 300px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    🟨 S'abonner avec PayPal (Démo)
                </div>
            </a>
            """
        else:
            paypal_html = f"""
            <div id="paypal-button-container-fixed" style="max-width: 350px; margin-top: 20px;"></div>
            <script src="https://paypal.com{PAYPAL_CLIENT_ID}&vault=true&intent=subscription" data-sdk-integration-source="button-factory"></script>
            <script>
              paypal.Buttons({{
                  style: {{ shape: 'rect', color: 'gold', layout: 'vertical', label: 'subscribe' }},
                  createSubscription: function(data, actions) {{
                    return actions.subscription.create({{ 'plan_id': '{PAYPAL_PLAN_ID}' }});
                  }},
                  onApprove: function(data, actions) {{
                    alert('Abonnement réussi ! ID : ' + data.subscriptionID);
                  }}
              }}).render('#paypal-button-container-fixed');
            </script>
            """
        
        components.html(paypal_html, height=150, scrolling=False)
        
    with col_connexion:
        st.subheader("🔑 Déjà abonné ?")
        st.write("Connectez-vous pour activer vos accès.")
        email = st.text_input("Adresse e-mail")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter", use_container_width=True):
            if email == "test@client.com" and mot_de_passe == "access30":
                st.session_state.est_abonne = True
                st.success("Accès accordé !")
                st.rerun()
            else:
                st.error("Identifiants incorrects ou abonnement PayPal inactif.")

# CAS 2 : L'UTILISATEUR EST ABONNÉ -> ACCÈS COMPLET
else:
    st.write("✨ **Bienvenue dans votre espace Premium.** Votre abonnement est actif.")
    if st.button("🚪 Se déconnecter", key="logout"):
        st.session_state.est_abonne = False
        st.rerun()
        
    st.write("---")

    with st.container(border=True):
        col_prod, col_strat = st.columns(2)
        
        with col_prod:
            produit_principal = st.text_input("Quel est votre produit phare ?", placeholder="Ex: Crème hydratante bio, Montre de sport minimaliste...")
            prix_principal = st.number_input("Prix de vente de ce produit ($)", min_value=1.0, value=40.0)
            details = st.text_area("Description ou bénéfice clé", placeholder="Ex: Élimine les imperfections en 7 jours, protège de la pollution...")
            
        with col_strat:
            type_offre = st.selectbox("Type d'optimisation voulu", [
                "🔥 Le Bundle Parfait (Lots de produits complémentaires)", 
                "⚡ L'Upsell Post-Achat (Augmenter la quantité / Version supérieure)", 
                "🤝 Le Cross-Sell de Panier (Petits accessoires indispensables à ajouter)"
            ])
            agressivite = st.select_slider("Niveau d'incitation à l'achat", options=["Discret", "Équilibré", "Très Persuasif"])

        generer = st.button("🚀 Générer la Stratégie de Vente Rentable", use_container_width=True)

    if generer:
        if not API_KEY:
            st.error("⚠️ Erreur : La clé GROQ_API_KEY est manquante dans les Secrets du serveur.")
        elif not produit_principal:
            st.error("⚠️ Veuillez indiquer votre produit phare.")
        else:
            with st.spinner("L'IA de Groq calcule et rédige vos offres à forte conversion..."):
                try:
                    client = Groq(api_key=API_KEY)
                    
                    prompt_systeme = """Tu es un expert mondial en optimisation du panier moyen (AOV) et en ingénierie des offres pour le e-commerce.
                    Tu dois structurer une réponse en Markdown extrêmement claire et actionnable contenant :
                    1. **L'Idée d'offre phare** (Nom du pack / bundle et stratégie de prix psychologique conseillée).
                    2. **Les produits complémentaires exacts à ajouter** (Ce qu'il faut proposer en plus et pourquoi).
                    3. **Le Script de vente / Texte de l'offre** (Le message exact à afficher dans l'application ou sur la page de paiement pour pousser au clic).
                    Ne fais aucun blabla avant ou après, va directement au fait pour faire gagner de l'argent au commerçant."""

                    reponse = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": prompt_systeme},
                            {"role": "user", "content": f"Produit principal : '{produit_principal}' vendu à {prix_principal}$. Détails : '{details}'. Type de stratégie demandée : {type_offre}. Niveau d'incitation : {agressivite}."}
                        ],
                        temperature=0.7
                    )
                    
                  calendrier_genere = reponse.choices[0].message.content  # Ligne corrigée  (Adapte le nom de la variable selon l'app)
                    st.success("✨ Votre stratégie pour exploser le panier moyen est prête !")
                    st.markdown(strategie_generee)
                    st.text_area("Copier la stratégie brute :", value=strategie_generee, height=300)

                except Exception as e:
                    st.error(f"Erreur technique Groq : {str(e)}")
