"""
Database Module

This module contains all the code to manage the Database

The database is a SQL Database using SQLAlchemy as a  bject Relational Mapper
https://docs.sqlalchemy.org/

"""

from kivy.logger import Logger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from  sqlalchemy import Column, Integer, String, Float, Boolean
import os

Base = declarative_base()

class Ingredient(Base):
    """
    Mapped Class for the Ingredients
    """
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True)
    show_name = Column(String, unique=True)
    spoonacular_name = Column(String)
    spoonacular_id = Column(Integer)
    image = Column(String)
    
    def __repr__(self):
        return "<Ingredient(show_name='%s', spoonacular_name='%s', image='%s')>" % (self.show_name, self.spoonacular_name, self.image)

class Recipe(Base):
    """
    Mapped Class for the Recipes
    """
    __tablename__ = 'recipe'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    spoonacular_id = Column(Integer, unique=True)
    image = Column(String)
    opened = Column(Boolean)
        
    def __repr__(self):
        return "<Recipe(name='%s', image='%s')>" % (self.name, self.image)


class DatabaseManager:
    """
    Database Manager Class
    
    Contaions all the Variables and methods to use the SQL Database
    
    Tha Database will be cointained in the same directory as this script
    
    """
    
    def __init__(self):
        # Create Engine and Session
        basedir = os.path.abspath(os.path.dirname(__file__))
        path_db = os.path.join(basedir, 'whatsinmyfridge.db')
        engine = create_engine(f"sqlite:///{path_db}", echo=False)
        Base.metadata.create_all(bind=engine)
        self.Session = sessionmaker(bind=engine)
    
    def add_recipe(self, name:str, spoonacular_id: int, image: str, opened: bool):
        """
        Adds a new Recipe to the Database

        Args:
            name (str): [description]recipe name
            spoonacular_id (int): spoonacular identifier (for the API)
            image (str): image for the recipe
            opened (bool): has the user opened this Recipe yet?
        """
        # Open Session
        session = self.Session()        
        # Check if already exist
        to_check = session.query(Recipe).filter_by(spoonacular_id=spoonacular_id).first()
        if to_check is not None:
            Logger.info(f'AddRecipe: Already in DB <{name}>')
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
        
    def add_ingredient(self, show_name: str, spoonacular_name: str, spoonacular_id: int, image: str):
        """
        Adds a new Ingredient to the Database

        Args:
            show_name (str): ingredient name to show (as  user inputs)
            spoonacular_name (str): name given i  the spoonacular API (for searching recipes)
            spoonacular_id (int): Spoonacular Identifier for this ingredient
            image (str): ingredient imgae URL
        """
        # Open Session
        session = self.Session()
        # Add ingredient
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
        """Returns a list of the Ingredients present in the database

        Returns:
            Ingredient: All the ingredients in the DB
        """
        # Open Session
        session = self.Session()
        ingredients = session.query(Ingredient).all()   
        # Close Session
        session.close()
        return ingredients

    def delete_ingredient(self, show_name: str):
        """
        Deletes an ingredient from the DB

        Args:
            show_name (str): name to search in the Database (and the delete it)
        """
        # Open Session
        session = self.Session()
        # Search for the ingredient
        to_delete = session.query(Ingredient).filter_by(show_name=show_name).first() 
        session.delete(to_delete)
        session.commit()
        # Close Session
        session.close()
