$ ->
  init()

init = ->
  bindChallengeModals()
  $.get("/start")
  setInterval(updateChals, 1000)

bindChallengeModals = ->
  $(".chal-wrapper").click ->
    chalId = $(this).data "id"
    $.get "/problem/#{chalId}", (data) ->
      $("#chal-problem-wrapper").html data
      $("#submission_form").ajaxForm( ->
        $('#chalModal').modal('toggle')
        setSolved(chalId)
      )

updateChals = ->
  $.get "/update", (data) ->
    window.chals = data.chals
    if data['yolo_avail']
      yoloBtn = $("#yoloButton")
      yoloBtn.click ->
        $("#yoloContainer").hide()
        $.get "/attack"
      $("#yoloContainer").show()
    else
      $("#yoloContainer").hide()

    if !!data["yolo"]
      eval data['yolo']

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

  $(chal).find(".progress-bar").css("width", "#{percent}%")

  if progressBar.hasClass('progress-bar-success')
    return
  if percent <= -10
    return
  if percent <= 15
    setState(progressBar, "danger")
  else if percent <= 50
    setState(progressBar, "warning")

setState = (progressBar, state) ->
  $(progressBar).removeClass("progress-bar-info")
  $(progressBar).removeClass("progress-bar-warning")
  $(progressBar).removeClass("progress-bar-danger")
  $(progressBar).addClass("progress-bar-#{state}")

setSolved = (chalId) ->
  chal = $("#chal-wrapper-#{chalId}")
  progressBar = $(chal).find(".progress-bar")
  setState(progressBar, "success")

lol = () ->
  undefined
