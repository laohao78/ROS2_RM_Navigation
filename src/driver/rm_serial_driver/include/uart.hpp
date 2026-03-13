#pragma once

#include <iostream>
#include <libserial/SerialPort.h>
#include <string>
#include <vector>
#include <memory>
#include <cstring>
#include <limits>

using namespace LibSerial;

typedef union
{
    uint8_t U8_Buff[4];
    float Float;
} Bint32_Union;

class Driver
{
private:
    std::shared_ptr<SerialPort> _serial_port = nullptr;
    std::string _port_name;
    BaudRate _bps;
    bool isOpen = false;

    // 串口发送单个字节
    int send(unsigned char byte)
    {
        try
        {
            _serial_port->WriteByte(byte);
        }
        catch (const std::runtime_error &)
        {
            std::cerr << "Serial write runtime_error." << std::endl;
            return -2;
        }
        catch (const NotOpen &)
        {
            std::cerr << "Serial port not open." << std::endl;
            return -1;
        }
        return 0;
    }

    // 串口发送字节数组
    int send(const std::vector<unsigned char> &data)
    {
        try
        {
            _serial_port->Write(data);
            std::cout << "[Driver] Sent good " << std::endl;
        }
        catch (const std::runtime_error &)
        {
            std::cerr << "Serial write runtime_error." << std::endl;
            return -2;
        }
        catch (const NotOpen &)
        {
            std::cerr << "Serial port not open." << std::endl;
            return -1;
        }

        _serial_port->DrainWriteBuffer(); // 等待写缓冲区耗尽
        return 0;
    }

public:
    Driver(const std::string &port_name, BaudRate bps)
        : _port_name(port_name), _bps(bps) {

        }
    ~Driver() { close(); }

    // 打开串口
    int open()
    {
        _serial_port = std::make_shared<SerialPort>();
        try
        {
            _serial_port->Open(_port_name);
            _serial_port->SetBaudRate(_bps);
            _serial_port->SetCharacterSize(CharacterSize::CHAR_SIZE_8);
            _serial_port->SetFlowControl(FlowControl::FLOW_CONTROL_NONE);
            _serial_port->SetParity(Parity::PARITY_NONE);
            _serial_port->SetStopBits(StopBits::STOP_BITS_1);
        }
        catch (...)
        {
            std::cerr << "Failed to open serial port: " << _port_name << std::endl;
            isOpen = false;
            return -1;
        }

        _serial_port->FlushIOBuffers();
        isOpen = true;
        return 0;
    }

    // 关闭串口
    void close()
    {
        if (_serial_port != nullptr)
        {
            _serial_port->Close();
            _serial_port = nullptr;
            isOpen = false;
        }
    }

    // 通过串口发送下位机协议数据（vy_set + vx_set + CRC8）
    void nav_data(float vx, float vy, float wz)
    {
        if (!isOpen)
        {
            std::cerr << "Serial port not open!" << std::endl;
            return;
        }

        //下位机死区0.05
        //if(vx>0.15) vx=0.15;
        //else if(vx<-0.15) vx=-0.15;
        //if(vy>0.15) vy=0.15;   
        //else if(vy<-0.15) vy=-0.15;
        //if(wz>0.3) wz=0.3;   
        //else if(wz<-0.3) wz=-0.3;
        //下位机0.0021

        //std::cout << "[Driver] Send cmd_vel_chassis: vx=" << vx << " m/s, vy=" << vy << " m/s, wz=" << wz << " rad/s" << std::endl;

        Bint32_Union vy_union, vx_union, wz_union;
        vy_union.Float = -vy;//thth
        vx_union.Float = vx;
        wz_union.Float = wz;

        std::vector<unsigned char> buf(13);
        buf[0] = vx_union.U8_Buff[0];
        buf[1] = vx_union.U8_Buff[1];
        buf[2] = vx_union.U8_Buff[2];
        buf[3] = vx_union.U8_Buff[3];

        buf[4] = vy_union.U8_Buff[0];
        buf[5] = vy_union.U8_Buff[1];
        buf[6] = vy_union.U8_Buff[2];
        buf[7] = vy_union.U8_Buff[3];

        buf[8] = wz_union.U8_Buff[0];
        buf[9] = wz_union.U8_Buff[1];
        buf[10] = wz_union.U8_Buff[2];
        buf[11] = wz_union.U8_Buff[3];
        // 计算 CRC8 (多项式 0x07)
        uint8_t crc = 0;
        for (int i = 0; i < 12; i++)
        {
            crc ^= buf[i];
            for (int j = 0; j < 8; j++)
            {
                if (crc & 0x80)
                    crc = (crc << 1) ^ 0x07;
                else
                    crc <<= 1;
            }
        }
        buf[12] = crc;

        send(buf);
    }

    // 串口接收单字节（可添加超时）
    int recvdata(unsigned char &byte, size_t msTimeout = 0)
    {
        try
        {
            _serial_port->ReadByte(byte, msTimeout);
        }
        catch (const ReadTimeout &)
        {
            return -2;
        }
        catch (const NotOpen &)
        {
            return -1;
        }
        return 0;
    }


};
