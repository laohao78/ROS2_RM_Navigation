# 用于测试 RMSerialDriver，只发 vx, vy, wz 到 /cmd_vel
# 可直接运行：python3 test_cmd_vel_pub.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelTestPublisher(Node):
    def __init__(self):
        super().__init__('cmd_vel_test_pub')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel_chassis', 10) #/cmd_vel_chassis
        self.timer = self.create_timer(1.0, self.timer_callback)  # 每秒发布一次

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 0.0   # vx
        msg.linear.y = -0.5   # vy
        msg.angular.z = 0.0  # wz
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: vx={msg.linear.x}, vy={msg.linear.y}, wz={msg.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelTestPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


## 运行
# python3 test_cmd_vel_pub.py