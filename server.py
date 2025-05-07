import streamlit as st
from app.vector_store import VectorStore, EmbeddingType

st.set_page_config(
    page_title="Vector DB Test",
    page_icon="🔍",
    layout="wide"
)

# Hide all menus and buttons using CSS
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        .stToolbar {display:none;}
        .stApp [data-testid="stToolbar"] {display:none;}
    </style>
""", unsafe_allow_html=True)

st.title("Vector DB Test Application")

# Initialize VectorStore
embedding_type = st.selectbox(
    "Select embedding type",
    options=[e.value for e in EmbeddingType],
    format_func=lambda x: x.capitalize()
)

if 'vector_store' not in st.session_state or st.session_state.get('current_embedding_type') != embedding_type:
    st.session_state.vector_store = VectorStore(embedding_type=EmbeddingType(embedding_type))
    st.session_state.current_embedding_type = embedding_type
    st.session_state.vector_store.load()

# Document input area
st.header("Document Input")
col1, col2, col3 = st.columns(3)

with col1:
    doc1 = st.text_area("Document 1", height=200)
with col2:
    doc2 = st.text_area("Document 2", height=200)
with col3:
    doc3 = st.text_area("Document 3", height=200)

# Document load button
if st.button("Load Documents"):
    if doc1 or doc2 or doc3:
        try:
            # 문서들을 리스트로 모음
            documents = [doc for doc in [doc1, doc2, doc3] if doc]

            # VectorStore에 문서 추가
            st.session_state.vector_store.add_documents(documents)
            st.session_state.documents_loaded = True
        except Exception as e:
            st.error(f"Error loading documents: {str(e)}")
    else:
        st.warning("Please enter at least one document.")

# 문서 로드 상태 표시
if st.session_state.get('documents_loaded', False):
    st.success("Documents loaded successfully!")

# Search area
st.header("Search")
user_query = st.text_input("Enter your search query:")

if st.button("Search"):
    if user_query:
        st.write("Processing your query...")
        try:
            # Execute search
            results = st.session_state.vector_store.search(query=user_query, k=3)

            # Display results
            if results:
                st.success("Search completed!")
                for idx, doc in enumerate(results, 1):
                    with st.container():
                        st.markdown(f"### 🏆 Rank {idx} (Similarity Score: {doc.metadata['score']:.2f})")
                        st.markdown(f"""
                        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                            {doc.metadata['page_content']}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No relevant results found.")
        except Exception as e:
            st.error(f"Error during search: {str(e)}")
    else:
        st.warning("Please enter a search query.")