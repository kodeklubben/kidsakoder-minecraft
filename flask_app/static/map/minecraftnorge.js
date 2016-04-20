function drawPolygon() {
    drawReset(), polygonLayer = new OpenLayers.Layer.Vector("Polygon Layer"), mouseControl = new OpenLayers.Control.MousePosition, map.addLayer(polygonLayer), drawControl = new OpenLayers.Control.DrawFeature(polygonLayer, OpenLayers.Handler.RegularPolygon, {
        handlerOptions: {
            sides: 4,
            irregular: !0
        }
    }), map.addControl(drawControl), drawControl.activate(), drawControl.events.register("featureadded", this, function () {
        if (validSize()) {
            var a = (new OpenLayers.Format.WKT).write(polygonLayer.features[polygonLayer.features.length - 1]);
            $("#geom").val(a), drawControl.deactivate()
            $("#submit").removeClass("alert alert-success alert-danger fade in").addClass("alert alert-success fade in");
        } else {
            $("#geom").val("toolarge"), drawControl.deactivate();
            $("#submit").removeClass("alert alert-success alert-danger fade in").addClass("alert alert-danger fade in");
            $("#results").html("<p>Området du har tegnet er for stort</p>")
            $("#resultpanel").css("visibility", "visible");
            $("#resultpanel").css("height", "auto");
            $("#resultpanel").css("width", "auto");
        }
    })
}

function drawReset() {
    $("#results").html(""), $("#resultpanel").css("visibility", "hidden"), $("#resultpanel").css("height", "0px"), $("#resultpanel").css("width", "0px"), $("#geom").val("empty"), drawControl && (map.removeLayer(polygonLayer), polygonLayer = null, mouseControl.deactivate(), mouseControl = null, drawControl.deactivate(), drawControl = null, clippingGeometry = []);
    $("#submit").removeClass("alert alert-success alert-danger fade in");
}

function validSize() {
    var a = getArea(polygonLayer.features[polygonLayer.features.length - 1].geometry);
    return console.log("Area: " + a + "km2"), 64 > a
}

function getArea(a) {
    proj4.defs("EPSG:32633", "+proj=utm +zone=33 +ellps=WGS84 +datum=WGS84 +units=m +no_defs");
    for (var b = a.components[0].components, c = [], d = 0; d < b.length; d++) {
        var e = b[d].x, f = b[d].y, g = proj4(proj4("EPSG:900913"), proj4("EPSG:32633"), [e, f]);
        c.push(new OpenLayers.Geometry.Point(g[0], g[1]))
    }
    var h = new OpenLayers.Geometry.LinearRing(c), i = Math.abs(h.getArea());
    return Math.round(i / 1e6)
}

$(document).ready(function () {
    dataDist.init({
        host: "https://mc-sweco.fmecloud.com",
        token: "175db7e3e55c52182b834f10cc5e9986d9154963",
        detail: "low&token=8fce04aca10b65ffe1b53cd73c1fc90679ede88b"
    })
});

