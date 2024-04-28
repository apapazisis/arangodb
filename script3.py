
sys_db.delete_graph("graph")
graph = sys_db.create_graph("graph")

sys_db.delete_collection("users")
users = graph.create_vertex_collection("users")

sys_db.delete_collection("collections")
collections = graph.create_vertex_collection("collections")

sys_db.delete_collection("items")
items = graph.create_vertex_collection("items")

sys_db.delete_collection("user_created_collection")
userCollectionEdges = graph.create_edge_definition(
    edge_collection="user_created_collection",
    from_vertex_collections=["users"],
    to_vertex_collections=["collections"]
)

sys_db.delete_collection("collection_has_item")
collectionItemEdges = graph.create_edge_definition(
    edge_collection="collection_has_item",
    from_vertex_collections=["collections"],
    to_vertex_collections=["items"]
)

sys_db.delete_collection("is_friend_with")
friendEdges = graph.create_edge_definition(
    edge_collection="is_friend_with",
    from_vertex_collections=["users"],
    to_vertex_collections=["users"]
)

sys_db.delete_collection("user_has_collection_of_hat")
userCollectionsHats = graph.create_edge_definition(
    edge_collection="user_has_collection_of_hat",
    from_vertex_collections=["users"],
    to_vertex_collections=["items"]
)

docs = []
for i in range(1, 1000001):
    docs.append({"_key": str(i), "full_name": "Anna Smith"})
users.import_bulk(docs)
print("Added users")

docs = []
for i in range(1, 1000001):
    docs.append({"_key": str(i), "title": "Collection_1"})
collections.import_bulk(docs)
print("Added collections")

docs = []
for i in range(1, 11):
    docs.append({"_key": str(i), "title": "Item_" + str(i)})
items.import_bulk(docs)
print("Added items")

edge1 = []
edge2 = []
edge3 = []
for i in range(1, 100000):
    userId = str(randint(1, 1000000))
    collectionId = str(i)
    itemId = str(randint(1, 10))
    edge1.append({"_from": "users/" + userId, "_to": "collections/" + collectionId})
    edge2.append({"_from": "collections/" + collectionId, "_to": "items/" + itemId})
    
    if {"_from": "users/" + userId, "_to": "items/" + itemId} not in edge3:
        edge3.append({"_from": "users/" + userId, "_to": "items/" + itemId})
    print(i)
userCollectionEdges.import_bulk(edge1)
collectionItemEdges.import_bulk(edge2)
userCollectionsHats.import_bulk(edge3)
print("Added collections with users")    

friends = []
for i in range(2, 5000):
    friends.append({"_from": "users/1", "_to": "users/" + str(i)})
friendEdges.import_bulk(friends)
print("Added friends")


aql_query = """
    WITH collections, items, users
    RETURN LENGTH(
    FOR collection, edge, item IN 1..1 INBOUND @startVertex collection_has_item
        FOR user IN 1..1 INBOUND collection user_created_collection
            RETURN DISTINCT user._id
    )
"""
# OR
aql_query = """
    WITH items, users
    RETURN LENGTH(
    FOR user IN 1..1 INBOUND @startVertex user_has_collection_of_hat
        RETURN user._id
    )
"""

result = sys_db.aql.execute(aql_query, bind_vars={"startVertex": "items/1"})

for r in result:
    print(r)

# Θα μπορούσα να φτιάξω μια σύνδεση has_collection_of_hat μεταξύ user και hat 
# και να παίρνω απο εκει το σύνολο απο τα τους φίλους που έχουν για ένα συγκεκριμένο 
# hat, collection

    # WITH collections, items, users
    # FOR friend, edge, me IN 1..1 ANY "users/1" is_friend_with
    #     FOR collection IN 1..1 OUTBOUND friend create_collection
    #         FOR hat IN 1..1 OUTBOUND collection collection_has_item
    #             FILTER hat._id == "items/1"
    #             RETURN distinct { "hatId": hat._id, "userId": friend._id }
    # OR better
    # WITH items, users
    #     RETURN LENGTH( 
    #     FOR friend IN 1..1 ANY "users/1" is_friend_with
    #      FOR hat, edge IN 1..1 OUTBOUND friend user_has_collection_of_hat
    #          FILTER edge._to == "items/1"
    #          RETURN friend._id
    # )
    # OR EVEN BETTER cache the friends of the user in Redis
    # WITH items
    # LET myArray = [
    #   {
    #     "_key": "4905",
    #     "_id": "users/4905",
    #     "_rev": "_hm57ZpW-_q",
    #     "full_name": "Anna Smith"
    #   },
    #   {
    #     "_key": "4807",
    #     "_id": "users/4807",
    #     "_rev": "_hm57ZpW--I",
    #     "full_name": "Anna Smith"
    #   },
    # ]
    # RETURN LENGTH( 
    # FOR friend IN myArray
    #     FOR hat, edge IN 1..1 OUTBOUND friend user_has_collection_of_hat
    #         FILTER edge._to == "items/1"
    #         RETURN friend._id
    # )



# // Prepei na paro tous users pou einai filoi mou 
# // na paro tis collections ton filon mou
# // kai na paro apo ta collections ta hats
# // filtraroume vasi tou hat pou theloume
# // epistrefoume ta monadika apotelesmata giati
# // enas users mporei na exei polles collections gia to idio hat
