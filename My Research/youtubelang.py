import argparse
from langchain_community.document_loaders import YoutubeLoader
from langchain.indexes import VectorstoreIndexCreator
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from langchain_huggingface import HuggingFaceEmbeddings
# from llama_index.core import BaseQueryEngine
from langchain.llms.openai import OpenAI


def extract_youtube_id(youtube_url):             #youtube_url
   return youtube_url.split("v=")[-1]


def load_and_vectorize(youtube_url_id ) :
   loader = YoutubeLoader.from_youtube_url(f"https://www.youtube.com/watch?v={youtube_url_id}" , add_video_info = False )
   docs = loader.load()
   embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
   index = VectorstoreIndexCreator(embedding=embeddings)
   return index.from_documents(docs)

def query_index(index , query , llm) :
     return index.query(query , llm=llm)

def main() :
    parser = argparse.ArgumentParser(description = "Query a youtube video:")
    parser.add_argument("-url", type=str, help="the url from youtube video")
    args = parser.parse_args()
    youtube_url_id = extract_youtube_id(args.url)
    index = load_and_vectorize(youtube_url_id)
    llm = OpenAI(temperature=0)
    query = input("what is question?(enter ‘quit’ to exit)")

    while True :

        response = query_index(index , query)
        print(f"Answer: {response}")
        query = input("what is your question?(enter ‘quit’ or ‘q’ to exit)")
        if query == "quit" or query == "q":
           break

if __name__ == "__main__" :
    # url = "https://www.youtube.com/watch?v=TsfLm5iiYb4"
    # print(extract_youtube_id(url))
    # youtube_url_id = extract_youtube_id(url)
    # print(load_and_vectorize(youtube_url_id ))
    main()


