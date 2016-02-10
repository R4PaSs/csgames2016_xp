setInterval(->
  $.get("/ready/", (data) ->
    if data["status"] == "ongoing"
      document.location = "/play"
  )
, 2000)
