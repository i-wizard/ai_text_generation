from app.models.generated_text import GeneratedText
from sqlalchemy.orm import Session


class GeneratedTextRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_generated_text(self, user_id, prompt, response):
        new_text = GeneratedText(user_id=user_id, prompt=prompt, response=response)
        self.db_session.add(new_text)
        self.db_session.commit()
        return new_text

    def get_generated_text_by_id(self, text_id):
        return self.db_session.get(GeneratedText, text_id)

    def get_generated_text_by_id_and_user(self, text_id, user_id):
        return (
            self.db_session.query(GeneratedText)
            .filter_by(user_id=user_id, id=text_id)
            .first()
        )

    def get_all_texts_by_user(self, user_id):
        return self.db_session.query(GeneratedText).filter_by(user_id=user_id).all()

    def update_generated_text(self, text_id, user_id, new_response):
        generated_text = self.get_generated_text_by_id_and_user(text_id, user_id)
        if generated_text:
            generated_text.response = new_response
            self.db_session.commit()
        return generated_text

    def delete_generated_text(self, text_id, user_id):
        generated_text = self.get_generated_text_by_id_and_user(text_id, user_id)
        if generated_text:
            self.db_session.delete(generated_text)
            self.db_session.commit()
            return True
        return False
