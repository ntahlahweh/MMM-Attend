/// node_helper.js
const spawn = require("child_process").spawn
var NodeHelper = require("node_helper")
var process = spawn("python", ["/home/pi/MagicMirror/modules/MMM-Attend/attendance.py"])
var interval = 1000
module.exports = NodeHelper.create({
  
  socketNotificationReceived: function(notification, payload) {
    switch(notification) {
      case "GIVE_ME_DATA":
        this.job()
        break
    }
  },
  job: function() {
    process.stdout.on("data", (data)=>{
      //var timer = setInterval(() =>{
	    console.log ("node_helper", data)
        //}, 1000) 
      var result = String.fromCharCode.apply(null, new Uint16Array((data)))
      this.sendSocketNotification("HERE_IS_DATA", result)
    })    

  }
})

