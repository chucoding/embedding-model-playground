import streamlit as st
from app.vector_store import VectorStore, EmbeddingType

st.set_page_config(
    page_title="Embedding Model Test Playground",
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

st.title("Embedding Model Test Playground")

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

# Document management section
st.header("Document Management")

# Add custom CSS for alignment
st.markdown("""
    <style>
        .stButton {
            padding-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Display all documents
all_documents = st.session_state.vector_store.get_all_documents()
if all_documents:
    with st.expander(f"📚 Documents ({len(all_documents)})", expanded=True):
        for idx, (doc_id, doc) in enumerate(all_documents, 1):
            col1, col2 = st.columns([0.95, 0.05])
            with col1:
                st.markdown(f"""
                    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                        <strong>Content:</strong><br>
                        {doc['text']}
                    </div>
                """, unsafe_allow_html=True)
                
                if 'metadata' in doc and doc['metadata']:
                    st.markdown(f"""
                        <div style='background-color: #e6f3ff; padding: 10px; border-radius: 5px; margin: 5px 0;'>
                            <strong>Metadata:</strong><br>
                            {doc['metadata']}
                        </div>
                    """, unsafe_allow_html=True)
                    
            with col2:
                if st.button("🗑️", key=f"delete_{idx}"):
                    try:
                        st.session_state.vector_store.delete_document(doc_id)
                        st.success("Document deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting document: {str(e)}")

# Add new document
st.subheader("Add New Document")
new_doc = st.text_area("Document Content", height=100)

# Add metadata input
with st.expander("📝 Metadata (Optional)", expanded=False):

    if 'metadata_pairs' not in st.session_state:
        st.session_state.metadata_pairs = [{'key': '', 'value': ''}]
    
    for i, pair in enumerate(st.session_state.metadata_pairs):
        col1, col2, col3 = st.columns([0.4, 0.4, 0.2])
        with col1:
            st.session_state.metadata_pairs[i]['key'] = st.text_input(
                "Key", 
                value=pair['key'],
                key=f"key_{i}"
            )
        with col2:
            st.session_state.metadata_pairs[i]['value'] = st.text_input(
                "Value", 
                value=pair['value'],
                key=f"value_{i}"
            )
        with col3:
            st.markdown("<div style='padding-top: 15px;'>", unsafe_allow_html=True)
            if st.button("🗑️", key=f"remove_meta_{i}"):
                st.session_state.metadata_pairs.pop(i)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("➕ Add Metadata Field"):
        st.session_state.metadata_pairs.append({'key': '', 'value': ''})
        st.rerun()

if st.button("Add Document"):
    if new_doc:
        try:

            metadata = {
                pair['key']: pair['value'] 
                for pair in st.session_state.metadata_pairs 
                if pair['key'] and pair['value']
            }
            
            metadata = metadata if metadata else None
            
            st.session_state.vector_store.add_documents(new_doc, metadata)
            st.rerun()
        except Exception as e:
            st.error(f"Error adding document: {str(e)}")
    else:
        st.warning("Please enter document content.")

# Search area
st.header("Search")
st.markdown("""
### About Search
- Uses `similarity_search_with_score` method from InMemoryVectorStore
- Returns documents sorted by similarity score (cosine similarity)
- Higher score means more relevant to the query
- Results are ranked based on pure semantic similarity
""")
search_query = st.text_input("Enter your search query:")

# Expander for filter settings
with st.expander("🔍 Search Filter (Optional)", expanded=False):
    st.markdown("""
    Please write the filter function in Python code. Example:
    ```python
    def filter_function(doc):
        return doc.metadata.get("key") == "value"
    ```
    """)
    filter_code = st.text_area("Filter Function", height=150, 
        value="def filter_function(doc):\n    return True")

if st.button("Search"):
    if search_query:
        try:
            filter_function = None
            if filter_code and filter_code.strip() != "def filter_function(doc):\n    return True":
                local_dict = {}
                exec(filter_code, globals(), local_dict)
                filter_function = local_dict['filter_function']
            
            # Execute search
            search_results = st.session_state.vector_store.search(
                query=search_query, 
                k=3, 
                filter=filter_function
            )

            st.session_state.search_results = search_results
            st.session_state.search_query = search_query
        except Exception as e:
            st.error(f"Error during search: {str(e)}")
    else:
        st.warning("Please enter a search query.")

if 'search_results' in st.session_state and st.session_state.search_results:
    st.success(f"Search results for: {st.session_state.search_query}")
    for idx, doc in enumerate(st.session_state.search_results, 1):
        with st.container():
            st.markdown(f"### 🏆 Rank {idx} (Similarity Score: {doc.metadata['score']:.2f})")
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 11px; border-radius: 5px; margin: 10px 0;'>
                {doc.metadata['page_content']}
            </div>
            """, unsafe_allow_html=True)
            
            if hasattr(doc, 'metadata') and doc.metadata:
                st.markdown(f"""
                <div style='background-color: #e6f3ff; padding: 10px; border-radius: 5px; margin: 5px 0;'>
                    <strong>Metadata:</strong><br>
                    {doc.metadata}
                </div>
                """, unsafe_allow_html=True)

# Retrive area
st.header("Retrieve")
st.markdown("""
### About Retrieve
- Uses MMR (Maximal Marginal Relevance) search algorithm
- Balances between relevance and diversity in results
- Helps avoid redundant or very similar results
- Useful when you want diverse perspectives on a topic
""")
retrieve_query = st.text_input("Enter your retrieve query:")

# Add metadata filter for Retrieve
with st.expander("🔍 Retrieve Filter (Optional)", expanded=False):
    st.markdown("""
    Please write the filter function in Python code. Example:
    ```python
    def filter_function(doc):
        return doc.metadata.get("key") == "value"
    ```
    """)
    retrieve_filter_code = st.text_area("Filter Function", height=150, 
        value="def filter_function(doc):\n    return True",
        key="retrieve_filter")

if st.button("Retrive"):
    if retrieve_query:
        try:
            filter_function = None
            if retrieve_filter_code and retrieve_filter_code.strip() != "def filter_function(doc):\n    return True":
                local_dict = {}
                exec(retrieve_filter_code, globals(), local_dict)
                filter_function = local_dict['filter_function']
            
            # Execute retrive
            retrieve_results = st.session_state.vector_store.retrive(
                query=retrieve_query, 
                k=3, 
                filter=filter_function
            )
            st.session_state.retrieve_results = retrieve_results
            st.session_state.retrieve_query = retrieve_query
        except Exception as e:
            st.error(f"Error during retrieve: {str(e)}")
    else:
        st.warning("Please enter a retrieve query.")

if 'retrieve_results' in st.session_state and st.session_state.retrieve_results:
    st.success(f"Retrieve results for: {st.session_state.retrieve_query}")
    for idx, doc in enumerate(st.session_state.retrieve_results, 1):
        with st.container():
            st.markdown(f"### 🏆 Rank {idx}")
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                {doc.page_content}
            </div>
            """, unsafe_allow_html=True)
            
            if hasattr(doc, 'metadata') and doc.metadata:
                st.markdown(f"""
                <div style='background-color: #e6f3ff; padding: 10px; border-radius: 5px; margin: 5px 0;'>
                    <strong>Metadata:</strong><br>
                    {doc.metadata}
                </div>
                """, unsafe_allow_html=True)
