#!/usr/bin/env python                                                                               
from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)

db = client.test

# Number of

#mongodb_project = db.final_project.find_one()

# Number of documents

#mongodb_project = db.final_project.find().count()

# Number of nodes

#mongodb_project = db.final_project.find({"type" : "node"}).count()

# Number of ways

#mongodb_project = db.final_project.find({"type" : "way"}).count()


# Number of disticnt users

'''
mongodb_project = db.final_project.distinct("created.user")



count = 0
for m in mongodb_project:
    count += 1

print count
'''


# Top 5 contributing users
'''
mongodb_project = db.final_project.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
                                        {"$sort":{"count":-1}}, {"$limit":5}])

'''
# Number of users appearing only once (having 1 post)
'''
mongodb_project = db.final_project.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
                                        {"$group":{"_id":"$count", "num_users":{"$sum":1}}},
                                        {"$sort":{"_id":1}}, {"$limit":1}])
'''


# Top 10 appearing amenities
'''
mongodb_project = db.final_project.aggregate([{"$match":{"amenity":{"$exists":1}}},
                                              {"$group":{"_id":"$amenity", "count":{"$sum":1}}},
                                              {"$sort":{"count":-1}}, {"$limit":10}])

'''
# Top 5 places of worship
'''
mongodb_project = db.final_project.aggregate([{"$match":{"amenity":{"$exists":1},"religion":{"$exists":1},"amenity":"place_of_worship"}},
                                              {"$group":{"_id":"$religion", "count":{"$sum":1}}},
                                              {"$sort":{"count":-1}}, {"$limit":5}])

'''
# Top 10 popular cuisines
'''
mongodb_project = db.final_project.aggregate([{"$match":{"amenity":{"$exists":1},"cuisine":{"$exists":1},"amenity":"restaurant"}},
                                              {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
                                              {"$sort":{"count":-1}}, {"$limit":10}])

'''

# Bank with most branches
'''
mongodb_project = db.final_project.aggregate([{"$match":{"amenity":{"$exists":1},"operator":{"$exists":1}, "amenity":"bank"}},
                                              {"$group":{"_id":"$operator", "count":{"$sum":1}}},
                                              {"$sort":{"count":-1}}, {"$limit":1}])

'''

# Top 3 Tree Types
'''
mongodb_project = db.final_project.aggregate([{"$match":{"natural":{"$exists":1},"tree_type":{"$exists":1},"natural":"tree"}},
                                              {"$group":{"_id":"$tree_type", "count":{"$sum":1}}},
                                              {"$sort":{"count":-1}}, {"$limit":3}])

'''

# Top 3 Gas Stations
'''
mongodb_project = db.final_project.aggregate([{"$match":{"amenity":{"$exists":1},"name":{"$exists":1},"amenity":"fuel"}},
                                              {"$group":{"_id":"$name", "count":{"$sum":1}}},
                                              {"$sort":{"count":-1}},{"$limit":3}])

'''

# Top 5 Bike rentals with most capacity
'''
mongodb_project = db.final_project.aggregate([{"$match":{"amenity":{"$exists":1},"capacity":{"$exists":1},"amenity":"bicycle_rental"}},
                                              {"$project":{"_id":"$name", "capacity":"$capacity"}},
                                              {"$sort":{"capacity":-1}},{"$limit":5}])

'''

# Cafes
'''
mongodb_project_cafe = db.final_project.aggregate([{"$match":{"amenity":{"$exists":1},"cuisine":{"$exists":1},"amenity":"cafe"}},
                                                      {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
                                                      {"$sort":{"count":-1}},{"$limit":10}])

# Fast Food

mongodb_project_fast = db.final_project.aggregate([{"$match":{"amenity":{"$exists":1},"cuisine":{"$exists":1},"amenity":"fast_food"}},
                                              {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
                                              {"$sort":{"count":-1}},{"$limit":10}])


# Restaurants

mongodb_project_restaurant = db.final_project.aggregate([{"$match":{"amenity":{"$exists":1},"cuisine":{"$exists":1},"amenity":"restaurant"}},
                                              {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
                                              {"$sort":{"count":-1}},{"$limit":10}])


pprint.pprint(mongodb_project_cafe)
pprint.pprint(mongodb_project_fast)
pprint.pprint(mongodb_project_restaurant)

'''
pprint.pprint(mongodb_project)