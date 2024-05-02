import csv

import sqlalchemy
from src.models.schemas.chat import MessagesResponse
from pymilvus import db
from datasets import load_dataset

from src.models.db.chat import ChatHistory
from src.config.settings.const import UPLOAD_FILE_PATH
from src.repository.ai_models import ai_model
from src.repository.rag.base import BaseRAGRepository
from src.repository.vector_database import vector_db
from src.repository.conversation import ConversationWithSession, conversations

class RAGChatModelRepository(BaseRAGRepository):
    async def load_model(self, session_id: int, model_name: str) -> bool:
        # Init model with input model_name
        try:
            ai_model.initialize_model(model_name)
            pass
        except Exception as e:
            print(e)
            return False
        return True

    def search_context(self, query, n_results=1):
        query_embeddings = ai_model.encode_string(query)
        print(query_embeddings.shape)
        return vector_db.search(data=query_embeddings, n_results=n_results)

    async def get_response(self, session_id: int, input_msg: str, chat_repo) -> str:

        if session_id not in conversations:
            conversations[session_id] = ConversationWithSession(session_id, chat_repo)
            await conversations[session_id].load()
        con = conversations[session_id]
        con.conversation.add_message({"role": "user", "content": input_msg})
        context = self.search_context(input_msg)
        answer = ai_model.generate_answer(con,context)
        print(f'ai generate_answer value:{answer}')
        # TODO stream output
        return answer

    async def load_csv_file(self, file_name: str, model_name: str) -> bool:
        # read file named file_name and convert the content into a list of strings @Aisuko
        print(file_name)
        print(model_name)
        data = []
        with open(UPLOAD_FILE_PATH + file_name, "r") as file:
            # Create a CSV reader
            reader = csv.reader(file)
            # Iterate over each row in the CSV
            print(f"reader Data:{reader}")
            for row in reader:
                # Add the row to the list
                data.extend(row)
        print(f"load_csv_file data_row:{data}")                
        embedding_list = ai_model.encode_string(data)
        vector_db.insert_list(embedding_list, data)

        return True



    async def load_data_set(self, dataset_name: str)-> str:
        reader_dataset=load_dataset(dataset_name)
        print(f"reader_dataset：{reader_dataset}")
        data_row = []
        for row in reader_dataset:
            data_row.extend(row)
            res=reader_dataset['train'].to_pandas().to_numpy()
        print(f"data_row:{data_row}")
        print(f"res:{data_row}")
        vector_db.insert_list(res, data_row)
        return True