var dataDist = function () {
    function a(a) {
        $("#spindiv").css("visibility", "hidden");
        var b = a.serviceResponse.statusInfo.status,
            c = "",
            d = $("<div />");

        if (b == "success") {
            var c = a.serviceResponse.url;
            d.append($("<p>Vellykket! <br> Overfører verden </p>"));
            d.append(new Spinner().spin().el)
            $.post('/mc_world_url', {
                url : c,
                description : $("#description").val()

                }, function (data, status) {
                    var json_data = $.parseJSON(data);
                    $("#results").html(json_data.message);
                    $("#world_id").val(json_data.world_id);

                    $("#submit").removeClass("alert alert-success alert-danger fade in");
                    $("#continue").css("display", "block");
                    $("#continue").addClass("alert alert-success fade in");
                })
            //d.append($('<a href="' + c + '">Last ned! </a>')));
        } else {
            d.append($("<p>Mislykket. Prøv igjen!</p>"))
        }

        $("#results").html(d);
        $("#resultpanel").css("visibility", "visible");
        $("#resultpanel").css("height", "auto");
        $("#resultpanel").css("width", "auto");
    }

    var b, c, d = "publicweb", e = "generateworld.fmw";
    return {
        init: function (a) {
            b = a.host, c = a.token, hostVisible = a.hostVisible, FMEServer.init({
                server: b,
                token: c,
                detail: "high&token=8fce04aca10b65ffe1b53cd73c1fc90679ede88b"
            })
        }, orderData: function () {
            if ("empty" == $("#geom").val())return $("#results").html("Tegn område!"), $("#resultpanel").css("visibility", "visible"), $("#resultpanel").css("height", "auto"), $("#resultpanel").css("width", "auto"), !1;
            if (validSize() || "toolarge" != $("#geom").val()) {
                var b = e;
                $('input[name="texted_world"]').prop("checked") && (b = "generateworld_text.fmw");
                var c = $("#world_name").val().trim();
                /^[^\\/?%*:|"<>\.]+$/.test(c) || (c = "new_world");
                var f = "";
                return f += "ROI_WKT=" + $("#geom").val(), f += "&ROI_COORDSYS=EPSG:900913&WORLD_NAME=" + c, $("#spindiv").css("visibility", "visible"), FMEServer.runDataDownload(d, b, f, a), !1
            }
            var g = getArea(polygonLayer.features[polygonLayer.features.length - 1].geometry);
            return $("#results").html(" Området du har tegnet er " + g + " km2. Det må være mindre enn 64 km2."), $("#resultpanel").css("visibility", "visible"), $("#resultpanel").css("height", "auto"), $("#resultpanel").css("width", "auto"), !1
        }
    }
}();

$("#draw").attr("onclick", "drawPolygon();"), $("#reset").attr("onclick", "drawReset();");
var drawControl, mouseControl, polygonLayer, map, fromProjection, toProjection, clippingGeometry = [];
$("#helpmodal").modal("hide");

$.fn.bootstrapSwitch.defaults.onColor = "default";
$.fn.bootstrapSwitch.defaults.onText = "På";
$.fn.bootstrapSwitch.defaults.offText = "Av";
//$.fn.bootstrapSwitch.defaults.labelWidth = "55px";
$.fn.bootstrapSwitch.defaults.labelWidth = "79px";
$.fn.bootstrapSwitch.defaults.handleWidth = "41px";
$("[name='texted_world']").bootstrapSwitch();
$(".bootstrap-switch-label").css({
    "font-size": "10px",
    "line-height": "10px",
    "height": "32px",
    "margin-top": "-3px",
    "margin-bottom": "-1px",
    "padding-top": "5px",
    "padding-bottom": "0px",
    "vertical-align": "middle"
    });
//$(".bootstrap-switch-container").css({width: "174px"});
$(".bootstrap-switch-wrapper").css({width: "100%"});

$("#submit").attr("disabled", !0);
$("#world_name").on("keyup", function () {
    $("#world_name").val().trim().length > 3 ? $("#submit").removeAttr("disabled") : $("#submit").attr("disabled", !0)
});
$("#world_name").keyup();

$("#continue").click(function () {
    $("#continue_form").submit();
});

var map = new OpenLayers.Map({
    div: "map",
    projection: new OpenLayers.Projection("EPSG:900913"),
    center: [1973496, 9164033],
    zoom: 5,
    layers: [new OpenLayers.Layer.WMS("TopoGrayWMS", "http://opencache.statkart.no/gatekeeper/gk/gk.open?SERVICE=WMS&", {
        layers: "topo2graatone",
        srs: "EPSG:900913"
    })]
}), opts = {
    lines: 13,
    length: 28,
    width: 14,
    radius: 42,
    scale: 1,
    corners: 1,
    color: "#000",
    opacity: .25,
    rotate: 0,
    direction: 1,
    speed: 1,
    trail: 60,
    fps: 20,
    zIndex: 2e9,
    className: "spinner",
    top: "50%",
    left: "50%",
    shadow: !1,
    hwaccel: !1,
    position: "absolute"
}, target = document.getElementById("spindiv"), spinner = new Spinner(opts).spin(target);

$("#helpbtn").click(function () {
    $("#helpmodal").modal("show")
});
