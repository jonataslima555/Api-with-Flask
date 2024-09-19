from peewee import CharField, SqliteDatabase, Model, ForeignKeyField

db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField(unique=True)
    password = CharField()

    @classmethod
    def create_user(cls, name, password):
        with db.atomic():
            return User.create(
                name=name,
                password=password
            )


class Books(BaseModel):
    user = ForeignKeyField(User, backref='users')
    name = CharField()
    
    @classmethod
    def create_book(cls, user, name):
        with db.atomic():
            return Books.create(
                user=user,
                name=name
            )

with db.atomic():
    db.create_tables([User, Books])

#User.create_user('jon', '123')
#Books.create_book(1, 'Livro 1')