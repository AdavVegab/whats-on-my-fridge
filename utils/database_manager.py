"""
Database Module

This module contains all the code to manage the Database

The database is a SQL Database using SQLAlchemy as a  bject Relational Mapper
https://docs.sqlalchemy.org/

"""

from logging import StringTemplateStyle
import re
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
    show_name = Column(String)
    spoonacular_name = Column(String)
    spoonacular_id = Column(Integer, unique=True)
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
    favorite = Column(Boolean)
        
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
    
    def add_recipe(self, name:str, spoonacular_id: int, image: str):
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
        recipe.favorite = False
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
            List: All the ingredients in the DB
        """
        # Open Session
        session = self.Session()
        ingredients = session.query(Ingredient).all()   
        # Close Session
        session.close()
        return ingredients
    
    def get_all_recipes(self):
        """Returns a list of the Recipes present in the database

        Returns:
            List: All the recipes in the DB
        """
        # Open Session
        session = self.Session()
        recipes = session.query(Recipe).all()   
        # Close Session
        session.close()
        return recipes
        

    def delete_ingredient(self, spoonacular_id: int):
        """
        Deletes an ingredient from the DB

        Args:
            spoonacular_id (int): id to search in the Database (and the delete it)
        """
        # Open Session
        print(spoonacular_id)
        session = self.Session()
        # Search for the ingredient
        to_delete = session.query(Ingredient).filter_by(spoonacular_id=spoonacular_id).first() 
        print(to_delete.spoonacular_id)
        session.delete(to_delete)
        session.commit()
        # Close Session
        session.close()
        
    def check_for_favorite(self, spoonacular_id):
        # Open Session
        session = self.Session()
        to_check = to_toggle = session.query(Recipe).filter_by(spoonacular_id=spoonacular_id).first()
        # Close Session
        session.close()
        if to_check.favorite:
            return True
        else:
            return False

    def toggle_favorite_recipe(self, spoonacular_id):
        new_value = False
        # Open Session
        session = self.Session()
        # Search for the Recipe
        to_toggle = session.query(Recipe).filter_by(spoonacular_id=spoonacular_id).first()
        if to_toggle.favorite:
            to_toggle.favorite = False
            new_value = False
        else:
            to_toggle.favorite = True
            new_value = True
        session.commit()
        # Close Session
        session.close()
        return new_value