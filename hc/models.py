from __future__ import unicode_literals
from django.db import models

import pdb
import json

class Control(models.Model):
    """
    Describes the control and required inputs

    """
    name = models.CharField(max_length=50)
    mobilename = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    color = models.CharField(max_length=50)
    state = models.CharField(max_length=200)

    def flatten(self):
        mobilename = self.mobilename
        if len(mobilename) == 0:
            mobilename = None
        controlDict = dict(id=self.pk, description=self.description, color=self.color, name=self.name, state=self.state, mobilename=mobilename)
        controlDict["inputs"] = [inputModel.flatten() for inputModel in self.input_set.all()]
        return controlDict


class Input(models.Model):
    """
    An input for a homecontrol

    """
    name = models.CharField(max_length=50)
    input_type = models.CharField(max_length=50)
    properties = models.CharField(max_length=200)
    control = models.ForeignKey(Control, on_delete=models.CASCADE)

    def flatten(self):
        inputDict = dict(id=self.pk, input_type=self.input_type, name=self.name, control_id=self.control.pk)
        inputDict.update(json.loads(self.properties))
        return inputDict


class GridLayout(models.Model):
    """
    grid layout object to store preferences of user's grid
    """
    user = models.IntegerField()
    name = models.CharField(max_length=50)

    def flatten(self):
        layoutDict = dict(id=self.pk, user=self.user, name=self.name)
        layoutDict["widgets"] = [widgetModel.flatten() for widgetModel in self.widget_set.all()]
        return layoutDict


class Widget(models.Model):
    """
    A widget describes the position and size of a grid component

    """
    col = models.IntegerField()
    row = models.IntegerField()
    size_x = models.IntegerField()
    size_y = models.IntegerField()
    state = models.CharField(max_length=200)
    control_id = models.IntegerField()
    layout = models.ForeignKey(GridLayout, on_delete=models.CASCADE)

    def flatten(self):
        stateDict = dict()
        try:
            stateDict = json.loads(self.state)
        except:
            pass

        return dict(id=self.pk, col=self.col, row=self.row, size_x=self.size_x, size_y=self.size_y, control_id=self.control_id, state=stateDict)
