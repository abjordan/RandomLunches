#!/usr/bin/env python

from peewee import *
import argparse

db = SqliteDatabase('randomLunch.db')

class BaseModel(Model):
    class Meta:
        database = db

class Person(BaseModel):
    name = CharField(unique=True)
    email = CharField(unique=True)
    department = CharField()

class Lunch(BaseModel):
    personOne = ForeignKeyField(Person, related_name="p1_lunches")
    personTwo = ForeignKeyField(Person, related_name="p2_lunches")
    dateHeld = DateField(null=True)

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Lunch Tool")
    parser.add_argument("command", metavar="CMD", type=str,
                        help="Command to run [help for list]")
    parser.add_argument("cmd_opts", metavar="CMDOPTS", type=str, nargs="*",
                        default=None,
                        help="Command arguments")

    args = parser.parse_args()

    if args.command == "help":
        print "Commands:"
        print "   help                       Print this list"
        print "   init                       Set up the database"
        print "   add <name> <email>         Add a user"
        print "   testdata                   Create some test data"
        print "   lunchlist                  Export a lunch list"
        print "   lunched <name1> <name2>    Report a lunch success"

    elif args.command == "init":
        
        db.connect()
        db.create_tables([Person, Lunch])

    elif args.command == "testdata":
    
        alex = Person.create(name="Alex Jordan", 
                             email="ajordan@bbn.com", 
                             department="D").save()
        jack = Person.create(name="Jack Dietz", 
                             email="jdietz@bbn.com", 
                             department="D").save()
        lunch = Lunch.create(personOne=alex,
                             personTwo=jack,
                             dateHeld=None).save()

    elif args.command == "add":
        
        n = args.cmd_opts[0]
        e = args.cmd_opts[1]
    
        try:
            p = Person.create(name=n, email=e, department="?").save()
            print "Added user", n, "/", e
        except IntegrityError:
            print "ERROR: User", n, "already exists"

    elif args.command == "lunchlist":

        # Find pairs of people who haven't had lunch yet (and aren't
        #   currently scheduled for a lunch)
        # Add the pair to the lunch table
        # Produce the list of outstanding lunches
