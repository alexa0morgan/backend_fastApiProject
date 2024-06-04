from sqlalchemy import create_engine
import models.brand
import models.car
import models.user

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
