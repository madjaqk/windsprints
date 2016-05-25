var express = require("express");
var app= express()
var bodyParser = require("body-parser");
var path = require("path");
var mongoose = require("mongoose");

mongoose.connect("mongodb://localhost/quote_dojo")

var QuoteSchema = new mongoose.Schema(
	{
		name: {type: String, required: true},
		quote: {type: String, required: true}
	},
	{timestamps: true}
	)

mongoose.model("Quote", QuoteSchema)
var Quote = mongoose.model("Quote")

app.use(bodyParser.urlencoded());
app.use(express.static(__dirname + "./static"))
app.use(express.static(__dirname + "/node_modules"))

app.set("views", path.join(__dirname, "./views"))
app.set("view engine", "ejs")

app.get("/", function(req, res){
	res.render("welcome")
})

app.get("/quotes", function(req, res){
	Quote.find({}, function(err, quotes){
		if(err){
			console.log("Quote find error", err)
			res.json(err)
		} else {
			quotes.sort(function(a,b){
				return b.updatedAt - a.updatedAt
			})
			res.render("index", {quotes: quotes})
		}
	})
})

app.post("/quotes", function(req, res){
	quote = new Quote(req.body)
	quote.save(function(err){
		if(err){
			console.log("quote save error", err)
			res.json(err)
		} else {
			res.redirect("/quotes")
		}
	})
})

app.post("/update_quote", function(req, res){
	Quote.findOneAndUpdate({_id: req.body.quote_id}, {quote: req.body.quote}, function(err){
		if(err){
			console.log("findOneAndUpdate error", err)
			res.json(err)
		} else {
			res.redirect("/quotes")
		}
	})
})

app.get("/delete/:quote_id", function(req, res){
	Quote.findOneAndRemove({_id: req.params.quote_id}, function(err){
		if(err){
			console.log("quote delete error", err)
		} else {
			res.redirect("/quotes")
		}
	})
})

app.listen(8000, function() {
	console.log("listening on port 8000")
})