###################################
    # DEPENDENCIES AND SETUP
###################################
import os
import pandas as pd
import numpy as np

# sqlalchemy is the Python SQL toolkit and Object Relational Mapper 
# The simplest usage of automap is to reflect an existing database into a new model.
# We create a new AutomapBase class in a similar manner as to how we create a declarative base class, using automap_base().
# We then call AutomapBase.prepare() on the resulting base class, asking it to reflect the schema and produce mappings:
from sqlalchemy.ext.automap import automap_base
# object-relational mapper (ORM), an optional component that provides the data mapper pattern
# where classes can be mapped to the database in open ended
from sqlalchemy.orm import Session
#session (link) from Python to the DB
from sqlalchemy import create_engine


# Flask is a web framework.
# This means flask provides you with tools, libraries and technologies that allow you to build a web application.
# Flask is a Python web framework.Flask can be used for building complex , database-driven websites,starting with mostly static pages.
# "falsk" is the framework while "Flask" is the python class data type
# Used Flask jsonify to convert your API data into a valid JSON response object

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

#########################
    # FLASK SETUP
#########################
#Flask constructor takes the name of current module (__name__) as argument.
# The route() function of the Flask class is a decorator, which tells the application which URL should call the associated function.
# create an instance of the Flask class for our web app.
# Flask will call functions
# Flask is a popular Python web framework, meaning it is a third-party Python library used for developing web applications.
app = Flask(__name__)

#########################
    # DATABASE SETUP
#########################
# sqlite is a software library that provides a relational database management system.
# The lite in sqlite means light weight in terms of setup, database administration, and required resource.
# sqlite has the following noticeable features: self-contained, serverless, zero-configuration, transactional.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
db = SQLAlchemy(app)

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
# mapped classes are now created with names by default
# matching that of the table name.
Samples_Metadata = Base.classes.sample_metadata
Samples = Base.classes.samples

#######################################################################################################################
                                        # FLASK ROUTES
#######################################################################################################################



####################################################################
# DISPLAY THE STATIC ROUTE
# The route home display the index.html the web page


@app.route("/")
def index():
    
    """Return the homepage."""
    return render_template("index.html")

####################################################################
# DISPLAY THE STATIC ROUTE
# The route "/names" display the array of samples



@app.route("/names")
def names():

    """Return a list of sample names."""

    # Use Pandas to Perform SQL query
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of column names (sample names)

    return jsonify(list(df.columns)[2:])


#######################################################################
# DISPLAY METADATA OF SAMPLE AS DICTIONARY
# Dictionary provides details of ethinicity,gender,age,location,bbtype,wfreq,sample
# Specify the dynamic route "/metadata/<enter sample>" to see the sample details.


@app.route("/metadata/<sample>")
def sample_metadata(sample):

    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.sample,
        Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary Entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    print(sample_metadata)
    # jsonifying the sample_metadata
    return jsonify(sample_metadata)


#########################################################################
# DISPLAY A DICTIONARY WITH KEYS("otu_ids","otu_labels","sample_values") AND VALUES(AS LIST)
# Specify the dynamic route "/samples/<enter sample >" to see the result


@app.route("/samples/<sample>")
def samples(sample):

    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # Only Keep Rows with Values above 1
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
    
    # Sort by sample
    sample_data.sort_values(by=sample, ascending=False, inplace=True)
    
    # Format Data to Send as JSON
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    # jsonifying the data
    return jsonify(data)


###############################################################################
# Python assigns the name "__main__" to the script when the script is executed.
#   "__name__" is a variable automatically set in an executing python program
# If you import your module from another program, __name__ will be set to the name of the module
# Here program run directly    
# If you run your program directly, __name__ will be set to __main__


if __name__ == "__main__":
    #print ("I am being run directly")
    app.run()
#else:
    #print ("I am being imported")