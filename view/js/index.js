var graphic;

graphic = new Object;

var data = [["Beastie Boys", 13], ["The Magnetic Fields", 12], ["Beck", 11], ["Devo", 9], ["David Bowie", 8], ["Django Django", 8], ["Tom Waits", 8], ["Metronomy", 7], ["Sweet Lights", 7], ["The Mountain Goats", 7], ["Battles", 7], ["Pink Floyd", 6], ["Leonard Cohen", 6], ["Drop Down Smiling", 6], ["Death Grips", 6], ["Burial", 6], ["New Order", 6], ["Talking Heads", 6], ["Fleetwood Mac", 6], ["Siriusmo", 6]];


graphic.create = function() {
  var g, height, i, size, width, _i, _len, _ref, _results;
  width = $(document).width() / 2;
  height = $(document).height() * .85;
  size = d3.min([width, height]);
  graphic.svg = d3.select("#graphic").append("svg").attr("width", size).attr("height", size);
  g = graphic.svg.append("g");
  _ref = _.range(size / 10);
  _results = [];
  for (_i = 0, _len = data.length; _i < _len; _i++) {
    i = data[_i][0];
    j = data[_i][1];
    _results.push(graphic.svg.append("rect").attr("width", j * 30).attr("height", 20).attr("fill", "tan").attr('y', _i * 22));
    _results.push(graphic.svg.append("text").text(i).attr('y', 15 + _i * 22));
  }
  return _results;
};

graphic.update = function() {};

graphic.destroy = function() {
  graphic.svg.remove();
  return delete graphic.svg;
};

$(document).ready(function() {
  graphic.create();
  return $(window).resize(function() {
    graphic.destroy();
    return graphic.create();
  });
});
