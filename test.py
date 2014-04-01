#!/usr/bin/python
from vboxapi import VirtualBoxManager

manager = VirtualBoxManager()
constants = manager.constants
vbox = manager.vbox
machine = vbox.findMachine('vmfuse-test')
session = manager.getSessionObject(vbox)
machine.launchVMProcess(session, 'gui', None).waitForCompletion(-1)
eventSource = session.console.eventSource
listener = eventSource.createListener()
eventSource.registerListener(listener,
    [constants.VBoxEventType_OnStateChanged], False)

while True:
    event = eventSource.getEvent(listener, 10000)
    if event:
        state_event = manager.queryInterface(event, 'IStateChangedEvent')
        if state_event.state == constants.MachineState_PoweredOff:
            break

print "Done!"
