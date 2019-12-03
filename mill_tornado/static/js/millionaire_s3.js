/**
* Edits the number prototype to allow money formatting
*
* @param fixed the number to fix the decimal at. Default 2.
* @param decimalDelim the string to deliminate the non-decimal
*        parts of the number and the decimal parts with. Default "."
* @param breakdDelim the string to deliminate the non-decimal
*        parts of the number with. Default ","
* @return returns this number as a USD-money-formatted String
*         like this: x,xxx.xx
*/
Number.prototype.money = function(fixed, decimalDelim, breakDelim){
    var n = this, 
    fixed = isNaN(fixed = Math.abs(fixed)) ? 2 : fixed, 
    decimalDelim = decimalDelim == undefined ? "." : decimalDelim, 
    breakDelim = breakDelim == undefined ? "," : breakDelim, 
    negative = n < 0 ? "-" : "", 
    i = parseInt(n = Math.abs(+n || 0).toFixed(fixed)) + "", 
    j = (j = i.length) > 3 ? j % 3 : 0;
    return negative + (j ? i.substr(0, j) +
         breakDelim : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "1" + breakDelim) +
          (fixed ? decimalDelim + Math.abs(n - i).toFixed(fixed).slice(2) : "");
}

var question_sec = 15;
var stage = 1;

/**
* Plays a sound via HTML5 through Audio tags on the page
*
* @require the id must be the id of an <audio> tag.
* @param id the id of the element to play
* @param loop the boolean flag to loop or not loop this sound
*/
startSound = function(id, loop) {
    soundHandle = document.getElementById(id);
    if(loop)
        soundHandle.setAttribute('loop', loop);
//  soundHandle.play();
}

/**
* The View Model that represents one game of
* Who Wants to Be a Millionaire.
* 
* @param data the question bank to use
*/
var n_questions = 3;

var MillionaireModel = function(data) {
    
    var self = this;

    var topics = Object.keys(data)

    // Questions
    this.questions = [];
        
    for(var i = 1; i <= n_questions; i++) {
        var topic = topics[Math.floor(Math.random() * topics.length)];
        var types = Object.keys(data[topic]);
        var type = types[Math.floor(Math.random() * types.length)];
        var current_question = data[topic][type][Math.floor(Math.random() * data[topic][type].length)]
        this.questions.push(current_question);
    }

    // A flag to keep multiple selections
    // out while transitioning levels
    this.transitioning = false;

    // The current money obtained
    this.money = new ko.observable(0);

    // The current level(starting at 1) 
    this.level = new ko.observable(1);

    // Grabs the question text of the current question
    self.getQuestionText = function() {
        ws.send(self.questions[self.level() - 1].question);
        //self.questionID = Math.floor(Math.random() *)
        // params = { op: "hola" };
        // $.getJSON('http://198.18.0.2:8888/com', params);
        return self.questions[self.level() - 1].question;
    }

    // Gets the answer text of a specified question index (0-3)
    // from the current question
    self.getAnswerText = function(index) {
        return self.questions[self.level() - 1].content[index];
    }


    // Fades out an option used if possible
    self.fadeOutOption = function(item, event) {
        if(self.transitioning)
            return;
        $(event.target).fadeOut('slow');
    }

    // Attempts to answer the question with the specified
    // answer index (0-3) from a click event of elm
    self.answerQuestion = function(index, elm) {
        if(self.transitioning)
            return;
        self.transitioning = true;

        $("#game").fadeOut('slow', function() {
            $("#score").html('Puntos: '+ self.money());
            $("#score").fadeIn('slow');
            $("#hint").html('Hola');
            $("#hint").fadeIn('slow');
            $("#key").html(' ');
        })      

        if(index === 0){
            self.money(self.money() + 100);
			ws.send("Yes");
        }
		if(index === 1){
			ws.send("No");				
		}
		if(index === 2){
			ws.send("Later");
		}
    }
    
    // Gets the money formatted string of the current won amount of money.
    self.formatMoney = function() {
        return self.money().money(0, '', ',');
    }
};


var myModel;
var keys = [];
var hints = [];
var ws;

// Executes on page load, bootstrapping
// the start game functionality to trigger a game model
// being created
$(document).ready(function() {
    console.log("On Ready");
    $.getJSON("static/questions_test_s3.json", function(data) {
        $("#pre-start").show();
        $("#start").click(function() {

            // var host = "198.18.0.1";
            var host = "localhost"; // For PC
            var port = "8888";
            var uri = "/ws";

            ws = new WebSocket("ws://"+host+":"+port+uri)
            ws.onmessage = function(evt) {
                console.log("Message Received: " + evt.data);
                alert("message received: " + evt.data);
                };
                 
            // Close Websocket callback
            ws.onclose = function(evt) {
                console.log("***Connection Closed***");
                $("div#message_details").empty();

                };

            // Open Websocket callback
            ws.onopen = function(evt) { 
                console.log("***Connection Opened***");
                };

            $("#pre-start").fadeOut('slow', function() {
            startSound('background', true);
            $("#game").fadeIn('slow');
            for(var i = 1; i <= data.sist_oseo.length; i++) {
                $("#problem-set").append('<option value="' + i + '">' + i + '</option>');
            }
            var index = 0;
            myModel = new MillionaireModel(data);
            ko.applyBindings(myModel);
            startSound('background', true);
            $("#game").fadeIn('slow');
            //interval = window.setInterval(stopWatch, 1000);
            });
            
    $.getJSON("static/keys_hints.json", function(keys_hints) {
        keys = keys_hints.keys; 
        hints = keys_hints.hints; 
    });
            
            });
        });
});

