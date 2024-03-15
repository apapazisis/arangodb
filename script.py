# Get the connection from the ArangoDB admin panel

sys_db.delete_graph("school")
graph = sys_db.create_graph("school")

students = graph.create_vertex_collection("students")
lectures = graph.create_vertex_collection("lectures")

edges = graph.create_edge_definition(
    edge_collection="register",
    from_vertex_collections=["students"],
    to_vertex_collections=["lectures"]
)

# Insert vertex documents into "students" (from) vertex collection.
students.delete({"_key": "01"})
students.insert({"_key": "01", "full_name": "Anna Smith"})

students.delete({"_key": "02"})
students.insert({"_key": "02", "full_name": "Jake Clark"})

students.delete({"_key": "03"})
students.insert({"_key": "03", "full_name": "Lisa Jones"})

# Insert vertex documents into "lectures" (to) vertex collection.
lectures.delete({"_key": "MAT101"})
lectures.insert({"_key": "MAT101", "title": "Calculus"})

lectures.delete({"_key": "STA101"})
lectures.insert({"_key": "STA101", "title": "Statistics"})

lectures.delete({"_key": "CSC101"})
lectures.insert({"_key": "CSC101", "title": "Algorithms"})


# Insert edge documents into "register" edge collection.
edges.insert({"_from": "students/01", "_to": "lectures/MAT101"})
edges.insert({"_from": "students/01", "_to": "lectures/STA101"})
edges.insert({"_from": "students/01", "_to": "lectures/CSC101"})
edges.insert({"_from": "students/02", "_to": "lectures/MAT101"})
edges.insert({"_from": "students/02", "_to": "lectures/STA101"})
edges.insert({"_from": "students/03", "_to": "lectures/CSC101"})

edge_definitions = graph.edge_definitions()
vertex_collections = graph.vertex_collections()

print(edge_definitions)
print(vertex_collections)

aql_query = """
    WITH students, lectures
    FOR v, e, p IN 1..1 OUTBOUND @startVertex register
      RETURN p.vertices[1]
"""

result = sys_db.aql.execute(aql_query, bind_vars={"startVertex": "students/01"})

for lecture in result:
    print(lecture)


##########################
print("")
##########################


users = graph.create_vertex_collection("users")

edges = graph.create_edge_definition(
    edge_collection="friendship",
    from_vertex_collections=["users"],
    to_vertex_collections=["users"]
)

users.delete({"_key": "01"})
users.insert({"_key": "01", "full_name": "Michael Schumacher"})

users.delete({"_key": "02"})
users.insert({"_key": "02", "full_name": "Kimi Raikkonen"})

users.delete({"_key": "03"})
users.insert({"_key": "03", "full_name": "Mika Hakkinen"})

users.delete({"_key": "04"})
users.insert({"_key": "04", "full_name": "Rubens Barrichello"})

users.delete({"_key": "05"})
users.insert({"_key": "05", "full_name": "Charls Leclerc"})

users.delete({"_key": "06"})
users.insert({"_key": "06", "full_name": "David Coulthard"})

edges.insert({"_from": "users/01", "_to": "users/02", "status": "1"})
edges.insert({"_from": "users/01", "_to": "users/03", "status": "1"})
edges.insert({"_from": "users/01", "_to": "users/04", "status": "1"})
edges.insert({"_from": "users/02", "_to": "users/05", "status": "1"})
edges.insert({"_from": "users/02", "_to": "users/03", "status": "1"})
edges.insert({"_from": "users/03", "_to": "users/06", "status": "1"})
edges.insert({"_from": "users/06", "_to": "users/01", "status": "0"})

aql_query = """
    WITH users
    FOR v, e, p IN 1..1 INBOUND @inVertex friendship
        FILTER e.status == "0"
        RETURN p.vertices[1]
"""

# it returns all the friend requests I received the above query

friends = sys_db.aql.execute(aql_query, bind_vars={"inVertex": "users/01"})

for friend in friends:
    print(friend)

