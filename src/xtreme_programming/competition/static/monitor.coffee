$ ->
  init()

init = ->
  setInterval(updateAttacks, 1000)

updateAttacks = ->
  $.get "/update_monitor", (data) ->
    $('#attackContainer').empty();
    $.each data.attacks, (idx, att) ->
      addAttack(att)

addAttack = (att) ->

  attWell = $("<div></div>").addClass('well')
  wellData = $("<span></span>")

  attWell.append(wellData)
  $('#attackContainer').prepend(attWell)

  attackerColor = window.teams[att.attacker % window.teams.length].color
  attackerName = $("<span></span>")
    .css("color", attackerColor)
    .css("font-weight", "bold")
    .text(att.attacker_name)
  wellData.append(attackerName)

  if att["distributed"] == true
    attWell.addClass("well-sm")

    attText = " is #{att.name}'ing "
    wellData.append($(document.createTextNode(attText)))

    receiverColor = window.teams[att.receiver % window.teams.length].color
    receiverName = $("<span></span>")
      .css("color", receiverColor)
      .css("font-weight", "bold")
      .text(att.receiver_name)

    wellData.append(receiverName)

  else
    attWell.addClass("well-lg")

    attText = " is #{att.name}'ing "
    wellData.append($(document.createTextNode(attText)))

    receiverColor = window.teams[att.receiver % window.teams.length].color
    receiverName = $("<span></span>")
      .css("color", receiverColor)
      .css("font-weight", "bold")
      .text(att.receiver_name)

    wellData.append(receiverName)


