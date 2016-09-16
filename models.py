"""This module contains all the class definitions for the subject entities
that we will be persisting using peewee
"""
__author__ = 'eljefeloco'

from peewee import *

# A single database should do us.
escort_db = SqliteDatabase("escorts.db")



class BaseModel(Model):
    """Base Class for all persisted objects.  Ensures they wil inherit the
    database connection, probably other stuff we can include here
    """
    class Meta:
        """Ensure db connection inherited"""
        database = escort_db

class Location(BaseModel):
    """Defines the locations/incalls that a service is currently using and placing girls at"""
    name = CharField()        # Miami
    description = TextField() # South Beach Luxury Incall
    directions = TextField()  # I-95/Golden Glades exit



class Escort(BaseModel):
    """Defines an escort and the relationships she has with other entities
    Contains the following attributes:
    name            height      weight      hair_color  eyes
    vitals          bust        implants    tattoos     piercings   language
    brand_text      nationality ethnicity   description ad_text
    featured        available   vacation    new_girl    gfe
    pse             located_at

    null    index   unique  default
    """
    name = CharField(unique=True)
    height = CharField(null=True)
    weight = SmallIntegerField(null=True)
    hair_color = CharField(null=True)
    eyes = CharField(null=True)
    vitals = CharField(null=True)
    bust = CharField(null=True)
    implants = BooleanField(null=True)
    tattoos = CharField(null=True,default=True)
    piercings = CharField(null=True, default=False)
    language = CharField(default='English')
    brand_text = CharField()
    nationality = CharField(null=True)
    ethnicity = CharField(null=True)
    description = TextField()
    ad_text = TextField()
    # Flags
    featured = BooleanField(default=False)
    available = BooleanField(default=False)
    vacation = BooleanField(default=False)
    new_girl = BooleanField(default=True)
    gfe = BooleanField(default=True)
    pse = BooleanField(default=False)
    # Foreign Keys
    located_at = ForeignKeyField(Location,related_name="takes visits at", null=True)



def initialise():
    """Just scaffolding for persistence.  Create the database etc."""
    escort_db.connect()
    escort_db.create_tables([Escort, Location],safe=True)


def main():
    """This is just a stub that will drive saving and loading of the models
    :return: None
    """
    initialise()

    stella = Escort(name='Stella',height="5'0",weight=105,eyes='Blue',
                    brand_text='Best a Man can Get',implants=True,new_girl=True,
                    gfe=True,
                    description="""
                    Stella is out eastern european lovely.  She is new with us but has promised to
                    be the best a man can get""", ad_text="Ad text",
                    bust='34D')
    robin  = Escort(name='Robin',height="5'1",weight=115,eyes='Green',
                    brand_text='British Spinner',implants=False,new_girl=True,
                    gfe=True,
                    pse=True, ad_text="Robins ad text",
                    description="""Robin has recently arrived on these shores and has brought
                    her English attitude of refinement and couture with her.   She is a
                    bright girl, who will quickly put you at ease and then some.""",
                    bust='32C')

    aloc = Location(name="FTL",description="A Descr",directions="Go West")

    allfields= Escort(name='Robinallfields',height="5'1",weight=115,eyes='Green',
                    brand_text='British Spinner',implants=False,new_girl=True,
                    gfe=True,
                    pse=True,
                    description="""Robin has recently arrived on these shores and has brought
                    her English attitude of refinement and couture with her.   She is a
                    bright girl, who will quickly put you at ease and then some.""",
                    bust='32C',located_at=aloc, hair_color="Blonde",vitals="32-34-32",tattoos=False,
                      piercings=False, language="Englsh", nationality='Russian', ethnicity='AA',
                      ad_text="Get it!",featured=True,available=True,vacation=False)
    try:
        new_girl = Escort.create(name='Naomi',height="5'3",weight=95,eyes='Green',
                        brand_text='AA Spinner',implants=False,new_girl=True,
                        gfe=True,
                        pse=True,
                        description="""Naomi has big tits and goes bareback""",
                        bust='36C',located_at=aloc, hair_color="Black",vitals="36-34-32",tattoos=False,
                          piercings=False, language="Englsh", nationality='American', ethnicity='AA',
                          ad_text="Get it bare!",featured=False,available=True,vacation=False)


        robin.save()
        stella.save()
        aloc.save()
        allfields.save()
    except IntegrityError:
        pass
    else:
        raise


    for escort in Escort.select():
        print(escort.name, escort.featured)
        if escort.featured==True:
            escort.featured=False
        escort.save()

    escort_db.commit()
    escort_db.close()

    # finished
    return
if __name__ == '__main__':
   main()
else:
    print(__name__, __doc__)