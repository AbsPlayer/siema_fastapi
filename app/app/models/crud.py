class Crud:
    @classmethod
    def read(cls, db_session):
        return db_session.query(cls).all()

    @classmethod
    def exists(cls, db_session, _id):
        return db_session.query(cls).get(_id) is not None

    @classmethod
    def read_by_id(cls, db_session, _id):
        return db_session.query(cls).get(_id)

    def save(self, db_session):
        if self.id is None:
            db_session.add(self)
        db_session.commit()
        db_session.refresh(self)
        return self

    def destroy(self, db_session):
        db_session.delete(self)
        db_session.commit()
        return self
