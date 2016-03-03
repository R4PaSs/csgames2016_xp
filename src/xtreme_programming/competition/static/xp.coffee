$ ->
  init()

init = ->
  bindChallengeModals()
  updateChals()
  setInterval(updateChals, 5000)
  window.currentZoom = 1.0;

validateSubmission = (formData, jqForm, options) ->
  for formField in formData
    if !formField.value
      if formField.name == "comment"
        alert("You must fill the readme field before submitting.")
      else if formField.name == "file"
        alert("You must select a zip file before submitting.")
      return false
  return true

bindChallengeModals = ->
  $(".chal-wrapper").click ->
    chalId = $(this).data "id"
    $.get "/problem/#{chalId}", (data) ->
      $("#chal-problem-wrapper").html data
      $("#submission_form").ajaxForm(
        {
          beforeSubmit: validateSubmission,
          success: ->
            $('#chalModal').modal('toggle')
            setSolved(chalId)
            document.location.reload()
        }
      )

updateChals = ->
  $.get "/update/", (data) ->
    if data['global_status'] == "finished"
      document.location = "/done"
    window.chals = data.chals
    if data['yolo_avail']
      yoloBtn = $("#yoloButton")
      yoloBtn.click ->
        $("#yoloContainer").hide()
        $.get "/attack/"
        document.location.reload()
      $("#yoloContainer").show()
    else
      $("#yoloContainer").hide()

    if !!data["yolo"]
      eval data['yolo']

    window.serverTime = data["server_time"]
    for chalWrapper in $(".chal-wrapper")
      updateProgress chalWrapper

updateProgress = (chal) ->
  # From static data tags
  chalId = $(chal).data("id")
  chalLength = $(chal).data("length")

  # From dynamic json
  chalEnd = window.chals[chalId]["end"]
  chalSubmitted = window.chals[chalId]["submitted"]
  serverTime = window.serverTime

  progressBar = $(chal).find(".progress-bar")
  if !chalEnd
    progressBar.css("width", "0%")
    return

  if chalSubmitted == true
    setState(progressBar, "success")

  timeLeft = chalEnd - serverTime
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
