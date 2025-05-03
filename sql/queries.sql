db.hotels.aggregate([
  { $unwind: "$rooms" },
  { $match: { "rooms.available": true } },
  { 
    $group: {
      _id: "$name",
      location: { $first: "$location" },
      rooms: { $push: "$rooms" }
    }
  },
  { 
    $project: {
      "Hotel": "$_id",
      "Location": "$location",
      "Rooms": {
        $map: {
          input: "$rooms",
          as: "room",
          in: {
            "Number": "$$room.number",
            "Type": "$$room.type",
            "Price": "$$room.price"
          }
        }
      }
    }
  }
]);

db.hotels.aggregate([
  { $unwind: "$rooms" },
  { 
    $group: {
      _id: "$name",
      average_price: { $avg: "$rooms.price" }
    }
  },
  { $sort: { _id: 1 } }
]);

db.reservations.find(
  { "guest_email": "anna.nowak@example.com" },
  { 
    "_id": 0,
    "hotel_name": 1,
    "room_number": 1,
    "check_in": 1,
    "check_out": 1,
    "status": 1
  }
).sort({ "check_in": 1 });

db.reservations.aggregate([
  { 
    $group: {
      _id: "$status",
      count: { $sum: 1 }
    }
  },
  { $sort: { _id: 1 } }
]);

