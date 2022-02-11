"""Map Step Processor"""
from engine.log import log
import engine.map
import engine.geometry as geo
import engine.time as time
import engine.server


class StepMap(engine.map.Map):
    '''Class which implements stepping the game forward in time.

    The StepMap class is responsible for calling the game logic, located 
    in sub-classes, which takes the game forward one step in time. It
    does this by finding methods that match the naming format and then
    calling those methods in a very specific order during each step. 
    Using the various methods name formats, a sub-classes can implement 
    many different game mechanics.

    The method name formats StepMap looks for are as follows. Except 
    for init<MechanicName>() the methods are called in this order
    during each step:

        0) init<MechanicName>(): Called only once when the map is loaded.

        1) stepMapStart<MechanicName>(): Called once at the start of each step.

        2) stepSpriteStart<MechanicName>(sprite): Called for every object
            on the sprite layer.

        3) trigger<MechanicName>(trigger, sprite): Called for every trigger 
            and sprite combination where the sprite anchor point is inside 
            the trigger.

        4) stepMove<MechanicName>(sprite): Called for every object
            on the sprite layer.

        5) stepSpriteEnd<MechanicName>(sprite): Called for every object
            on the sprite layer.

        6) stepMapEnd<MechanicName>(): Called once at the end of each step.

    <MechanicName> is replaced with the name of the game mechanic 
    being implemented.

    Besides implementing the step methods above, a game mechanic
    may need to extend, override, or implement other methods.
    See examples of implementing game mechanics in engine.servermap and 
    the various servermaps of the enginetest and demo games.

    The Server normally only calls the engine.stepmap.StepMap.StepMap()
    method if at least one player is on the map. So game logic stops for
    maps with no players.

    Also, the Server class normally calls stepServerStart() before the
    all the maps process there steps and calls stepServerEnd() after
    all maps have processed their steps. 
    See engine.server.Server.stepServer() for details.
    '''

    def __init__(self, tilesets, mapDir):
        """Extents engine.map.Map.__init__()

        Finds and calls the init<MechanicName>() methods.
        Finds all methods that match each step method type format.
        Sorts all methods by type and priority.
        """

        super().__init__(tilesets, mapDir)

        self['stepMethodTypes'] = (
            "stepMapStart",
            "stepSpriteStart",
            "trigger",
            "stepMove",
            "stepSpriteEnd",
            "stepMapEnd")

        self['stepMethodPriority'] = {}
        for stepMethodType in self['stepMethodTypes']:
            self['stepMethodPriority'][stepMethodType] = {'default': 50}

        self['stepMethods'] = {}

        # Find and call init* methods in this instance (methods could be from this class or a subclass)
        # Note, one important job of init methods is to add to
        # self['stepMethodPriority'] before the step methods are found and sorted
        # below.
        self['initMethods'] = sorted([func for func in dir(self) if callable(getattr(self, func))
                                      and func.startswith("init") and len(func) > len("init")])
        for initMethodName in self['initMethods']:
            initMethod = getattr(self, initMethodName, None)
            initMethod()

        # find step methods in this instance and sort by type and priority
        for stepMethodType in self['stepMethodTypes']:
            self['stepMethods'][stepMethodType] = [func for func in dir(self) if callable(
                getattr(self, func)) and func.startswith(stepMethodType)]
            # if stepMethod is not in priority list then add it with the default priority
            for methodName in self['stepMethods'][stepMethodType]:
                if methodName not in self['stepMethodPriority'][stepMethodType]:
                    self['stepMethodPriority'][stepMethodType][methodName] = self['stepMethodPriority'][stepMethodType]['default']
            self['stepMethods'][stepMethodType].sort(
                key=lambda methodName: self['stepMethodPriority'][stepMethodType][methodName])

        log(f"Map '{self['name']}' Methods:\n{self.getAllMethodsStr()}", "VERBOSE")

    def getAllMethodsStr(self):
        '''Return a multi-line string of all map init*, step*, and trigger* methods.'''

        allMethods = sorted([func for func in dir(self) if callable(getattr(self, func))
                             and not func.startswith("__")])

        stepMethodsStr = ""

        for i in range(len(self['stepMethodTypes'])):
            methodType = f"{self['stepMethodTypes'][i]}*"
            if "Sprite" in self['stepMethodTypes'][i]:
                methodType += "(sprite)"
            elif self['stepMethodTypes'][i].startswith("trigger"):
                methodType += "(trigger, sprite)"
            else:
                methodType += "()"
            stepMethodsStr += f"{methodType:32}"
        stepMethodsStr += "\n"
        for i in range(len(self['stepMethodTypes'])):
            stepMethodsStr += f"{'------------------------':32}"
        stepMethodsStr += "\n"

        j = 0
        keepGoing = True
        while keepGoing:
            keepGoing = False
            for i in range(len(self['stepMethodTypes'])):
                methodName = ""
                if j < len(self['stepMethods'][self['stepMethodTypes'][i]]):
                    methodName = self['stepMethods'][self['stepMethodTypes'][i]][j]
                    allMethods.remove(methodName)
                    methodName += f"/{self['stepMethodPriority'][self['stepMethodTypes'][i]][methodName]}"
                    keepGoing = True
                stepMethodsStr += f"{methodName:32}"
            stepMethodsStr += "\n"
            j += 1

        initMethods = []
        getMethods = []
        setMethods = []
        delMethods = []
        otherMethods = []
        for method in allMethods:
            if method.startswith('init'):
                initMethods.append(method)
            elif method.startswith('get'):
                getMethods.append(method)
            elif method.startswith('set'):
                setMethods.append(method)
            elif method.startswith('del'):
                delMethods.append(method)
            else:
                otherMethods.append(method)

        otherMethodsStr = f"\n{'init*':32}{'get*':32}{'set*':32}{'del*':32}{'other':32}\n"
        otherMethodsStr += f"{'------------------------':32}{'------------------------':32}{'------------------------':32}{'------------------------':32}{'------------------------':32}\n"
        for i in range(max(len(initMethods), len(getMethods), len(setMethods), len(otherMethods))):
            if i < len(initMethods):
                otherMethodsStr += f"{initMethods[i]:32}"
            else:
                otherMethodsStr += f"{'':32}"
            if i < len(getMethods):
                otherMethodsStr += f"{getMethods[i]:32}"
            else:
                otherMethodsStr += f"{'':32}"
            if i < len(setMethods):
                otherMethodsStr += f"{setMethods[i]:32}"
            else:
                otherMethodsStr += f"{'':32}"
            if i < len(delMethods):
                otherMethodsStr += f"{delMethods[i]:32}"
            else:
                otherMethodsStr += f"{'':32}"
            if i < len(otherMethods):
                otherMethodsStr += f"{otherMethods[i]:32}"
            else:
                otherMethodsStr += f"{'':32}"
            otherMethodsStr += '\n'

        return otherMethodsStr + "\n" + stepMethodsStr

    def addStepMethodPriority(self, stepMethodType, stepMethodName, priority):
        """Set the prioriy of a step method. 

        This is normally used by subclass init* methods to prioritize step 
        methods before finding and sorting them.

        Args:
            stepMethodType (str): One of self['stepMethodPriority']
            stepMethodName (str): A method name that starts with stepMethodType
            priority (int): The priority of stepMethodName.Lower number is 
                higher priority.
        """
        if stepMethodType not in self['stepMethodPriority']:
            log(f"{stepMethodType} is not a valid stepMethodType.", "WARNING")
            return
        self['stepMethodPriority'][stepMethodType][stepMethodName] = priority

    ########################################################
    # STEP DISPATCHER (Order of steps matters!)
    ########################################################

    def stepMap(self):
        """Move the map forward one step in time"""

        # call all self.stepMapStart*() methods
        for methodName in self['stepMethods']['stepMapStart']:
            method = getattr(self, methodName, None)
            method()

        # call all self['step']SpriteStart*(sprite) methods for each sprite
        for methodName in self['stepMethods']['stepSpriteStart']:
            method = getattr(self, methodName, None)
            for sprite in self['sprites']:
                method(sprite)

        # for each sprite find all triggers sprite is inside and call
        # corresponding trigger* method.
        for sprite in self['sprites']:
            self.stepTriggers(sprite)

        # call all self['step']Move*(sprite) methods for each sprite
        for methodName in self['stepMethods']['stepMove']:
            method = getattr(self, methodName, None)
            for sprite in self['sprites']:
                method(sprite)

        # call all self['step']SpriteEnd*(sprite) methods  for each sprite
        for methodName in self['stepMethods']['stepSpriteEnd']:
            method = getattr(self, methodName, None)
            for sprite in self['sprites']:
                method(sprite)

        # call all self.stepMapEnd*() methods
        for methodName in self['stepMethods']['stepMapEnd']:
            method = getattr(self, methodName, None)
            method()

    def stepTriggers(self, sprite):
        """Process all triggers for a sprite.

        Find all triggers (objects on the trigger layer) that contain this 
        sprite's anchor and call the corresponding trigger* method.
        
        The search excludes the sprite itself from the search 
        since objects may be on the sprite and trigger layer at the
        same time.

        Args:
            sprite (dict): Tiled object from the sprite layer.
        """

        # get a list of all triggers that the sprite's anchor is inside of.
        triggers = self.findObject(
            x=sprite['anchorX'],
            y=sprite['anchorY'],
            objectList=self['triggers'],
            returnAll=True,
            exclude=sprite)

        # remove any triggers that do not have trigger* methods to call.
        # log warning since this should not happen.
        for trigger in triggers:
            triggerMehodName = self.getTriggerMethodName(trigger)
            # if trigger is not in priority list then log error and remove it
            if triggerMehodName not in self['stepMethodPriority']['trigger']:
                log(
                    f"ServerMap does not have method named {triggerMehodName} for trigger type {trigger['type']}.",
                    "ERROR")
                triggers.remove(trigger)

        # sort trigger method names by priority (lower first)
        triggers.sort(key=lambda trigger: self['stepMethodPriority']['trigger'][self.getTriggerMethodName(trigger)])

        # call each triggers method. e.g. trigger['type'] == 'mapDoor' will call triggerMapDoor(trigger, sprite)
        for trigger in triggers:
            triggerMethod = getattr(self, self.getTriggerMethodName(trigger), None)
            stopOtherTriggers = triggerMethod(trigger, sprite)
            if stopOtherTriggers:
                break  # do not process any more triggers for this sprite on this step.

    def getTriggerMethodName(self, trigger):
        """Given a trigger name, return the name of a trigger's method.

        Convert a trigger type (eg. trigger['type'] == "mapDoor") to method 
        name (eg. "triggerMapDoor")

        Args:
            trigger (dict): Tiled object that is on this maps trigger layer.

        Returns:
            str: The name of the method used to process the trigger.
        """
        return "trigger" + trigger['type'][:1].capitalize() + trigger['type'][1:]
