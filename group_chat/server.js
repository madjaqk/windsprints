var express = require("express");

var app = express();
var bodyParser = require("body-parser");

app.use(express.static(__dirname + "/static"))
app.use(express.static(__dirname + "/node_modules"))
app.use(bodyParser.urlencoded());

app.set("views", __dirname + "/views")
app.set("view engine", "ejs");

app.get("/", function(req, res){
	res.render("index")
})

var server = app.listen(8000, function() {
	console.log(__dirname+"/static")
})

var chat_history = []

function update_history(){
	io.emit("update_history", {history: chat_history})
}

var io = require("socket.io").listen(server)

io.sockets.on("connection", function(socket){
	console.log("socket", socket.id)
	update_history() // This will broadcast the history to everyone every time someone joins, which may not be desirable in a high-traffic app
	
	socket.on("post", function(data){
		console.log("post data", data)
		chat_history.push(data)
		update_history()
	})
})