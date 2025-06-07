from flask import Flask, render_template

app = Flask(__name__)

rooms = [
    {"id": 1, "name": "Deluxe Room", "price": 120, "image": "https://source.unsplash.com/400x300/?hotel-room"},
    {"id": 2, "name": "Suite", "price": 200, "image": "https://source.unsplash.com/400x300/?luxury-suite"},
    {"id": 3, "name": "Standard Room", "price": 80, "image": "https://source.unsplash.com/400x300/?room"}
]

@app.route('/')
def index():
    return render_template("index.html", rooms=rooms)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/room/<int:id>')
def room_detail(id):
    room = next((r for r in rooms if r["id"] == id), None)
    return render_template("room.html", room=room)

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=9111)
