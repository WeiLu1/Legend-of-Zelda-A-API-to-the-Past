import os
import pandas as pd
from . import db, project_path
from flask_restful import abort


class BossesModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    effective_weapons = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(40), nullable=False)
    rewards = db.Column(db.String(50), nullable=True)
    # dungeons = db.relationship('Dungeons', lazy=True)

    @staticmethod
    def get_all_bosses():
        return BossesModel.query.all()

    @staticmethod
    def get_boss_by_id(boss_id):
        if boss_id.isdigit():
            boss = BossesModel.query.filter_by(id=boss_id).first()
        else:
            boss = BossesModel.query.filter_by(name=boss_id).first()

        if not boss:
            abort(404, message='boss not found')

        return boss

    # @classmethod
    # def get_boss_by_id(cls, boss_id):
    #     if boss_id:
    #         boss = cls.query.filter_by(id=boss_id).first()
    #         return boss

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, effective weapons: {self.effective_weapons}, location: {self.location}, rewards: {self.rewards}\n"


class CharactersModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    race = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    location = db.Column(db.String(100))

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, race: {self.race}, gender: {self.gender}, location: {self.location}\n"

    @staticmethod
    def get_all_characters():
        return CharactersModel.query.all()

    @staticmethod
    def get_character_by_id(character_id):
        if character_id.isdigit():
            character = CharactersModel.query.filter_by(id=character_id).first()
        else:
            character = CharactersModel.query.filter_by(name=character_id).first()

        if not character:
            abort(404, message='character not found')

        return character


class DungeonsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    boss = db.Column(db.String(20))
    enemies = db.Column(db.String(500))
    items = db.Column(db.String(60))
    rewards = db.Column(db.String(50))
    boss_id = db.Column(db.Integer, nullable=True)
    # boss_id = db.Column(db.Integer, db.ForeignKey('bosses.id'), nullable=True)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, boss: {self.boss}, enemies: {self.enemies}, items: {self.items}, rewards: {self.rewards}, boss id: {self.boss_id}\n"

    @staticmethod
    def get_all_dungeons():
        return DungeonsModel.query.all()

    @staticmethod
    def get_dungeon_by_id(dungeon_id):
        if dungeon_id.isdigit():
            dungeon = DungeonsModel.query.filter_by(id=dungeon_id).first()
        else:
            dungeon = DungeonsModel.query.filter_by(name=dungeon_id).first()

        if not dungeon:
            abort(404, message='dungeon not found')

        return dungeon


class EnemiesModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, location: {self.location}\n"

    @staticmethod
    def get_all_enemies():
        return EnemiesModel.query.all()

    @staticmethod
    def get_enemy_by_id(enemy_id):
        if enemy_id.isdigit():
            enemy = EnemiesModel.query.filter_by(id=enemy_id).first()
        else:
            enemy = EnemiesModel.query.filter_by(name=enemy_id).first()

        if not enemy:
            abort(404, message='enemy not found')

        return enemy


class ItemsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    uses = db.Column(db.String(100))

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, location: {self.location}, uses: {self.uses}\n"

    @staticmethod
    def get_all_items():
        return ItemsModel.query.all()

    @staticmethod
    def get_item_by_id(item_id):
        if item_id.isdigit():
            item = ItemsModel.query.filter_by(id=item_id).first()
        else:
            item = ItemsModel.query.filter_by(name=item_id).first()

        if not item:
            abort(404, message='item not found')

        return item


def populate_everything():
    db.create_all()
    data_path = os.path.join(project_path, 'data')
    files = os.listdir(os.path.join(project_path, 'data'))
    for file in files:
        full_file_path = data_path + '/' + file
        model = file.split('.')[0]
        data = pd.read_csv(full_file_path).values.tolist()
        if model == 'bosses':
            for row in data:
                boss = BossesModel(name=row[0], effective_weapons=row[1], location=row[2], rewards=row[3])
                db.session.add(boss)
        elif model == 'characters':
            for row in data:
                character = CharactersModel(name=row[0], race=row[1], gender=row[2], location=row[3])
                db.session.add(character)
        elif model == 'dungeons':
            for row in data:
                dungeon = DungeonsModel(name=row[0], boss=row[1], enemies=row[2], items=row[3], rewards=row[4], boss_id=row[5])
                db.session.add(dungeon)
        elif model == 'enemies':
            for row in data:
                enemy = EnemiesModel(name=row[0], location=row[1])
                db.session.add(enemy)
        elif model == 'items':
            for row in data:
                item = ItemsModel(name=row[0], location=row[1], uses=row[2])
                db.session.add(item)
        db.session.commit()
    db.session.close()
