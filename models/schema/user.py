from sqlalchemy import String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(255))
    phone:Mapped[str] = mapped_column(String(100))
    email:Mapped[str] = mapped_column(String(255))
    address:Mapped[str] = mapped_column(String(255))
    list:Mapped[str] = mapped_column(String(255))
    country:Mapped[str] = mapped_column(String(100))
    
    def __repr__(self):
        return f"({self.id}) {self.name} {self.phone}\n"
    
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' }