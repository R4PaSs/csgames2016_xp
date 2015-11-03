$ ->
  init()

init = ->
  bindChallengeModals()
  $.get("/start")
  setInterval(updateChals, 5000)
#  setInterval(updateChals, 2000)
#  setInterval(cycleBackground, 150) # lol

bindChallengeModals = ->
  $(".chal-wrapper").click ->
    chalId = $(this).data "id"
    $.get "/problem/#{chalId}", (data) ->
      $("#chal-problem-wrapper").html data
      $("#submission_form").ajaxForm()

updateChals = ->
  $.get "/update", (data) ->
    window.chals = data
    for chalWrapper in $(".chal-wrapper")
      updateProgress chalWrapper

updateProgress = (chal) ->
  # From static data tags
  chalId = $(chal).data("id")
  chalLength = $(chal).data("length")

  # From dynamic json
  chalEnd = window.chals[chalId]["end"]

  progressBar = $(chal).find(".progress-bar")
  if !chalEnd
    progressBar.css("width", "0%")
    return

  time = new Date().getTime()
  timeLeft = chalEnd - time
  percent = timeLeft / (chalLength * 60 * 1000) * 100

  if percent <= -10
    return
  if percent <= 15
    setState(progressBar, "danger")
  else if percent <= 50
    setState(progressBar, "warning")

  $(chal).find(".progress-bar").css("width", "#{percent}%")

setState = (progressBar, state) ->
  $(progressBar).removeClass("progress-bar-info")
  $(progressBar).removeClass("progress-bar-warning")
  $(progressBar).removeClass("progress-bar-danger")
  $(progressBar).addClass("progress-bar-#{state}")

cycleBackground = ->
  if document.body.style.getPropertyValue("background-color") == "green"
    document.body.style.background = "blue"
  else if document.body.style.getPropertyValue("background-color") == "blue"
    document.body.style.background = "red"
  else if document.body.style.getPropertyValue("background-color") == "red"
    document.body.style.background = "purple"
  else if document.body.style.getPropertyValue("background-color") == "purple"
    document.body.style.background = "yellow"
  else if document.body.style.getPropertyValue("background-color") == "yellow"
    document.body.style.background = "white"
  else if document.body.style.getPropertyValue("background-color") == "white"
    document.body.style.background = "black"
  else
    document.body.style.background = "green"
