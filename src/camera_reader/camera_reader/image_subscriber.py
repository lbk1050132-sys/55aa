import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
# 引入 QoS 必要的庫
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        
        # 設定為 Best Effort (盡力而為)，解決延遲卡頓
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw', # 確認這是你剛才測試有頻率的門牌
            self.listener_callback,
            qos_profile)
            
        self.bridge = CvBridge()
        self.get_logger().info('影像接收節點已啟動 (QoS: Best Effort)')

    def listener_callback(self, data):
        try:
            # 轉換 ROS 影像為 OpenCV 格式
            current_frame = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            # 顯示畫面
            cv2.imshow("Camera View", current_frame)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f'轉換影像時發生錯誤: {e}')

# 💡 這是你剛才消失的啟動開關！
def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    try:
        self_logger = image_subscriber.get_logger()
        self_logger.info('正在接收畫面中，按 Ctrl+C 可停止...')
        rclpy.spin(image_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        # 關閉節點與視窗
        image_subscriber.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()