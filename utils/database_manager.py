from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from  sqlalchemy import Column, Integer, String, Float, Boolean
import os

Base = declarative_base()

class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True)
    show_name = Column(String, unique=True)
    spoonacular_name = Column(String)
    spoonacular_id = Column(Integer)
    image = Column(String)
    
    def __repr__(self):
        return "<Ingredient(show_name='%s', spoonacular_name='%s', image='%s')>" % (self.show_name, self.spoonacular_name, self.image)

class Recipe(Base):
    __tablename__ = 'recipe'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    spoonacular_id = Column(Integer, unique=True)
    image = Column(String)
    opened = Column(Boolean)
    
    
    def __repr__(self):
        return "<Recipe(name='%s', image='%s')>" % (self.name, self.image)


class DatabaseManager:
    def __init__(self):
        # Create Engine
        basedir = os.path.abspath(os.path.dirname(__file__))
        path_db = os.path.join(basedir, 'whatsinmyfridge.db')
        engine = create_engine(f"sqlite:///{path_db}", echo=False)
        Base.metadata.create_all(bind=engine)
        self.Session = sessionmaker(bind=engine)
    
    def add_recipe(self, name:str, spoonacular_id: int, image: str, opened: bool):
        
        # Open Session
        session = self.Session()        
        # Check if already exist
        to_check = session.query(Recipe).filter_by(spoonacular_id=spoonacular_id).first()
        if to_check is not None:
            session.close()
            return       
        # Add new Recipe
        recipe = Recipe()
        recipe.name = name
        recipe.spoonacular_id = spoonacular_id
        recipe.image = image
        recipe.opened = opened
        # Update Database
        session.add(recipe)
        session.commit()
        # Close Session
        session.close()
        
    def add_ingredient(self, show_name, spoonacular_name, spoonacular_id, image):
        # Open Session
        session = self.Session()
        ingredient = Ingredient()
        ingredient.show_name = show_name
        ingredient.image = image
        ingredient.spoonacular_name = spoonacular_name
        ingredient.spoonacular_id = spoonacular_id
        # Update Database
        session.add(ingredient)
        session.commit()
        # Close Session
        session.close()
    
    def get_all_ingredients(self):
        # Open Session
        session = self.Session()
        ingredients = session.query(Ingredient).all()   
        # Close Session
        session.close()
        return ingredients

    def delete_ingredient(self, show_name):
        # Open Session
        session = self.Session()
        to_delete = session.query(Ingredient).filter_by(show_name=show_name).first() 
        session.delete(to_delete)
        session.commit()
        # Close Session
        session.close()