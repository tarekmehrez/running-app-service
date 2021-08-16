import uuid

from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import UniqueConstraint
from sqlalchemy import func

from app.models.validators import users as users_validator
from app.providers import db
from app.providers import metadata


users_table = Table(
    "users",
    metadata,
    Column("id", String, nullable=False, primary_key=True),
    Column("name", String, nullable=True),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
    UniqueConstraint("email", name="user_email_unique"),
)

agents_table = Table(
    "agents",
    metadata,
    Column("id", String, nullable=False, primary_key=True),
    Column("name", String, nullable=True),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
    UniqueConstraint("email", name="agents_email_unique"),
)


admins_table = Table(
    "admins",
    metadata,
    Column("id", String, nullable=False, primary_key=True),
    Column("name", String, nullable=True),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
    UniqueConstraint("email", name="admins_email_unique"),
)

USER_TABLES_DICT = {
    users_validator.UserType.USER: users_table,
    users_validator.UserType.AGENT: agents_table,
    users_validator.UserType.ADMIN: admins_table,
}


class UserModel:
    @staticmethod
    async def list(
        user_type: users_validator.UserType,
        page: int = None,
        page_count: int = None,
    ) -> users_validator.UsersPaginate:
        """
        fetch user table corresponding to type
        get users and remove password from returned records
        return a paginated list for a given page number and count
        """
        table = USER_TABLES_DICT[user_type]

        list_query = table.select()
        list_query = UserModel._paginate_query(page, page_count, list_query)
        users_fetched = await db.fetch_all(query=list_query)

        users_results = []
        for user in users_fetched:
            user_dict = dict(user.__dict__["_row"])
            user_dict.pop("password")
            users_results.append(user_dict)

        users_list = users_validator.UsersPaginate(results=users_results)
        return users_list

    @staticmethod
    def _paginate_query(page: int, page_count: int, query):
        if page and page_count:
            limit = page_count
            offset = (page - 1) * limit
            query = query.limit(limit).offset(offset)
        return query

    @staticmethod
    async def insert(
        user: users_validator.UserSignup,
        user_type: users_validator.UserType,
    ) -> users_validator.UsersDB:
        """
        fetch user table corresponding to type
        create a new uid
        insert new user
        """
        table = USER_TABLES_DICT[user_type]
        uid = str(uuid.uuid4())
        query = table.insert().returning(*[col for col in table.c])
        user = user.dict()
        user["id"] = uid
        created_user = await db.fetch_one(query=query, values=user)

        created_user = users_validator.UsersDB(**created_user, exclude_unset=True)
        return created_user

    @staticmethod
    async def get(
        user_type: users_validator.UserType, id: str = None, email: str = None
    ) -> users_validator.UsersDB:
        """
        fetch user table corresponding to type
        fetch user based on email or id
        """
        if not (id or email):
            raise ValueError("Missing id or email as input to the user get function")

        table = USER_TABLES_DICT[user_type]

        if email:
            query = table.select().where(table.c.email == email)

        if id:
            query = table.select().where(table.c.id == id)

        user = await db.fetch_one(query=query)

        if not user:
            return None
        else:
            return users_validator.UsersDB(**user, exclude_unset=True)
