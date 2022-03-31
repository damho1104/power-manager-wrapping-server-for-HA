# Power Manager Wrapping Server for HA
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fdamho1104%2Fpower-manager-wrapping-server-for-HA&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Github&edge_flat=false)](https://hits.seeyoufarm.com)
![Python](https://img.shields.io/badge/Python-3776AB.svg?&style=flat&logo=Python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)  
css5831 께서 구축해주신 서버를 기반으로 한 Home Assistant 연동가능 API 서버 입니다.  
Home Assistant 서버는 같은 내부망에 존재한다고 가정합니다.  
[PowerManager 로컬 서버 by css5831](https://github.com/SeongSikChae/PowerManagerServer/releases)  

## Release
### v1.0.2
- 다원 기기 서버 연결 상태 출력 버그 수정 
### v1.0.1
- python 코드 공개
### v1.0.0
- HA 와 연동가능한 API 서버 릴리즈

## 1. config.json 생성
- 서버를 실행시킬 host ip 와 port 정보를 입력합니다.
- server 항목에 실행 중인 PowerManager 로컬 서버의 정보를 입력합니다.
- PowerManager 로컬 서버가 여러 대인 경우에도 연동 가능합니다.  
  - PowerManager 로컬 서버가 1 대인 경우 device 항목 생략 가능  
  - PowerManager 로컬 서버가 2 대 이상인 경우 default 서버에 붙은 device 정보는 입력하지 않으셔도 됩니다.  
  - PowerManager 로컬 서버가 2 대 이상인 경우 인증서는 같다는 가정하에 동작합니다.
```text
{
  "ip": "[HOST_IP]",
  "port": "[HOST_PORT]",
  "server": {
    "[SERVER_NAME]": {
      "default": true,
      "use_cert": true,
      "power_manager_server_ip": "[POWER_MANAGER_SERVER_IP]",
      "power_manager_server_port": "[POWER_MANAGER_SERVER_PORT]"
    },
    "[OTHER_SERVER_NAME]": {
      "use_cert": true,
      "power_manager_server_ip": "[OTHER_POWER_MANAGER_SERVER_IP]",
      "power_manager_server_port": "[OTHER_POWER_MANAGER_SERVER_PORT]"
    },
    ...
  },
  "devices": {
    "[DEVICE_ID_1]": "[SERVER_NAME]",
    "[DEVICE_ID_2]": "[OTHER_SERVER_NAME]"
  },
  "ip_whitelist": [
    "[CLIENT_IP]"
  ],
  "certs": {
    "root_cert_path": "[ROOT_CERT_PATH](ca.crt)",
    "client_cert_path": "[CLIENT_CERT_PATH](C.crt)",
    "client_cert_key_path": "[CLIENT_CERT_KEY_PATH](C.key)"
  }
}
```
### Example
#### Case 1. PowerManager 로컬 서버(192.168.0.4, 443) 가 1대인 경우
```json
{
  "ip": "192.168.0.3",
  "port": "18080",
  "server": {
    "my_local_server": {
      "default": true,
      "use_cert": true,
      "power_manager_server_ip": "192.168.0.4",
      "power_manager_server_port": "443"
    }
  },
  "ip_whitelist": [
    "192.168.0.3",
    "192.168.0.4",
    "192.168.0.5"
  ],
  "certs": {
    "root_cert_path": "C:\\Certificate\\newcerts\\ca.crt",
    "client_cert_path": "C:\\Certificate\\newcerts\\C.crt",
    "client_cert_key_path": "C:\\Certificate\\private\\C.key"
  }
}
```
#### Case 2. PowerManager 로컬 서버가 2대인 경우
```text
PowerManager 로컬 서버 정보(동일한 인증서를 사용시에만 가능)
1. [내부 서버, default] 192.168.0.3, 443
2. [외부 서버] www.myserver.com, 20443

192.168.0.3 로컬 서버에 붙은 device id
ab1234cde55b
cd5678fgh67c

www.myserver.com 로컬 서버에 붙은 device id
ef1357cdf25g
gh5218fgg62d  
```
```json
{
  "ip": "192.168.0.3",
  "port": "18080",
  "server": {
    "my_local_server": {
      "default": true,
      "use_cert": true,
      "power_manager_server_ip": "192.168.0.3",
      "power_manager_server_port": "443"
    },
    "my_external_server": {
      "use_cert": true,
      "power_manager_server_ip": "www.myserver.com",
      "power_manager_server_port": "20443"
    }
  },
  "devices": {
    "ef1357cdf25g": "my_external_server",
    "gh5218fgg62d": "my_external_server"
  },
  "ip_whitelist": [
    "192.168.0.3",
    "192.168.0.4",
    "192.168.0.5"
  ],
  "certs": {
    "root_cert_path": "C:\\Certificate\\newcerts\\ca.crt",
    "client_cert_path": "C:\\Certificate\\newcerts\\C.crt",
    "client_cert_key_path": "C:\\Certificate\\private\\C.key"
  }
}
```
## 2. 실행
### 1. Windows OS
- pmws-v1.0.0.zip 압축 파일을 다운로드 받습니다.
- 다운로드 받은 파일의 압축을 풀고 파일이 위치하는 곳에서 cmd 창을 켜서 아래와 같은 방법으로 실행합니다.
```shell
> cd [압축 푼 디렉토리 경로]
> pm-server.exe
```
### 2. Others
- Python 3.9 기반에서 작성되었습니다.
- 해당 프로젝트를 clone 후 디렉토리로 이동합니다.
- 패키지를 다운로드 받습니다.
  ```shell
  $ pip3 install -r requirements.txt
  ```
- 이후부터는 case 1 혹은 2 를 수행하시면 됩니다.
#### Case 1. Build
- 아래 명령과 같이 실행합니다.
  ```shell
  $ pyinstaller pm-server.spec
  ```
- dist 디렉토리로 이동하여 아래 명령과 같이 실행합니다.
  ```shell
  $ ./pm-server
  ```
#### Case 2. Run script
- 아래 명령과 같이 실행합니다.
  ```shell
  $ python3 pm-server.py
  ```
## 3. API 설명
### 스위치
#### 1. 스위치 ON
```text
http://[SERVER_IP]:[PORT]/device/switch/[DEVICE_ID]/On
```
- 예제
  ```text
  http://192.168.0.3:18080/device/switch/cd5678fgh67c/On
  ```
  ```json
  {
      "code": null,
      "message": null,
      "statusCode": 1
  }
  ```
#### 2. 스위치 OFF
```text
http://[SERVER_IP]:[PORT]/device/switch/[DEVICE_ID]/Off
```
- 예제
  ```text
  http://192.168.0.3:18080/device/switch/cd5678fgh67c/Off
  ```
  ```json
  {
      "code": null,
      "message": null,
      "statusCode": 1
  }
  ```
#### 3. 현재 스위치 상태
```text
http://[SERVER_IP]:[PORT]/device/switch/[DEVICE_ID]/status
```
```text
{
    "on": [BOOLEAN 값]
}
```
- 예제(해당 장치는 꺼져 있는 상태)
  ```text
  http://192.168.0.3:18080/device/switch/cd5678fgh67c/status
  ```
  ```json
  {
      "on": false
  }
  ```
### 센서
#### 1. 스위치 내 센서 현재 상태
```text
http://[SERVER_IP]:[PORT]/device/status/[DEVICE_ID]
```
- 예제
  ```text
  http://192.168.0.3:18080/device/status/cd5678fgh67c
  ```
  ```json
  {
      "currentWatt": 597.06,
      "dayPrice": 978.7500132611106,
      "monthPrice": 5664.4117207111385,
      "originalVolt": 216.96,
      "switch": 1,
      "temperature": 0,
      "version": "2.01.58",
      "volt": 216.96,
      "voltError": 0
  }
  ```
## 4. Home Assistant 연동 방법
### configuration.yaml
```yaml
...
sensor: !include sensors.yaml
switch: !include switches.yaml
binary_sensor: !include binary_sensors.yaml
...
```
### switches.yaml
```yaml
...
- platform: command_line
  switches:
    [스위치 이름]:
      command_on: curl -s http://[SERVER_IP]:[PORT]/device/switch/[DEVICE_ID]/On
      command_off: curl -s http://[SERVER_IP]:[PORT]/device/switch/[DEVICE_ID]/Off
      command_state: curl -s http://[SERVER_IP]:[PORT]/device/switch/[DEVICE_ID]/status
      value_template: >-
        {{ value_json.on }}
...
```
- 예제
  ```yaml
  ...
  - platform: command_line
    switches:
      main_multitab_switch:
        command_on: curl -s http://192.168.0.3:18080/device/switch/cd5678fgh67c/On
        command_off: curl -s http://192.168.0.3:18080/device/switch/cd5678fgh67c/Off
        command_state: curl -s http://192.168.0.3:18080/device/switch/cd5678fgh67c/status
        value_template: >-
          {{ value_json.on }}
  ...
  ```
### sensors.yaml
```yaml
...
- platform: command_line
  name: [name]
  unique_id: [id, name 과 동일해도 되나 띄어쓰기 없애기]
  command: curl -s http://[SERVER_IP]:[PORT]/device/status/[DEVICE_ID]
  scan_interval: 10
  unit_of_measurement: W
  value_template: >-
    {% set watt = value_json.currentWatt %}
      {{ watt }}
...
```
- 예제
  ```yaml
  ...
  - platform: command_line
    name: main multitab usage
    unique_id: main_multitab_usage
    command: curl -s http://192.168.0.3:18080/device/status/cd5678fgh67c
    scan_interval: 10
    unit_of_measurement: W
    value_template: >-
      {% set watt = value_json.currentWatt %}
        {{ watt }}
  ...
  ```
### binary_sensors.yaml  
```yaml
  ...
  - platform: command_line
    name: [name, 띄어쓰기 없이]
    command: curl -s http://[SERVER_IP]:[PORT]/device/connection/[DEVICE_ID]
    device_class: connectivity
    payload_on: "connected"
    payload_off: "disconnected"
    scan_interval: 20
  ...
```
- 예제
  ```yaml
  ...
  - platform: command_line
    name: main_multitab_connection
    command: curl -s http://192.168.0.3:18080/device/connection/cd5678fgh67c
    device_class: connectivity
    payload_on: "connected"
    payload_off: "disconnected"
    scan_interval: 20
  ...
  ```