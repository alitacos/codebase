 def install_and_set_huggingface_sentence_transformer_model(model_name:str='all-MiniLM-L6-v2'):
    from sentence_transformers import SentenceTransformer, util
    try:
        if not model or not insinstance(model, str) or not model.strip():
            return None
        return SentenceTransformer(model.strip())
    except Exception as e:
        #print(e)
        return None
