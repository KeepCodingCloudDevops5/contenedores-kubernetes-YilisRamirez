db = db.getSiblingDB("student_db");
db.student_tb.drop();

db.student_tb.insertMany([
    {
        "DNI": 4387679M,
        "name": "Cristina",
        "course": "primary"
     },
     {
         "DNI": 5463890T,
         "name": "Mauricio",
         "course": "secondary"
     },
     {
          "DNI": 6543678Y,
          "name": "Laura",
          "course": "prymary"
     },
]);
