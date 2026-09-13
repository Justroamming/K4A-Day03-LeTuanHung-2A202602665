"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ và thông tin học vụ của sinh viên VinUni bằng mã sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
                }
            },
            "required": ["student_id"]
        }
    },
    
    {
        "name": "iot_sensor_query",
        "description": "Tra cứu dữ liệu cảm biến từ thiết bị IoT (ví dụ: DHT22, độ ẩm đất) theo mã thiết bị.",
        "parameters": {
            "type": "object",
            "properties": {
                "device_id": {
                    "type": "string",
                    "description": "Mã thiết bị IoT cần tra cứu (ví dụ: 'DEV0000001')"
                },
                "sensor_type": {
                    "type": "string",
                    "description": "Loại cảm biến cần đọc (ví dụ: 'DHT22', 'soil_moisture', 'all')"
                }
            },
            "required": ["device_id"]
        }
    },
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn về hệ thống IoT/Hệ thống tưới tự động với chuyên gia.",
        "parameters": {
            "type": "object",
            "properties": {
                "device_id": {
                    "type": "string",
                    "description": "Mã thiết bị IoT liên quan (ví dụ: 'DEV0000001')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn (ví dụ: '14:00 15/09/2026')"
                },
                "expert_name": {
                    "type": "string",
                    "description": "Tên chuyên gia tư vấn"
                }
            },
            "required": ["device_id"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    },
    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.60,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
    }
}

IoT_DEVICES = {
    "DEV0000001": {
        "device_id": "DEV0000001",
        "device_name": "ESP32-WROOM-NodeA",
        "location": "Khu vực vườn A",
        "sensors": {
            "DHT22": {"temperature": 28.5, "humidity": 65},
            "soil_moisture": 25
        },
        "status": "online"
    },
    "DEV0000002": {
        "device_id": "DEV0000002",
        "device_name": "ESP32-WROOM-NodeB",
        "location": "Khu vực vườn B",
        "sensors": {
            "DHT22": {"temperature": 31.2, "humidity": 52},
            "soil_moisture": 25
        },
        "status": "online"
    },
    "DEV0000003": {
        "device_id": "DEV0000003",
        "device_name": "RaspberryPi-Gateway",
        "location": "Phòng điều khiển",
        "sensors": {
            "DHT22": {"temperature": 26.0, "humidity": 70},
            "soil_moisture": 55
        },
        "status": "online"
    }
}


def execute_academic_query(student_id: str) -> str:
    """Thực thi tra cứu học vụ theo mã sinh viên"""
    student = MOCK_DATABASE.get(student_id.strip().upper())
    if student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": student_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_iot_sensor_query(device_id: str, sensor_type: str = "all") -> str:
    """Thực thi tra cứu dữ liệu cảm biến IoT theo mã thiết bị"""
    device = IoT_DEVICES.get(device_id.strip().upper())
    if device:
        if sensor_type.lower() == "all" or sensor_type == "":
            sensor_data = device["sensors"]
        else:
            sensor_data = {sensor_type: device["sensors"].get(sensor_type, f"Cảm biến '{sensor_type}' không có trên thiết bị này")}
        return json.dumps({
            "status": "SUCCESS",
            "device_id": device_id,
            "device_name": device["device_name"],
            "location": device["location"],
            "sensor_data": sensor_data,
            "device_status": device["status"]
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy thiết bị IoT có mã '{device_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(device_id: str, datetime_str: str, expert_name: str = "PGS.TS Nguyễn Văn A") -> str:
    """Thực thi đặt lịch hẹn tư vấn hệ thống IoT"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{device_id}-99",
        "device_id": device_id,
        "datetime": datetime_str,
        "expert": expert_name,
        "message": f"Đặt lịch tư vấn thành công cho thiết bị {device_id} với {expert_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "academic_query": execute_academic_query,
    "iot_sensor_query": execute_iot_sensor_query,
    "schedule_appointment": execute_schedule_appointment
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
