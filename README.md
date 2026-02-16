# 🟣 PHD SOLUTIONS HDMI Matrix Switch — Home Assistant Integration
### Version: `0.0.1`

[![Add to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](
https://my.home-assistant.io/redirect/hacs_repository/?owner=marsh4200&repository=phd_solutions&category=integration
)

<a href="https://my.home-assistant.io/redirect/config_flow_start/?domain=phd_solutions" target="_blank"></a>




A custom [Home Assistant](https://www.home-assistant.io/) integration by **@marsh4200** for controlling and monitoring the **PHD 4K444 HDMI Matrix Switch**.  
This integration communicates directly with the matrix over **TCP (port 23)** to manage **power** and **HDMI routing** — fully **local** with **no cloud dependency**.

---

## ✨ Features

- ✅ Power **ON / OFF** control  
- ✅ Real-time **Power Status Sensor**  
- ✅ **Input → Output** HDMI routing control  
- ✅ Works **locally** — no internet or cloud required  
- ⚙️ Simple setup through **HACS**

> **Supported Functions:** Power & Routing Only

---

## ⚙️ Installation

1. Open **Home Assistant → HACS → Integrations → ⋮ → Custom repositories**
2. Add the repository:


**Category:** `Integration`

3. Click **Add**, then search for **PHD 4K444 Matrix** in HACS  
4. Click **Install** and **Restart Home Assistant**
5. Go to **Settings → Devices & Services → Add Integration → PHD 4K444 Matrix**
6. Enter the details below:

| Setting | Description | Example |
|----------|--------------|----------|
| **Host** | IP address of your matrix | `192.168.45.11` |
| **Port** | Control port (default) | `23` |

---

## 🎛️ Entities Created

| Entity | Type | Description |
|---------|------|-------------|
|                | Switch | Toggle matrix power |
|                | Sensor | Displays power state (ON/OFF) |

> 💡 Additional routing entities are created for each input → output combination (16 total).

---

## 🔹 HDMI Routing Control

Each button entity sends a **direct command** to route a specific input to an output.  
You can assign these to dashboard buttons, scripts, or automations.

| Input | Output | Description |
|:------:|:------:|-------------|
| 1 | 1 | Input 1 → Output 1 |
| 1 | 2 | Input 1 → Output 2 |
| 1 | 3 | Input 1 → Output 3 |
| 1 | 4 | Input 1 → Output 4 |
| 2 | 1 | Input 2 → Output 1 |
| 2 | 2 | Input 2 → Output 2 |
| 2 | 3 | Input 2 → Output 3 |
| 2 | 4 | Input 2 → Output 4 |
| 3 | 1 | Input 3 → Output 1 |
| 3 | 2 | Input 3 → Output 2 |
| 3 | 3 | Input 3 → Output 3 |
| 3 | 4 | Input 3 → Output 4 |
| 4 | 1 | Input 4 → Output 1 |
| 4 | 2 | Input 4 → Output 2 |
| 4 | 3 | Input 4 → Output 3 |
| 4 | 4 | Input 4 → Output 4 |

---

## 🧩 Example Dashboard Card

```yaml
type: grid
title: 🎛️ PHD 4K444 Matrix
columns: 4
cards:
- type: button
 entity: switch.phd_4k444_power
 name: Power
- type: button
 entity: switch.input_1_output_1
 name: Input 1 → Output 1
- type: button
 entity: switch.input_1_output_2
 name: Input 1 → Output 2
- type: button
 entity: switch.input_1_output_3
 name: Input 1 → Output 3
