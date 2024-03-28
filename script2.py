sys_db.delete_graph("graph")
graph = sys_db.create_graph("graph")

sys_db.delete_collection("users")
users = graph.create_vertex_collection("users")

sys_db.delete_collection("collections")
collections = graph.create_vertex_collection("collections")

sys_db.delete_collection("items")
items = graph.create_vertex_collection("items")

userCollectionEdges = graph.create_edge_definition(
    edge_collection="create_collection",
    from_vertex_collections=["users"],
    to_vertex_collections=["collections"]
)

collectionItemEdges = graph.create_edge_definition(
    edge_collection="collection_has_item",
    from_vertex_collections=["collections"],
    to_vertex_collections=["items"]
)

friendEdges = graph.create_edge_definition(
    edge_collection="is_friend_with",
    from_vertex_collections=["users"],
    to_vertex_collections=["users"]
)

docs = []
for i in range(1, 100001):
    docs.append({"_key": str(i), "full_name": "Anna Smith"})
    print(i)
users.import_bulk(docs)

docs = []
for i in range(1, 10001):
    docs.append({"_key": str(i), "title": "Collection_1"})
    print(i)
collections.import_bulk(docs)

docs = []
for i in range(1, 11):
    docs.append({"_key": str(i), "title": "Item_" + str(i)})
    print(i)
items.import_bulk(docs)

for i in range(1, 10000):
    userId = str(randint(1, 100000))
    collectionId = str(i)
    itemId = str(randint(1, 10))
    userCollectionEdges.insert({"_from": "users/" + userId, "_to": "collections/" + collectionId})
    collectionItemEdges.insert({"_from": "collections/" + collectionId, "_to": "items/" + itemId})
    print(i)

friendEdges.insert({"_from": "users/1", "_to": "users/2"})

aql_query = """
    WITH collections, items, users
    FOR collection, edge, item IN 1..1 INBOUND @startVertex collection_has_item
        FOR user IN 1..1 INBOUND collection create_collection
            RETURN DISTINCT user._id
"""

result = sys_db.aql.execute(aql_query, bind_vars={"startVertex": "items/1"})

for r in result:
    print(r)
