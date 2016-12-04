from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views import View
import json
import pdb
from models import Widget, GridLayout, Control, Input

# import RPi.GPIO as GPIO
# import time

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(18, GPIO.OUT)

def isMobile(request):
    userAgent = request.META.get("HTTP_USER_AGENT")
    if "mobile" in userAgent.lower():
        return True
    return False

def objAndJson(obj, name):
    double = dict()
    double[name] = obj
    double[name + "JSON"] = json.dumps(obj)
    return double

"""
Controls: BOTH JavaScript and Load
Layout: BOTH JavaScript and Load
Templates: JUST JavaScript
Widgets: JUST JavaScript
"""
class IndexView(View):
    def get(self, request):
        mobile = isMobile(request)

        controls = [control.flatten() for control in Control.objects.all()]

        templates = [render_to_string("partials/widget.html", dict(control=control, mobile=mobile)) for control in controls]
        controlPanels = [render_to_string("partials/controlpanel.html", dict(control=control, mobile=mobile)) for control in controls]

        layout = LayoutView.getFirstLayout()

        context = dict(title="HomeControl", mobile=isMobile(request), templatesJSON=json.dumps(templates), controlPanels="\n".join(controlPanels))
        context.update(**objAndJson(controls, "controls"))
        context.update(**objAndJson(layout, "layout"))

        return render(request, "index.html", context)

class ControlView(View):
    def post(self, request):
        try:
            controlDict = json.loads(request.body)
            print "=== Control ID: ", controlDict["control_id"], " requested state: ", controlDict["state"]
            control = Control.objects.filter(id=controlDict["control_id"]).first()
            if control is not None:
                control.state = controlDict["state"]
                control.save()
                return HttpResponse(json.dumps(dict(status="success", payload=control.flatten())))
            else:
                return HttpResponse(json.dumps(dict(status="failure", message="Failed to load control with control_id: '" + controlDict["control_id"] + "'")))
        except:
            return HttpResponse(json.dumps(dict(status="failure", message="Failed to load JSON: '" + request.body + "'")))


class LayoutView(View):
    @staticmethod
    def getFirstLayout():
        layout = GridLayout.objects.order_by('pk', 'name').first()
        if layout is not None:
            return layout.flatten()
        else:
            return None

    def get(self, request):
        return HttpResponse(self.getFirstLayout())

    def post(self, request):
        try:
            return HttpResponse(json.dumps(dict(status="success", payload=dict(message="Saved layout as ID: 0"))))
            layoutDict = json.loads(request.body)
            """
            layoutModel = GridLayout(user=layout["user"], name=layout["name"])
            layoutModel.save()
            for widget in layout["widgets"]:
                existingWidget = Widget.objects.get(pk=widget["pk"])
                if existingWidget is not None:
                    existingWidget.update(**widget)
                else:
                    widgetModel = Widget.objects.Create(**widget)
                    
                Widget.createFromDict(widget, layoutModel.pk)
            print "Successfully created new layout with PK: ", layoutModel.pk
            """
            existingLayout = GridLayout.objects.filter(pk=layoutDict["id"]).first()
            if existingLayout is not None:
                existingLayout.delete()

            layout = GridLayout.objects.create(user=layoutDict["user"], name=layoutDict["name"])
            for widget in layoutDict["widgets"]:
                widgetDict = dict(widget)
                widgetDict["layout"] = layout
                widgetDict["state"] = json.dumps(widgetDict["state"])
                print widgetDict
                Widget.objects.create(**widgetDict)
            return HttpResponse(json.dumps(dict(status="success", payload=dict(message="Saved layout as ID: " + str(layout.pk)))))
        except Exception as e:
            print "Exception: ", e
            return HttpResponse(json.dumps(dict(status="error", message="Failed to parse JSON of layout")))
        



class LightView(View):
    def get(self, request):
        pdb.set_trace()
        print request.body
        state = json.loads(request.body)
        print state
        # print "LED on"
        # GPIO.output(18, GPIO.HIGH)
        # time.sleep(1)
        # print "LED off"
        # GPIO.output(18, GPIO.LOW)

        return HttpResponse('{"result": "success", "message": "Started the servo via GET"}')

    def post(self, request):
        print request.method
        print request.body
        return HttpResponse('{"result": "success", "message": "Started the servo via POST"}')  