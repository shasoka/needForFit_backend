from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):

    def dump_dict(self):
        row_dict = self.__dict__.copy()
        del row_dict['_sa_instance_state']
        return row_dict

    def exclude(self, field: str):
        row_dict = self.dump_dict()
        del row_dict[field]
        return row_dict
