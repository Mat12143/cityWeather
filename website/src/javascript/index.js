/// <reference path="jquery.js" />

// Change this path if you are using nginx to ../../website/records.json
$.getJSON("./records.json", function (data) {
  morningTot = 0;
  nrMorning = 0;
  afternoonTot = 0;
  nrAfternoon = 0;
  eveningTot = 0;
  nrEvening = 0;

  minTempMorning = 100;
  maxTempMorning = 0;

  minTempAfternoon = 100;
  maxTempAfternoon = 0;

  minTempEvening = 100;
  maxTempEvening = 0;

  for (key of Object.keys(data)) {
    for (dayMoment of Object.keys(data[key])) {
      if (dayMoment == "Morning") {
        temp = parseInt(data[key][dayMoment]["temperature"]);

        morningTot += temp;
        nrMorning += 1;

        if (temp < minTempMorning) minTempMorning = temp;
        if (temp > maxTempMorning) maxTempMorning = temp;
      }

      if (dayMoment == "Afternoon") {
        temp = parseInt(data[key][dayMoment]["temperature"]);

        afternoonTot += temp;
        nrAfternoon += 1;

        if (temp < minTempAfternoon) minTempAfternoon = temp;
        if (temp > maxTempAfternoon) maxTempAfternoon = temp;
      }

      if (dayMoment == "Evening") {
        temp = parseInt(data[key][dayMoment]["temperature"]);

        eveningTot += temp;
        nrEvening += 1;

        if (temp < minTempEvening) minTempEvening = temp;
        if (temp > maxTempEvening) maxTempEvening = temp;
      }
    }
  }

  $("#morning").html(Math.round(morningTot / nrMorning).toString() + " °C");
  $("#afternoon").html(
    Math.round(afternoonTot / nrAfternoon).toString() + " °C"
  );
  $("#evening").html(Math.round(eveningTot / nrEvening).toString() + " °C");

  $("#morning-maxmin").html(`${minTempMorning} - ${maxTempMorning} °C`);
  $("#afternoon-maxmin").html(`${minTempAfternoon} - ${maxTempAfternoon} °C`);
  $("#evening-maxmin").html(`${minTempEvening} - ${maxTempEvening} °C`);
});

// Change this path if you are using nginx to ../../website/lastRecord.json
$.get("./lastRecord.txt", function (data) {
  console.log(data);
  $("#lastRecord").html(
    `Last record at: ${data == "" ? "No Data Found" : data}`
  );
});
