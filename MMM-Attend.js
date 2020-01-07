Module.register("MMM-Attend",{
	// Default module config.
	defaults: {
		updateInterval: 30000,
		fadespeed: 4000 
		
		},
		

 getDom: function() {
    var e = document.createElement("div")
    e.id = "DISPLAY"
    //console.log (test)
    return e
  },
  
 start: function() {
    Log.info('Starting module: ' + this.name);
  },
 
  notificationReceived: function(notification, payload, sender) {
    switch(notification) {
      case "DOM_OBJECTS_CREATED":
        var timer = setInterval(()=>{
          this.sendSocketNotification("GIVE_ME_DATA")
          //var test = "kel"
        }, 1000)
        break
    }
  },
  socketNotificationReceived: function(notification, payload) {
    switch(notification) {
      case "HERE_IS_DATA":
        var e = document.getElementById("DISPLAY")
        e.innerHTML = payload // display nama
	var timer = setInterval(() =>{
	    console.log ("e", e.innerHTML)
        }, 1000) 
    }
  },
  getStyles: function() {
      return ['MMM-Attend.css']
  },
  
})
