#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
arm = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
left_wheel = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_wheel = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)
claw = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

driveTimer = None

def init():
    arm.spin(REVERSE, -40, RPM)
    claw.spin(REVERSE, 80, RPM)
    wait(1.5, SECONDS)
    claw.stop()
    arm.stop()

    arm.set_position(0, DEGREES)
    claw.set_position(0, DEGREES)


MAX_ANGLE_PERCENT = 1.8
DRIVE_MULT = .0575
ARM_SLOW_HEIGHT = -500
ARM_UP_SPEED_MULT = .6
CLAW_OPEN_ANGLE = 130

active = True
kill = False


def open_claw():
    if not active: return
    claw.spin(FORWARD, 5, VOLT)
    while (controller_1.buttonL1.pressing() or controller_1.buttonL2.pressing()) and claw.position(DEGREES) < CLAW_OPEN_ANGLE:
        pass
    claw.stop()

def close_claw():
    if not active: return
    claw.spin(REVERSE, 5, VOLT)
    while controller_1.buttonR1.pressing() or controller_1.buttonR2.pressing():
        pass
    claw.spin(REVERSE, .75, VOLT)

def stun():
    active = False
    wait(2, SECONDS)
    active = True

def _kill():
    print("robot terminated")
    global kill
    kill = True


controller_1.buttonL1.pressed(open_claw)
controller_1.buttonL2.pressed(open_claw)
controller_1.buttonR1.pressed(close_claw)
controller_1.buttonR2.pressed(close_claw)
controller_1.buttonUp.pressed(_kill)
controller_1.buttonDown.pressed(stun)


def driver_control():
    init()
    global kill
    global active
    while not kill:
        if not active: continue
        arm.spin(FORWARD, -controller_1.axis2.position() / (20 if arm.position(DEGREES) < ARM_SLOW_HEIGHT else 15), VOLT)
        left_wheel.spin(FORWARD, (controller_1.axis3.position() - controller_1.axis4.position()) * DRIVE_MULT * (ARM_UP_SPEED_MULT if arm.position(DEGREES) < ARM_SLOW_HEIGHT else 1), VOLT)
        right_wheel.spin(FORWARD, (controller_1.axis3.position() + controller_1.axis4.position()) * DRIVE_MULT * (ARM_UP_SPEED_MULT if arm.position(DEGREES) < ARM_SLOW_HEIGHT else 1), VOLT)
    for motor in [right_wheel, left_wheel, arm, claw]:
        motor.stop()

def autonomous():
    pass

competition = Competition(driver_control, autonomous)
