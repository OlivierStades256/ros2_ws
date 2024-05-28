import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class ActuationPrioPublisher(Node):
    def __init__(self):
        super().__init__('actuation_prio_publisher')  

        # Determine the names of the vessels you want to control
        self.vessel_ids = ['RAS_TN_DB', 'RAS_TN_OR', 'RAS_TN_GR']

        # Create a publisher for each vessel, on the priority actuation topic
        self.publishers = {}
        for vessel_id in self.vessel_ids:
            self.publishers[vessel_id] = self.create_publisher(JointState, f'/{vessel_id}/reference/actuation_prio', 10)

        timer_period = 0.5  # Publish command every 0.5 seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        # Create a JointState message for all vessels at once
        joint_state = JointState()
        for vessel_id in self.vessel_ids:

            # For each vessel, define the names of its actuated joints
            joint_state.name = [f'{vessel_id}/SB_aft_thruster_propeller', f'{vessel_id}/PS_aft_thruster_propeller']
            joint_state.position = [0.0, 0.0]  # Angles not used, set to 0
            joint_state.velocity = [1000.0, 1000.0]  # Set both aft thrusters to 1000 RPM
            joint_state.effort = [0.0, 0.0]        # Effort not used, set to 0

            # Publish the message on this vessel's topic
            self.publishers[vessel_id].publish(joint_state)

def main(args=None):
    rclpy.init(args=args)
    actuation_prio_publisher = ActuationPrioPublisher()
    rclpy.spin(actuation_prio_publisher)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

