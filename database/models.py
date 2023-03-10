import peewee


db = peewee.SqliteDatabase('database/history.db')


class BaseModel(peewee.Model):
    id = peewee.PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Command(BaseModel):
    telegram_id = peewee.CharField()
    command = peewee.CharField()
    date_time = peewee.DateTimeField()

    class Meta:
        db_table = 'commands'


class Hotel(BaseModel):
    name = peewee.CharField()
    url = peewee.CharField()
    command_id = peewee.ForeignKeyField(Command)

    class Meta:
        db_table = 'hotels'
