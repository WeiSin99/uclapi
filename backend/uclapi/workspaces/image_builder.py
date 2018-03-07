import redis

from lxml import etree
from django.conf import settings

from .occupeye import OccupEyeApi, BadOccupEyeRequest

class ImageBuilder():
    """
    Builds an SVG image with live sensor statuses/
    """
    def __init__(self, survey_id, map_id):
        # Confirm integers
        if not survey_id.isdigit():
            raise BadOccupEyeRequest
        if not map_id.isdigit():
            raise BadOccupEyeRequest

        self._api = OccupEyeApi()
        self._redis = redis.StrictRedis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        self._sensors = self._api.get_survey_sensors(
            survey_id,
            return_states=True
        )
        self._survey_id = survey_id
        self._map_id = map_id
        self._absent_colour = "#ABE00C"
        self._occupied_colour = "#FFC90E"


    def set_colours(self, absent="#ABE00C", occupied="#FFC90E"):
        self._absent_colour = absent
        self._occupied_colour = occupied


    def get_live_map(self):
        map_data = self._api.get_survey_image_map_data(
            self._survey_id,
            self._map_id
        )
        nsmap = {
            None: "http://www.w3.org/2000/svg",
            "xlink": "http://www.w3.org/1999/xlink",
            "ev": "http://www.w3.org/2001/xml-events"
        }
        svg = etree.Element(
            "svg",
            nsmap=nsmap
        )
        viewport = etree.SubElement(svg, "g")
        viewport.attrib["transform"] = "scale(0.02, 0.02)"
        base_map = etree.SubElement(viewport, "image")
        base_map.attrib["width"] = map_data["VMaxX"]
        base_map.attrib["height"] = map_data["VMaxY"]
        map_data = self._redis.hgetall(
            "occupeye:surveys:{}:maps:{}".format(
                self._survey_id,
                self._map_id
            )
        )
        (b64_data, content_type) = self._api.get_image(
            map_data["image_id"]
        )
        base_map.attrib["{http://www.w3.org/1999/xlink}href"] = "data:{};base64,{}".format(
            content_type,
            b64_data
        )
        bubble_overlay = etree.SubElement(viewport, "g")

        # Get the sensors for that map
        the_map = {}
        for map_obj in self._sensors["maps"]:
            if map_obj["id"] == self._map_id:
                the_map = map_obj
                break

        for sensor_id, sensor_data in the_map["sensors"].items():
            node = etree.SubElement(viewport, "g")
            node.attrib["transform"] = "translate({},{})".format(
                sensor_data["x_pos"],
                sensor_data["y_pos"]
            )
            circle = etree.SubElement(node, "circle")
            circle.attrib["r"] = "128"
            if sensor_data["last_trigger_type"] == "Absent":
                circle.attrib["fill"] = self._absent_colour
            else:
                circle.attrib["fill"] = self._occupied_colour

        return etree.tostring(svg, pretty_print=True)
