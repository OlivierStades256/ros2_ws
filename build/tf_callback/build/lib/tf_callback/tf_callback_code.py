import rclpy
from rclpy.node import Node
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import TransformStamped

class TFProcessor(Node):
    def __init__(self):
        super().__init__('tf_processor')

        self.subscription = self.create_subscription(
            TFMessage,
            '/tf',
            self.tf_callback,
            10
        )
        self.vessels = ["RAS_TN_DB", "RAS_TN_GR", "RAS_TN_OR"]

        # Create publishers (one per vessel) with renamed attribute
        self.pose_publishers = {}
        for vessel in self.vessels:
            topic_name = f"/{vessel}/pose"
            self.pose_publishers[vessel] = self.create_publisher(TransformStamped, topic_name, 10)

    def tf_callback(self, msg):
        for transform in msg.transforms:
            for vessel in self.vessels:
                if vessel in transform.child_frame_id:
                    pose_msg = TransformStamped()
                    pose_msg.header = transform.header
                    pose_msg.child_frame_id = transform.child_frame_id
                    pose_msg.transform = transform.transform

                    # Publish using the renamed attribute
                    self.pose_publishers[vessel].publish(pose_msg)

                    # Optional logging
                    self.get_logger().info(f"Published pose for {vessel} on {pose_msg.header.frame_id}")


def main(args=None):
    rclpy.init(args=args)
    tf_processor = TFProcessor()
    rclpy.spin(tf_processor)
    tf_processor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
