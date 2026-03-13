#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "uart.hpp" // 包含您提供的 Driver 类
#include <memory>
#include <limits>

class RMSerialDriver : public rclcpp::Node
{
public:
    RMSerialDriver()
        : Node("rm_serial_driver")
    {
        
        // ...existing code...
        vx_limit_ = this->declare_parameter("vx_limit", 1.0);
        vy_limit_ = this->declare_parameter("vy_limit", 1.0);
        wz_limit_ = this->declare_parameter("wz_limit", 1.0);
        // ...existing code...
        
        // 初始化串口驱动，例如设备为 /dev/ttyACM0，波特率 115200
        driver_ = std::make_shared<Driver>("/dev/ttyACM0", BaudRate::BAUD_115200);

        int ret = driver_->open();
        if (ret != 0)
        {
            RCLCPP_ERROR(this->get_logger(), "Failed to open serial port!");
        }
        else
        {
            RCLCPP_INFO(this->get_logger(), "Serial port opened successfully.");
        }

        // 订阅 /cmd_vel_chassis 主题，用于接收底盘控制指令
        cmd_vel_sub_ = this->create_subscription<geometry_msgs::msg::Twist>(
            "/cmd_vel", 10,
            std::bind(&RMSerialDriver::cmdVelCallback, this, std::placeholders::_1));

        // 创建一个定时器定期从串口接收数据并打印
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),                       // 每 100 毫秒定时器触发一次
            std::bind(&RMSerialDriver::receiveSerialData, this)); // 调用接收串口数据的回调函数
    }

    ~RMSerialDriver()
    {
        if (driver_)
        {
            driver_->close();            
        }
    }

    // ...existing code...
    float vx_limit_;
    float vy_limit_;
    float wz_limit_;
    // ...existing code...

private:
    // 处理 /cmd_vel 消息的回调
    void cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg)
    {
        float vx = std::clamp(static_cast<float>(msg->linear.x), -vx_limit_, vx_limit_);
        float vy = std::clamp(static_cast<float>(msg->linear.y), -vy_limit_, vy_limit_);
        float wz = std::clamp(static_cast<float>(msg->angular.z), -wz_limit_, wz_limit_);

        RCLCPP_INFO(this->get_logger(), "限幅后: vx=%.2f, vy=%.2f, wz=%.2f", vx, vy, wz);

        if (driver_)
        {
            driver_->nav_data(vx, vy, wz); // 使用限幅后的值
        }
        else
        {
            RCLCPP_ERROR(this->get_logger(), "Driver is not initialized!");
        }
    }

    // 定时从串口接收数据并打印
    void receiveSerialData()
    {
        if (!driver_)
        {
            RCLCPP_ERROR(this->get_logger(), "Driver is not initialized!");
            return;
        }

        unsigned char byte;
        int ret = driver_->recvdata(byte, 100); // 设置 100ms 的超时
        if (ret == 0)
        {
            // 如果成功接收到数据，打印接收到的字节
            RCLCPP_INFO(this->get_logger(), "Received byte from serial: 0x%02X", byte);
        }
        else if (ret == -2)
        {
            // 超时
            // RCLCPP_WARN(this->get_logger(), "No data received (timeout).");
        }
        else
        {
            // 串口未打开或其他错误
            RCLCPP_ERROR(this->get_logger(), "Error reading data from serial port.");
        }
    }

private:
    std::shared_ptr<Driver> driver_;                                         // 串口驱动对象
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_sub_; // 订阅者
    rclcpp::TimerBase::SharedPtr timer_;                                     // 定时器，用于定期接收串口数据
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<RMSerialDriver>());
    rclcpp::shutdown();
    return 0;
}

